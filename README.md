# Botometer Python API
A Python API for [Botometer by OSoMe](https://osome.iuni.iu.edu).

Behind the scenes, this uses the Botometer's HTTP endpoint, available via
[Mashape Market](https://market.mashape.com/OSoMe/botometer).

## Help
You probably want to have a look at [Troubleshooting & FAQ](/truthy/botometer-python/wiki/Troubleshooting-&-FAQ) in the wiki. Please feel free to suggest and/or contribute improvements to that page.

## Quickstart
From your command shell, run 

```
pip install botometer
```

then in a Python shell or script, enter something like this:
```python
import botometer

mashape_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
twitter_app_auth = {
    'consumer_key': 'xxxxxxxx',
    'consumer_secret': 'xxxxxxxxxx',
    'access_token': 'xxxxxxxxx',
    'access_token_secret': 'xxxxxxxxxxx',
  }
bom = botometer.Botometer(mashape_key=mashape_key, **twitter_app_auth)

# Check a single account
result = bom.check_account('@clayadavis')

# Check a sequence of accounts
accounts = ['@clayadavis', '@onurvarol', '@jabawack']
results = list(bom.check_accounts_in(accounts))
```

Result:
```json
{
  "categories": {
    "content": 0.18,
    "friend": 0.25,
    "network": 0.13,
    "sentiment": 0.19,
    "temporal": 0.31,
    "user": 0.44
  },
  "scores": {
    "english": 0.2,
    "universal": 0.25
  },
  "user": {
    "id_str": "1548959833",
    "screen_name": "clayadavis"
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


