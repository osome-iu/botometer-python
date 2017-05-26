from __future__ import print_function
import time
import warnings
from functools import wraps

import requests
from requests import ConnectionError, Timeout
import tweepy
from tweepy import RateLimitError, TweepError


class NoTimelineError(ValueError):
    def __init__(self, sn, *args, **kwargs):
        msg = "user '%s' has no tweets in timeline" % sn
        super(NoTimelineError, self).__init__(msg, *args, **kwargs)


class Botometer(object):
    _TWITTER_RL_MSG = 'Rate limit exceeded for Twitter API method'

    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret, mashape_key=None, **kwargs):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.wait_on_ratelimit = kwargs.get('wait_on_ratelimit', False)

        self.mashape_key = mashape_key

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token_key, self.access_token_secret)
        self.twitter_api = tweepy.API(
            auth,
            parser=tweepy.parsers.JSONParser(),
            wait_on_rate_limit=self.wait_on_ratelimit,
            )

        self.api_url = kwargs.get('botometer_api_url',
                                  'https://osome-botometer.p.mashape.com')
        self.api_version = kwargs.get('botometer_api_version', 2)

    @classmethod
    def create_from(cls, instance, **kwargs):
        my_kwargs = vars(instance)
        my_kwargs.update(kwargs)
        return cls(**my_kwargs)


    def _add_mashape_header(self, kwargs):
        if self.mashape_key:
            kwargs.setdefault('headers', {}).update({
                'X-Mashape-Key': self.mashape_key
            })
        return kwargs

    def _bom_get(self, *args, **kwargs):
        self._add_mashape_header(kwargs)
        return requests.get(*args, **kwargs)

    def _bom_post(self, *args, **kwargs):
        self._add_mashape_header(kwargs)
        return requests.post(*args, **kwargs)

    def _get_twitter_data(self, user, full_user_object=False):
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


    def check_accounts_in(self, accounts, full_user_object=False, **kwargs):
        sub_instance = self.create_from(self, wait_on_ratelimit=True)

        max_retries = kwargs.get('retries', 3)
        num_retries = 0

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
                except (Timeout, ConnectionError) as e:
                    if num_retries >= max_retries:
                        raise
                    else:
                        time.sleep(2 ** num_retries)

                if result is not None:
                    yield account, result
                    break
