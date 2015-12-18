# BotOrNot Python API
A Python API for [Truthy BotOrNot](http://truthy.indiana.edu/botornot/).

Behind the scenes, this uses the BotOrNot's REST endpoint as illustrated in
[this notebook](http://truthy.indiana.edu/botornot/rest-api.html).

## Quickstart

```python
import botornot

twitter_app_auth = {
    'consumer_key': 'xxxxxxxx',
    'consumer_secret': 'xxxxxxxxxx',
    'access_token': 'xxxxxxxxx',
    'access_token_secret': 'xxxxxxxxxxx',
  }
bon = botornot.BotOrNot(**twitter_app_auth)

bon.check_account('@clayadavis')
```

Result:
```json
{
  "score": 0.37,
  "meta": {"screen_name": "clayadavis", "user_id": "1548959833"},
  "categories": {
    "content_classification": 0.27,
    "friend_classification": 0.15,
    "network_classification": 0.17,
    "sentiment_classification": 0.25,
    "temporal_classification": 0.43,
    "user_classification": 0.36
  }
}
```

## Install instructions

1. Clone this repository and navigate to it with your terminal of choice.
2. `python setup.py install`

## Dependencies

### Python dependencies
* [requests](http://docs.python-requests.org/en/latest/)
* [tweepy](https://github.com/tweepy/tweepy)

Both of these dependencies are available via `pip`, so you can install both at once with

    pip install requests tweepy
    
### Twitter app
In order to access Twitter's API, one needs to have/create a [Twitter app](https://apps.twitter.com/).
Once you've created an app, the authentication info can be found in the "Keys and Access Tokens" tab of the app's properties:
![Screenshot of app "Keys and Access Tokens"](https://s3.amazonaws.com/clayadavis_public/twitter_app_keys.png)


