[![PyPI version](https://badge.fury.io/py/botometer.svg)](https://badge.fury.io/py/botometer)

# Botometer X Python API

A Python API for [Botometer X by OSoMe](https://osome.iu.edu).
Previously known as `botornot-python`.

Behind the scenes, this uses the Botometer's HTTP endpoint, available via
[RapidAPI](https://rapidapi.com/OSoMe/api/botometer-pro).

RapidAPI usage/account related questions should be posted on RapidAPI discussion.

## [Change Note/Announcement]

### June, 2024

We are releasing a new API endpoint for Botometer X.

Unlike the original Botometer that fetched data from Twitter and calculated bot scores on the fly, Botometer X is in archival mode and relies on pre-calculated scores based on historical data collected before June 2023.
The API endpoint allows users to fetch scores in bulk using a list of user ids or screen names, without the need of a Twitter/X's developer account.

For details of Botometer X, please refer to the [FQA](https://botometer.osome.iu.edu/faq).


## Help
> You probably want to have a look at [Troubleshooting & FAQ](https://github.com/osome-iu/botometer-python/wiki/Troubleshooting-&-FAQ) in the wiki. Please feel free to suggest and/or contribute improvements to that page.

## Prior to Utilizing Botometer
To begin using Botometer X, you must follow the steps below before running any code:
1. Create a free [RapidAPI](https://rapidapi.com/) account.
2. Subscribe to [Botometer Pro](https://rapidapi.com/OSoMe/api/botometer-pro) on RapidApi by selecting a plan.
    > There is a completely free version (which does not require any credit card information) for testing purposes.
3. Ensure Botometer Pro's dependencies are already installed.
    > See the [Dependencies](#dependencies) section for details.

## Quickstart
From your command shell, run

```
pip install botometer
```

### Botometer X

To access the Botometer X endpoint, enter something like this in a Python shell or script:

```python
import botometer

rapidapi_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

bomx = botometer.BotometerX(rapidapi_key=rapidapi_key)
```


```python
# Check accounts by usernames, note that @ is optional
bomx.get_botscores_in_batch(usernames=['@OSoMe_IU', 'botometer'])

# Check accounts by ids
bomx.get_botscores_in_batch(user_ids=[2451308594, 187521608])

# Check accounts by both usernames and ids
bomx.get_botscores_in_batch(usernames=['@OSoMe_IU'], user_ids=[2451308594])
```

The queries will return results like those below:

```json
[
    {
        "bot_score": 0.09,
        "timestamp": "Sat, 27 May 2023 23:57:16 GMT",
        "user_id": "2451308594",
        "username": "Botometer"
    },
    {
        "bot_score": 0.21,
        "timestamp": "Thu, 25 May 2023 22:54:53 GMT",
        "user_id": "187521608",
        "username": "OSoMe_IU"
    }
]
```
The response will be a list of JSON objects.
Meanings of the elements in the object:
- `bot_score`: The bot score, a float number between 0 and 1 (note that we rescale the score to 1 to 5 on the Botometer X website)
- `timestamp`: The time when the bot score was calculated
- `user_id`: ID of the account
- `username`: Username of the account

For more information on the API, consult the [API Overview](https://rapidapi.com/OSoMe/api/botometer-pro/details) on RapidAPI.


## Installation instructions

This package is on PyPI so you can install it with pip:

```
$ pip install botometer
```

## Dependencies

### Python dependencies
* [requests](http://docs.python-requests.org/en/latest/)

The dependency should be installed automatically with pip.

## References

- **Botometer X:** The scores are calculated using the BotometerLite model.

- ***Botometer v4:*** Mohsen Sayyadiharikandeh, Onur Varol, Kai-Cheng Yang, Alessandro Flammini, Filippo Menczer. "Detection of Novel Social Bots by Ensembles of Specialized Classifiers." [DOI](https://doi.org/10.1145/3340531.3412698), [ArXiv](https://arxiv.org/abs/2006.06867)

- ***BotometerLite:*** Yang, K.; Varol, O.; Hui, P.; and Menczer, F. "Scalable and Generalizable Social Bot Detection through Data Selection." AAAI (2020). [DOI](http://doi.org/10.1609/aaai.v34i01.5460), [ArXiv](https://arxiv.org/abs/1911.09179)

- ***Botometer v3:*** Yang, Kai‐Cheng, Onur Varol, Clayton A. Davis, Emilio Ferrara, Alessandro Flammini, and Filippo Menczer. "Arming the public with artificial intelligence to counter social bots." Human Behavior and Emerging Technologies 1, no. 1 (2019): 48-61. [DOI](https://onlinelibrary.wiley.com/doi/full/10.1002/hbe2.115), [ArXiv](https://arxiv.org/abs/1901.00912)

- ***Botometer v2:*** Varol, Onur, Emilio Ferrara, Clayton A. Davis, Filippo Menczer, and Alessandro Flammini. "Online Human-Bot Interactions: Detection, Estimation, and Characterization." ICWSM (2017). [AAAI](https://aaai.org/ocs/index.php/ICWSM/ICWSM17/paper/view/15587), [ArXiv](https://arxiv.org/abs/1703.03107)

- ***Botometer v1 aka BotOrNot:*** Davis, C. A., Varol, O., Ferrara, E., Flammini, A., & Menczer, F. (2016, April). "BotOrNot: A system to evaluate social bots". In Proceedings of the 25th International Conference Companion on World Wide Web (pp. 273-274). International World Wide Web Conferences Steering Committee. [DOI](https://doi.org/10.1145/2872518.2889302), [ArXiv](https://arxiv.org/abs/1602.00975)

- Varol O., Davis C., Menczer, F., Flammini, A. "Feature Engineering for Social Bot Detection", Feature Engineering for Machine Learning and Data Analytics [Google Books](https://books.google.com/books?id=661SDwAAQBAJ&lpg=PA311&dq=info%3AsM983rg_yb8J%3Ascholar.google.com&lr&pg=PA311#v=onepage&q&f=false)

- Ferrara, Emilio, Onur Varol, Clayton Davis, Filippo Menczer, and Alessandro Flammini. "The rise of social bots." Communications of the ACM 59, no. 7 (2016): 96-104. [DOI](https://doi.org/10.1145/2818717), [ArXiv](https://arxiv.org/abs/1407.5225)
