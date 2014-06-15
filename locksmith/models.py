from django.db import models
from django.db.models import ObjectDoesNotExist
# from django.utils.translation import ugettext_lazy as _
import datetime
# Create your models here.


class Key(models.Model):

    name = models.CharField(max_length=255)


class KeyChain(models.Model):

    keys = models.ManyToManyField(Key, blank=True)
    expiration_date = models.DateField(verbose_name="Expiration date")

    _cache = {}

    def is_expired(self):
        return datetime.datetime.now().date() >= self.expiration_date

    def __contains__(self, key_name):

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