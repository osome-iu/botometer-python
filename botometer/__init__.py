from __future__ import print_function
import time

import requests
from requests import ConnectionError, HTTPError, Timeout
import tweepy
from tweepy.error import RateLimitError, TweepError
import datetime


class NoTimelineError(ValueError):
    def __init__(self, sn, *args, **kwargs):
        msg = "user '%s' has no tweets in timeline" % sn
        super(NoTimelineError, self).__init__(msg, *args, **kwargs)


class Botometer(object):
    _TWITTER_RL_MSG = 'Rate limit exceeded for Twitter API method'

    def __init__(self,
                 consumer_key, consumer_secret,
                 access_token=None, access_token_secret=None,
                 rapidapi_key=None,
                 **kwargs):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.wait_on_ratelimit = kwargs.get('wait_on_ratelimit', False)

        self.rapidapi_key = rapidapi_key or kwargs.get('mashape_key')

        if self.access_token_key is None or self.access_token_secret is None:
            auth = tweepy.AppAuthHandler(
                self.consumer_key, self.consumer_secret)
        else:
            auth = tweepy.OAuthHandler(
                self.consumer_key, self.consumer_secret)
            auth.set_access_token(
                self.access_token_key, self.access_token_secret)

        self.twitter_api = tweepy.API(
            auth,
            parser=tweepy.parsers.JSONParser(),
            wait_on_rate_limit=self.wait_on_ratelimit,
            )

        self.api_url = kwargs.get('botometer_api_url',
                                  'https://botometer-pro.p.rapidapi.com')
        self.api_version = kwargs.get('botometer_api_version', 4)

    @classmethod
    def create_from(cls, instance, **kwargs):
        my_kwargs = vars(instance)
        my_kwargs.update(kwargs)
        return cls(**my_kwargs)


    def _add_rapidapi_header(self, kwargs):
        if self.rapidapi_key:
            kwargs.setdefault('headers', {}).update({
                'x-rapidapi-key': self.rapidapi_key
            })
        return kwargs

    def _bom_get(self, *args, **kwargs):
        self._add_rapidapi_header(kwargs)
        return requests.get(*args, **kwargs)

    def _bom_post(self, *args, **kwargs):
        self._add_rapidapi_header(kwargs)
        return requests.post(*args, **kwargs)

    def _get_twitter_data(self, user, full_user_object=False):
        try:
            user_timeline = self.twitter_api.user_timeline(
                    user,
                    include_rts=True,
                    count=200,
                    )

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

        payload = {
            'mentions': search['statuses'],
            'timeline': user_timeline,
            'user': user_data,
        }

        if not full_user_object:
            payload['user'] = {
                'id_str': user_data['id_str'],
                'screen_name': user_data['screen_name'],
            }

        return payload


    ####################
    ## Public methods ##
    ####################

    def bom_api_path(self, method=''):
        return '/'.join([
            self.api_url.rstrip('/'),
            str(self.api_version),
            method,
        ])


    def check_account(self, user, full_user_object=False):
        payload = self._get_twitter_data(user,
                                         full_user_object=full_user_object)
        if not payload['timeline']:
            raise NoTimelineError(payload['user'])

        url = self.bom_api_path('check_account')
        bom_resp = self._bom_post(url, json=payload)
        bom_resp.raise_for_status()
        classification = bom_resp.json()

        return classification


    def check_accounts_in(self, accounts, full_user_object=False,
                          on_error=None, **kwargs):

        sub_instance = self.create_from(self, wait_on_ratelimit=True,
                                        botometer_api_url=self.api_url)
        max_retries = kwargs.get('retries', 3)

        for account in accounts:
            for num_retries in range(max_retries + 1):
                result = None
                try:
                    result = sub_instance.check_account(
                        account, full_user_object=full_user_object)
                except (TweepError, NoTimelineError) as e:
                    err_msg = '{}: {}'.format(
                        type(e).__name__,
                        getattr(e, 'msg', '') or getattr(e, 'reason', ''),
                        )
                    result = {'error': err_msg}
                except (ConnectionError, HTTPError, Timeout) as e:
                    if num_retries >= max_retries:
                        raise
                    else:
                        time.sleep(2 ** num_retries)
                except Exception as e:
                    if num_retries >= max_retries:
                        if on_error:
                            on_error(account, e)
                        else:
                            raise

                if result is not None:
                    yield account, result
                    break


class BotometerLite(Botometer):
    """
    Class to interact with the BotometerLite API.
    The present class has two modes: the Twitter mode and the non-Twitter mode.

    Non-Twitter mode:
        No Twitter APP key is required in this mode, i.e., only rapidapi_key is required.
        The users provide a list of no more than 100 tweets that they want to perform
        bot detection on.
        Via the self.check_accounts_from_tweets method, the present class
        queries the RapidAPI to fetch the botscores.

    Twitter mode:
        A valid Tiwtter APP key is required in this mode, i.e., consumer_key, consumer_secret,
        and rapidapi_key are required.
        The users provide a list of no more than 100 user_ids or screen_names.
        Via the self.check_accounts_from_user_ids or check_accounts_from_screen_names method,
        the the present class first queries the Twitter user lookup API to fetch the user profiles,
        then queries the RapidAPI to fetch the botscore.

    Lists of tweets/user_ids/screen_names with more than 100 elements would be truncated to 100.
    The users are responsible to handle the exceptions.
    """
    TWEETS_PER_REQUEST = 100
    def __init__(
        self,
        rapidapi_key=None,
        consumer_key=None,
        consumer_secret=None,
        access_token=None,
        access_token_secret=None,
        **kwargs
    ):
        self.twitter_mode = False
        lite_api_url = kwargs.get(
                'botometerlite_api_url',
                'https://botometer-pro.p.rapidapi.com'
            )
        if consumer_key is None or consumer_secret is None:
        # No Twitter mode: the users provide the tweets
            self.api_url = lite_api_url
        else:
        # Twitter mode: use Twitter lookup to fetch user profile
            self.twitter_mode = True
            super(BotometerLite, self).__init__(
                consumer_key,
                consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                botometer_api_url=lite_api_url,
                wait_on_ratelimit=kwargs.get('wait_on_ratelimit', False)
            )

        self.api_version = kwargs.get('botometerlite_api_version', 'litev1')
        self.rapidapi_key = rapidapi_key or kwargs.get('mashape_key')

    def _get_utc_now(self):
        now_time = datetime.datetime.now(datetime.timezone.utc)
        return datetime.datetime.strftime(
            now_time, '%a %b %d %H:%M:%S %z %Y'
        )

    def _get_twitter_data(self, **kwargs):
        try:
            user_objs = self.twitter_api.lookup_users(**kwargs)
        except RateLimitError as e:
            e.args = (self._TWITTER_RL_MSG, 'users/lookup')
            raise e
        return user_objs

    def _check_accounts_twitter_mode(self, query, **kwargs):
        assert self.twitter_mode, "Twitter app key missing"

        user_objs = self._get_twitter_data(**query)
        now_str = self._get_utc_now()

        dummy_tweets = []
        for user_obj in user_objs:
            dummy_tweets.append({
                'created_at': now_str,
                'user': user_obj
            })
        return self.check_accounts_from_tweets(dummy_tweets)

    def check_accounts_from_user_ids(self, user_ids, **kwargs):
        """
        Check accounts based on a list of user_ids.
        The list should contain no more than 100 elements.
        A valid Twitter APP key is required.
        """
        query = {"user_ids": list(user_ids)[:self.TWEETS_PER_REQUEST]}
        return self._check_accounts_twitter_mode(query, **kwargs)

    def check_accounts_from_screen_names(self, screen_names, **kwargs):
        """
        Check accounts based on a list of screen_names (please remove the @).
        The list should contain no more than 100 elements.
        A valid Twitter APP key is required.
        """
        query = {"screen_names": list(screen_names)[:self.TWEETS_PER_REQUEST]}
        return self._check_accounts_twitter_mode(query, **kwargs)

    def check_accounts_from_tweets(self, tweets):
        """
        Check accounts based on a list of tweets.
        The list should contain no more than 100 elements.
        No Twitter APP key is required.
        """
        url = self.bom_api_path('check_accounts_in_bulk')
        bom_resp = self._bom_post(url, json=tweets)
        bom_resp.raise_for_status()
        classification = bom_resp.json()

        return classification
