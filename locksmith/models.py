from django.db import models
from django.db.models import ObjectDoesNotExist
import datetime
import functools


class K(object):

    AND = "and"
    OR = "or"

    def __init__(self, key_name):
        self._key_name = key_name
        self._bitwise_condition = self.AND
        self._others = []

    def set_condition(self, condition):
        self._bitwise_condition = condition

    @property
    def key_name(self):
        return self._key_name

    @property
    def condition(self):
        return self._bitwise_condition

    def __or__(self, other):

        other.set_condition(self.OR)
        self._others.append(other)

        return self

    def __and__(self, other):

        other.set_condition(self.AND)
        self._others.append(other)

        return self

    def __str__(self):

        return "K(%s, %s, %s)" % (self.condition, self.key_name,
                                  str(self._others))

    def __repr__(self):
        return str(self)

    def check_keychain(self, keychain):

        if len(self._others) == 0:
            return self.key_name in keychain

        def check(bool_value: bool, k):
            nonlocal keychain, self

            if k.condition == self.OR:
                bool_value = bool_value or k.check_keychain(keychain)
            else:
                bool_value = bool_value and k.check_keychain(keychain)

            return bool_value

        val = functools.reduce(check, self._others, self.key_name in keychain)
        return bool(val)


class Key(models.Model):

    name = models.CharField(max_length=255)

    def __or__(self, other):
        pass

    def __and__(self, other):
        pass


class KeyChain(models.Model):

    keys = models.ManyToManyField(Key, blank=True)
    expiration_date = models.DateField(verbose_name="Expiration date")


    def __init__(self, *args, **kwargs):
        super(KeyChain, self).__init__(*args, **kwargs)
        self._cache = {}

    def is_expired(self):
        return datetime.datetime.now().date() >= self.expiration_date

    def __contains__(self, key_name):

        if type(key_name) is K:
            key_name = key_name.key_name

        if len(self._cache) == 0:
            def set_cache(name, value):
                nonlocal self
                self._cache[name] = value

            [set_cache(key.name, key) for key in self.keys.all()]

        if key_name in self._cache:
            return True
        else:
            return False


class LocksmithMixin(models.Model):

    keychain = models.ForeignKey(KeyChain, blank=True, null=True)

    class Meta:
        abstract = True