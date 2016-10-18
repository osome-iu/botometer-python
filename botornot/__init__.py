from __future__ import print_function
import time
import tweepy
import requests
from functools import wraps
from tweepy import RateLimitError, TweepError
from requests import ConnectionError, Timeout


class NoTimelineError(ValueError):
    def __init__(self, sn, *args, **kwargs):
        msg = "user '%s' has no tweets in timeline" % sn
        return super(NoTimelineError, self).__init__(msg, *args, **kwargs)


class BotOrNot(object):
    _BON_RL_MSG = 'Rate limit exceeded for BotOrNot API method'
    _TWITTER_RL_MSG = 'Rate limit exceeded for Twitter API method'

    def __init__(self, consumer_key, consumer_secret,
            access_token, access_token_secret, **kwargs):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.wait_on_ratelimit = kwargs.get('wait_on_ratelimit', False)

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token_key, self.access_token_secret)
        self.twitter_api = tweepy.API(auth,
                parser=tweepy.parsers.JSONParser(),
                wait_on_rate_limit=self.wait_on_ratelimit)

        self.botornot_api = kwargs.get('botornot_api',
                'http://truthy.indiana.edu/botornot/api/')
        self.api_version = kwargs.get('api_version', 1)

        def _rate_limited(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                while True:
                    resp = func(*args, **kwargs)
                    try:
                        resp.raise_for_status()
                    except requests.HTTPError as e:
                        if resp.status_code == 429:
                            if self.wait_on_ratelimit:
                                data = resp.json()
                                secs = max(1, data['reset'] - data['current'])
                                time.sleep(secs)
                            else:
                                raise RateLimitError(self._BON_RL_MSG)
                        else:
                            raise
                    else:
                        return resp
            return wrapper

        self._bon_get = _rate_limited(requests.get)
        self._bon_post = _rate_limited(requests.post)


    @classmethod
    def create_from(cls, instance, **kwargs):
        my_kwargs = vars(instance)
        my_kwargs.update(kwargs)
        return cls(**my_kwargs)


    @property
    def bon_api_path(self, method=''):
        return  '%s/%s' % (self.botornot_api.rstrip('/'), self.api_version)


    def _bon_api_method(self, method=''):
        return '/'.join([self.bon_api_path.rstrip('/'), method.strip('/')])


    def _get_user_and_tweets(self, user):
        try:
            user_timeline = self.twitter_api.user_timeline(user, count=200)
        except RateLimitError as e:
            e.args = (self._TWITTER_RL_MSG, 'statuses/user_timeline')
            raise e

        if user_timeline:
            user_data = user_timeline[0]['user']
        else:
            user_data = self.twitter_api.get_user(user)
        screen_name = '@' + user_data['screen_name']

        try:
            search = self.twitter_api.search(screen_name, count=100)
        except RateLimitError as e:
            e.args = (self._TWITTER_RL_MSG, 'search/tweets')
            raise e

        tweets = user_timeline + search['statuses']

        return user_data, tweets


    def _check_account(self, user_data, tweets):
        post_body = {'content': tweets,
                     'meta': {'user_id': user_data['id_str'],
                              'screen_name': user_data['screen_name']}
                     }

        _url = self._bon_api_method('check_account')
        bon_resp = self._bon_post(_url, json=post_body)
        return bon_resp.json()


    ####################
    ## Public methods ##
    ####################


    def check_account(self, user):
        user_data, tweets = self._get_user_and_tweets(user)
        if not tweets:
            raise NoTimelineError(user)
        classification = self._check_account(user_data, tweets)

        return classification


    def check_accounts_in(self, accounts, **kwargs):
        sub_instance = self.create_from(self, wait_on_ratelimit=True)

        max_retries = kwargs.get('retries', 3)
        num_retries = 0

        for account in accounts:
            for num_retries in range(max_retries + 1):
                result = None
                try:
                    result = sub_instance.check_account(account)
                except (TweepError, NoTimelineError) as e:
                    err_msg = '{}: {}'.format(
                            type(e).__name__,
                            getattr(e, 'msg', '') or getattr(e, 'reason', ''),
                    )
                    result = {'error': err_msg}
                except (Timeout, ConnectionError) as e:
                    if num_retries >= max_retries:
                        raise
                    else:
                        time.sleep(2 ** num_retries)

                if result is not None:
                    yield account, result
                    break
