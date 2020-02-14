import binascii
import os

from django.core.cache import cache


class CacheModel:
    _cache = cache
    key_prefix = ''

    @classmethod
    def ttl(cls):
        raise NotImplementedError

    @classmethod
    def length(cls):
        raise NotImplementedError

    @classmethod
    def generate_token(cls, length=None):
        length = length if length is not None else cls.length()
        return binascii.hexlify(os.urandom(length)).decode()

    @classmethod
    def get_cache_key(cls, key):
        """key must be str. handle not-str keys by yourself"""
        return '-'.join(['pika', cls.key_prefix, key])

    """
    None values are restricted. If 'get' method returns None - there was no value for this key (or expired)
    """

    @classmethod
    def _set(cls, key, value, timeout=None):
        if value is None:
            # TODO: change exception class
            raise Exception
        return cls._cache.set(cls.get_cache_key(key), value, timeout or cls.ttl())

    @classmethod
    def _get(cls, key):
        return cls._cache.get(cls.get_cache_key(key))

    @classmethod
    def _delete(cls, key):
        cls._cache.delete(cls.get_cache_key(key))


class ScrapperAccessToken(CacheModel):
    key_prefix = 'scrapper'

    @classmethod
    def ttl(cls):
        # TODO: move to django.settings
        return 900

    @classmethod
    def length(cls):
        # TODO: move to django.settings
        return 20

    @classmethod
    def get_or_create(cls, scrapper_account_id, update_ttl=True):
        created = False

        account_key = cls.get_cache_key(str(scrapper_account_id))
        token = cls._get(account_key)

        if token is None:
            created, token = True, cls.generate_token()

        if created or update_ttl:
            token_key = cls.get_cache_key(token)
            # tokens -> account_id
            cls._set(token_key, scrapper_account_id)
            # account_id -> tokens
            cls._set(account_key, token)

        return token, created

    @classmethod
    def get_account_id(cls, token):
        return cls._get(cls.get_cache_key(token))

    @classmethod
    def remove(cls, token):
        token_key = cls.get_cache_key(token)
        scrapper_account_id = cls._get(token_key)

        cls._delete(token)
        cls._delete(str(scrapper_account_id))
