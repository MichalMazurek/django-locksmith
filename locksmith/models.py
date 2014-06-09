from django.db import models
# from django.utils.translation import ugettext_lazy as _
import datetime
# Create your models here.


class Key(models.Model):

    name = models.CharField(max_length=255)


class KeyChain(models.Model):

    keys = models.ManyToManyField(Key, blank=True)
    expiration_date = models.DateField(name="Expiration Date")

    def is_expired(self):
        return datetime.datetime.now().date() >= self.expiration_date


class LocksmithMixin(models.Model):

    keychain = models.ForeignKey(KeyChain, blank=True, null=True)

    class Meta:
        abstract = True