# Botometer Python API

A Python API for [Botometer by OSoMe](https://osome.iu.edu).
Previously known as `botornot-python`.

Behind the scenes, this uses the Botometer's HTTP endpoint, available via
[RapidAPI](https://rapidapi.com/OSoMe/api/botometer-pro).

RapidAPI usage/account related questions should be posted on RapidAPI discussion.

## [Change Note]

### September, 2020

We have a major update for Botometer:

1. Botometer has been upgraded to V4, and you can use the `/4/check_account` endpiont to access it.
2. The response of `/4/check_account` is reorganized.
3. A new endpoint for BotometerLite is added. It allows checking accounts in bulk.

You can see the full [announcement](https://cnets.indiana.edu/blog/2020/09/01/botometer-v4/) for details.

Due to the update, please upgrade `botometer-python` in your local environment to the newest version.
You may also need to modify your code to adapt to the new response from the API.
For more information, check out the documentation below.
If you want to try the new BotometerLite API, checkout the documentation below.

### May, 2020

We have made some changes to our API, please read the [announcement](https://twitter.com/Botometer/status/1250557098708144131) for details. Due to the API change, the old `botometer-python` package might stop to work. Please upgrade it in your local environment to the newest version.

## Help
> You probably want to have a look at [Troubleshooting & FAQ](https://github.com/IUNetSci/botometer-python/wiki/Troubleshooting-&-FAQ) in the wiki. Please feel free to suggest and/or contribute improvements to that page.

## Prior to Utilizing Botometer
To begin using Botometer, you must follow the steps below before running any code:
1. Create a free [RapidAPI](https://rapidapi.com/) account.
2. Subscribe to [Botometer Pro](https://rapidapi.com/OSoMe/api/botometer-pro) on RapidApi.
    > There is a completely free version (which does not require any credit card information) for testing purposes.
3. Create a Twitter application via https://developer.twitter.com/
    > Botometer utilizes the access credentials provided by Twitter for the application.
4. Ensure Botometer Pro's dependencies are already installed. 
    > See the [Dependencies](#dependencies) section for details.

**Note:** These steps are necessary to access credentials and download other packages which are needed for Botometer to work properly. Please see [RapidAPI and Twitter Access Details](#access) below for more details on this topic.

## Quickstart
From your command shell, run 

```
pip install botometer
```
### Botometer-V4

To access the Botometer-V4 API, enter something like this in a Python shell or script:

```python
import botometer

rapidapi_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
twitter_app_auth = {
    'consumer_key': 'xxxxxxxx',
    'consumer_secret': 'xxxxxxxxxx',
    'access_token': 'xxxxxxxxx',
    'access_token_secret': 'xxxxxxxxxxx',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
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
        "english": 0.8018818614025648,
        "universal": 0.5557322218336633
    },
    "display_scores": {
        "english": {
            "astroturf": 0.0,
            "fake_follower": 4.1,
            "financial": 1.5,
            "other": 4.7,
            "overall": 4.7,
            "self_declared": 3.2,
            "spammer": 2.8
        },
        "universal": {
            "astroturf": 0.3,
            "fake_follower": 3.2,
            "financial": 1.6,
            "other": 3.8,
            "overall": 3.8,
            "self_declared": 3.7,
            "spammer": 2.3
        }
    },
    "raw_scores": {
        "english": {
            "astroturf": 0.0,
            "fake_follower": 0.81,
            "financial": 0.3,
            "other": 0.94,
            "overall": 0.94,
            "self_declared": 0.63,
            "spammer": 0.57
        },
        "universal": {
            "astroturf": 0.06,
            "fake_follower": 0.64,
            "financial": 0.3133333333333333,
            "other": 0.76,
            "overall": 0.76,
            "self_declared": 0.74,
            "spammer": 0.47
        }
    },
    "user": {
        "majority_lang": "en",
        "user_data": {
            "id_str": "11330",
            "screen_name": "test_screen_name"
        }
    }
}
```

Meanings of the elements in the response:

* **user**: Twitter user object (from the user) plus the language inferred from majority of tweets
* **raw scores**: bot score in the [0,1] range, both using English (all features) and Universal (language-independent) features; in each case we have the overall score and the sub-scores for each bot class (see below for subclass names and definitions)
* **display scores**: same as raw scores, but in the [0,5] range
* **cap**: conditional probability that accounts with a score **equal to or greater than this** are automated; based on inferred language

Meanings of the bot type scores:

* `fake_follower`: bots purchased to increase follower counts 
* `self_declared`: bots from botwiki.org
* `astroturf`: manually labeled political bots and accounts involved in follow trains that systematically delete content
* `spammer`: accounts labeled as spambots from several datasets
* `financial `: bots that post using cashtags
* `other`: miscellaneous other bots obtained from manual annotation, user feedback, etc.

For more information on the response object, consult the [API Overview](https://rapidapi.com/OSoMe/api/botometer-pro/details) on RapidAPI.

### BotometerLite

In September, 2020, the BotometerLite endpoint was added. It leverages a lightweighted model and allows detecting likely bots in bulk.
Before accessing it, please make sure you have subscribed to the ULTRA plan on RapidAPI.

Unlike Botometer-V4, BotometerLite just needs the user profile information and the timestamp of when the information was collected to perform bot detection.
There are two modes for BotometerLite: non-Twitter mode and Twitter mode.

If you have already collected at least one tweet for each account you want to check, you can use the non-Twitter mode.
In this mode, you only need a RapidAPI key.

```python
import botometer

rapidapi_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
blt = botometer.BotometerLite(rapidapi_key=rapidapi_key)

# Prepare a list of tweets from the users that you want to perform bot detection on.
# The list should contain no more than 100 tweets.
tweet_list = [tweet1, tweet2, ...] 

blt_scores = blt.check_accounts_from_tweets(tweet_list)
```

Result:

```json
[
    {"botscore": 0.65, "tweet_id": "1234",  "user_id": 1111},
    {"botscore": 0.29, "tweet_id": "12345", "user_id": 2222}
]
```

Note that the tweet_id is also included in case multiple tweets from the same user are passed to the API.

If you only have a set of user_ids or screen_names, you will have to use the Twitter mode.
In addition to the RapidAPI key, this mode also requires a valid Twitter APP key.
The package would first query the Twitter user lookup API to fetch the user profiles, then pass the data to the Botometer Pro API
for the bot scores.

```python
import botometer

rapidapi_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
twitter_app_auth = {
    'consumer_key': 'xxxxxxxx',
    'consumer_secret': 'xxxxxxxxxx',
    'access_token': 'xxxxxxxxx',
    'access_token_secret': 'xxxxxxxxxxx',
  }
  
blt_twitter = botometer.BotometerLite(rapidapi_key=rapidapi_key, **twitter_app_auth)

# Prepare a list of screen_names you want to check.
# The list should contain no more than 100 screen_names; please remove the @
screen_name_list = ['yang3kc', 'onurvarol', 'clayadavis']
blt_scores = blt_twitter.check_accounts_from_screen_names(screen_name_list)

# Prepare a list of user_ids you want to check.
# The list should contain no more than 100 user_ids.
user_id_list = [1133069780917850112, 77436536, 1548959833]
blt_scores = blt_twitter.check_accounts_from_user_ids(user_id_list)
```

Result:
```json
[
    {"botscore": 0.17, "tweet_id": null, "user_id": 1133069780917850112},
    {"botscore": 0.2,  "tweet_id": null, "user_id": 77436536},
    {"botscore": 0.16, "tweet_id": null, "user_id": 1548959833}
]
```

The tweet_id is set to null in this mode.

Note that in the non-Twitter mode, the returned scores reflect the status of the accounts when the tweets were collected.
In the Twitter mode, on the other hand, the scores reflect the status of the accounts when you run the code, just like the Botometer-V4 endpoint.

## Install instructions
This package is on PyPI so you can install it with pip:

```
$ pip install botometer
```

<a id="dependencies"></a>
## Dependencies

### Python dependencies
* [requests](http://docs.python-requests.org/en/latest/)
* [tweepy](https://github.com/tweepy/tweepy)

Both of these dependencies are available via `pip`, so you can install both at once with

    pip install requests tweepy

<a id="access"></a>
## RapidAPI and Twitter Access Details

### RapidAPI key

Our API is served via [RapidAPI](//rapidapi.com). You must sign up
for a free account in order to obtain a RapidAPI secret key. The easiest way to
get your secret key is to visit
[our API endpoint page](https://rapidapi.com/OSoMe/api/botometer-pro/endpoints)
and look in the endpoint's header parametsrs for the "X-RapidAPI-Key" as shown below:

![Screenshot of RapidAPI header parameters](/docs/rapidapi_key.png)
    
### Twitter app
In order to access Twitter's API, one needs to have/create a [Twitter app](https://apps.twitter.com/).
Once you've created an app, the authentication info can be found in the "Keys and Access Tokens" tab of the app's properties:
![Screenshot of app "Keys and Access Tokens"](/docs/twitter_app_keys.png)

## Authentication
By default, Botometer uses **user authentication** when interacting with Twitter's API as it is the least restrictive and the ratelimit matches with Botometer's **Pro** plan: 180 requests per 15-minute window.
One can instead use Twitter's **application authentication** in order to take advantage of the higher ratelimit that matches our **Ultra** plan: 450 requests per 15-minute window. Do note the differences between user and app-only authentication found under the header "Twitter API Authentication Model" in [Twitter's docs on authentication](https://developer.twitter.com/en/docs/basics/authentication/overview/oauth).

To use app-only auth, just omit the `access_token` and `access_token_secret` in the `Botometer` constructor.

```python
import botometer

rapidapi_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # now it's called rapidapi key
twitter_app_auth = {
    'consumer_key': 'xxxxxxxx',
    'consumer_secret': 'xxxxxxxxxx'
    }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)
```

## References

- ***Botometer v4:*** Mohsen Sayyadiharikandeh, Onur Varol, Kai-Cheng Yang, Alessandro Flammini, Filippo Menczer. "Detection of Novel Social Bots by Ensembles of Specialized Classifiers." [ArXiv](https://arxiv.org/abs/2006.06867)

- ***BotometerLite:*** Yang, K.; Varol, O.; Hui, P.; and Menczer, F. "Scalable and Generalizable Social Bot Detection through Data Selection." AAAI (2020). [DOI](http://doi.org/10.1609/aaai.v34i01.5460), [ArXiv](https://arxiv.org/abs/1911.09179)

- ***Botometer v3:*** Yang, Kai‐Cheng, Onur Varol, Clayton A. Davis, Emilio Ferrara, Alessandro Flammini, and Filippo Menczer. "Arming the public with artificial intelligence to counter social bots." Human Behavior and Emerging Technologies 1, no. 1 (2019): 48-61. [DOI](https://onlinelibrary.wiley.com/doi/full/10.1002/hbe2.115), [ArXiv](https://arxiv.org/abs/1901.00912)

- ***Botometer v2:*** Varol, Onur, Emilio Ferrara, Clayton A. Davis, Filippo Menczer, and Alessandro Flammini. "Online Human-Bot Interactions: Detection, Estimation, and Characterization." ICWSM (2017). [AAAI](https://aaai.org/ocs/index.php/ICWSM/ICWSM17/paper/view/15587), [ArXiv](https://arxiv.org/abs/1703.03107)

- ***Botometer v1 aka BotOrNot:*** Davis, C. A., Varol, O., Ferrara, E., Flammini, A., & Menczer, F. (2016, April). "BotOrNot: A system to evaluate social bots". In Proceedings of the 25th International Conference Companion on World Wide Web (pp. 273-274). International World Wide Web Conferences Steering Committee. [DOI](https://doi.org/10.1145/2872518.2889302), [ArXiv](https://arxiv.org/abs/1602.00975)

- Varol O., Davis C., Menczer, F., Flammini, A. "Feature Engineering for Social Bot Detection", Feature Engineering for Machine Learning and Data Analytics [Google Books](https://books.google.com/books?id=661SDwAAQBAJ&lpg=PA311&dq=info%3AsM983rg_yb8J%3Ascholar.google.com&lr&pg=PA311#v=onepage&q&f=false)

- Ferrara, Emilio, Onur Varol, Clayton Davis, Filippo Menczer, and Alessandro Flammini. "The rise of social bots." Communications of the ACM 59, no. 7 (2016): 96-104. [DOI](https://doi.org/10.1145/2818717), [ArXiv](https://arxiv.org/abs/1407.5225)


```python

```
