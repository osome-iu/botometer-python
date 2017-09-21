# Botometer Python API
A Python API for [Botometer by OSoMe](https://osome.iuni.iu.edu).

Behind the scenes, this uses the Botometer's HTTP endpoint, available via
[Mashape Market](https://market.mashape.com/OSoMe/botometer).

## Help
You probably want to have a look at [Troubleshooting & FAQ](https://github.com/IUNetSci/botometer-python/wiki/Troubleshooting-&-FAQ) in the wiki. Please feel free to suggest and/or contribute improvements to that page.

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
bom = botometer.Botometer(wait_on_ratelimit=True,
                          mashape_key=mashape_key,
                          **twitter_app_auth)

# Check a single account
result = bom.check_account('@clayadavis')

# Check a sequence of accounts
accounts = ['@clayadavis', '@onurvarol', '@jabawack']
for screen_name, result in bom.check_accounts_in(accounts):
    # Do stuff
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

This package is on PyPI so you can install it with pip:

```
$ pip install botometer
```

## Dependencies

### Python dependencies
* [requests](http://docs.python-requests.org/en/latest/)
* [tweepy](https://github.com/tweepy/tweepy)

Both of these dependencies are available via `pip`, so you can install both at once with

    pip install requests tweepy

### Mashape Market API key
Our API is served via [Mashape Market](//market.mashape.com). You must sign up
for a free account in order to obtain a Mashape secret key. The easiest way to
get your secret key is to visit
[our API endpoint page](https://market.mashape.com/OSoMe/botometer)
and look in the "Request Example" as shown below:
![Screenshot of Mashape "Request example"](/docs/mashape_key.png)
    
### Twitter app
In order to access Twitter's API, one needs to have/create a [Twitter app](https://apps.twitter.com/).
Once you've created an app, the authentication info can be found in the "Keys and Access Tokens" tab of the app's properties:
![Screenshot of app "Keys and Access Tokens"](/docs/twitter_app_keys.png)

## References

- Varol, Onur, Emilio Ferrara, Clayton A. Davis, Filippo Menczer, and Alessandro Flammini. "Online Human-Bot Interactions: Detection, Estimation, and Characterization." ICWSM (2017). [AAAI](https://aaai.org/ocs/index.php/ICWSM/ICWSM17/paper/view/15587), [ArXiv](https://arxiv.org/abs/1703.03107)

- Davis, C. A., Varol, O., Ferrara, E., Flammini, A., & Menczer, F. (2016, April). BotOrNot: A system to evaluate social bots. In Proceedings of the 25th International Conference Companion on World Wide Web (pp. 273-274). International World Wide Web Conferences Steering Committee. [ArXiv](https://arxiv.org/abs/1602.00975), [ACM Library](http://dl.acm.org/citation.cfm?id=2889302)

- Ferrara, Emilio, Onur Varol, Clayton Davis, Filippo Menczer, and Alessandro Flammini. "The rise of social bots." Communications of the ACM 59, no. 7 (2016): 96-104. [ArXiv](https://arxiv.org/abs/1407.5225), [ACM Library](http://dl.acm.org/citation.cfm?id=2963119.2818717&coll=portal&dl=ACM)
