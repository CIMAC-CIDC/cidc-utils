"""
Defines caching before for user preferences
"""

import jwt
import time
from cachetools import TTLCache
from typing import Optional


class CredentialCache(TTLCache):
    """
    Subclass of TTLCache that temporarily stores and retreives user login credentials

    Arguments:
        TTLCache {TTLCache} -- A TTLCache object

    Returns:
        CredentialCache -- [description]
    """

    def cache_key(self, key):
        """
        Adds an access key to the cache

        Arguments:
            key {str} -- Google access token.
        """
        self["access_token"] = key

    def get_key(self) -> Optional[str]:
        """
        Retreive key from cache.
        """
        if "access_token" in self and self["access_token"]:
            try:
                decode = jwt.decode(self["access_token"], verify=False)
                exp = decode["exp"]
                if time.time() > exp:
                    print("Your token has expired!")
                    self["access_token"] = None
                return self["access_token"]
            except jwt.exceptions.DecodeError:
                print("This token is not a valid JWT!")
                return None
