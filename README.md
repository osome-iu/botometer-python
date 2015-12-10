# BotOrNot Python API
A Python API for [Truthy BotOrNot](http://truthy.indiana.edu/botornot)

## Quickstart

```python
import botornot

twitter_app_auth = {
    'consumer_key': 'xxxxxxxx',
    'consumer_secret': 'xxxxxxxxxx',
    'access_token': 'xxxxxxxxx',
    'access_token_secret': 'xxxxxxxxxxx',
  )
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
