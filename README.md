# Botometer Python API

A Python API for [Botometer by OSoMe](https://osome.iuni.iu.edu).
Previously known as `botornot-python`.

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

# Check a single account by screen name
result = bom.check_account('@clayadavis')

# Check a single account by id
result = bom.check_account(1548959833)

# Check a sequence of accounts
accounts = ['@clayadavis', '@onurvarol', '@jabawack']
for screen_name, result in bom.check_accounts_in(accounts):
    # Do stuff with `screen_name` and `result`
```

Result:
```json
{
  "cap": {
    "english": 0.0011785984309163565,
    "universal": 0.0016912294273666159
  },
  "categories": {
    "content": 0.058082395351262375,
    "friend": 0.044435259626385865,
    "network": 0.07064549990637549,
    "sentiment": 0.07214003430676995,
    "temporal": 0.07924665710801207,
    "user": 0.027817972609638725
  },
  "display_scores": {
    "content": 0.3,
    "english": 0.1,
    "friend": 0.2,
    "network": 0.4,
    "sentiment": 0.4,
    "temporal": 0.4,
    "universal": 0.1,
    "user": 0.1
  },
  "scores": {
    "english": 0.0215615093045025,
    "universal": 0.0254864249403189
  },
  "user": {
    "id_str": "1548959833",
    "screen_name": "clayadavis",
    "...": "..."
  }
}
```

For more information on this response object, consule the [API Overview](https://market.mashape.com/OSoMe/botometer/overview#wiki-response-object) on Mashape.

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

- Davis, C. A., Varol, O., Ferrara, E., Flammini, A., & Menczer, F. (2016, April). "BotOrNot: A system to evaluate social bots". In Proceedings of the 25th International Conference Companion on World Wide Web (pp. 273-274). International World Wide Web Conferences Steering Committee. [ArXiv](https://arxiv.org/abs/1602.00975), [ACM Library](http://dl.acm.org/citation.cfm?id=2889302)

- Varol O., Davis C., Menczer, F., Flammini, A. "Feature Engineering for Social Bot Detection", Feature Engineering for Machine Learning and Data Analytics [Google Books](https://books.google.com/books?id=661SDwAAQBAJ&lpg=PA311&dq=info%3AsM983rg_yb8J%3Ascholar.google.com&lr&pg=PA311#v=onepage&q&f=false)


- Ferrara, Emilio, Onur Varol, Clayton Davis, Filippo Menczer, and Alessandro Flammini. "The rise of social bots." Communications of the ACM 59, no. 7 (2016): 96-104. [ArXiv](https://arxiv.org/abs/1407.5225), [ACM Library](http://dl.acm.org/citation.cfm?id=2963119.2818717&coll=portal&dl=ACM)
