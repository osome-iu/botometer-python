import requests


class BotometerBase(object):
    def __init__(self, rapidapi_key, **kwargs):
        self.rapidapi_key = rapidapi_key

        self.api_url = kwargs.get(
            "botometer_api_url", "https://botometer-pro.p.rapidapi.com"
        )

    def _add_rapidapi_header(self, kwargs):
        if self.rapidapi_key:
            kwargs.setdefault("headers", {}).update(
                {"x-rapidapi-key": self.rapidapi_key}
            )

        return kwargs

    def _bom_get(self, *args, **kwargs):
        self._add_rapidapi_header(kwargs)
        return requests.get(*args, **kwargs)

    def _bom_post(self, *args, **kwargs):
        self._add_rapidapi_header(kwargs)
        return requests.post(*args, **kwargs)

    ####################
    ## Public methods ##
    ####################

    def bom_api_path(self, method=""):
        return "/".join(
            [
                self.api_url.rstrip("/"),
                str(self.api_version),
                method,
            ]
        )


class BotometerX(BotometerBase):
    """
    Class to interact with the Botometer X API endpoint.

    Lists of user_ids and/or screen_names with more than 100 elements would be truncated to 100.
    Users are responsible to handle the exceptions.
    """

    TWEETS_PER_REQUEST = 100

    def __init__(self, rapidapi_key, **kwargs):
        super(BotometerX, self).__init__(rapidapi_key, **kwargs)

        self.api_version = "botometer-x"

    def _is_list_of_type(self, list_to_check, type_to_check):
        if isinstance(list_to_check, list):
            return all(isinstance(item, type_to_check) for item in list_to_check)
        return False

    def get_botscores_in_batch(self, user_ids=None, usernames=None):
        """
        Get botscores based on a list of user_ids and/or screen_names.
        There should be no more than 100 accounts in the query.
        """
        # Assign default values if not provided
        user_ids = [] if user_ids is None else user_ids
        usernames = [] if usernames is None else usernames

        if not self._is_list_of_type(user_ids, int) and not self._is_list_of_type(
            user_ids, str
        ):
            raise ValueError("user_ids must be a list of integers or strings")

        if not self._is_list_of_type(usernames, str):
            raise ValueError("usernames must be a list of strings")

        if len(user_ids) == 0 and len(usernames) == 0:
            raise ValueError("Must provide either user_ids or usernames")

        N_BOTSCORES_PER_QUERY = 100

        # Will only query the first N_BOTS_PER_QUERY items
        if len(user_ids) > N_BOTSCORES_PER_QUERY:
            # We have enough user ids, so we will query the first N_BOTS_PER_QUERY and ignore the usernames
            user_ids = user_ids[:N_BOTSCORES_PER_QUERY]
            usernames = []
        else:
            # We will query all the user ids plus N_BOTS_PER_QUERY - len(user_ids) usernames
            usernames = usernames[: N_BOTSCORES_PER_QUERY - len(user_ids)]
        payload = {
            "user_ids": user_ids,
            "usernames": usernames,
        }

        url = self.bom_api_path("get_botscores_in_batch")
        bom_resp = self._bom_post(url, json=payload)
        bom_resp.raise_for_status()
        return bom_resp.json()
