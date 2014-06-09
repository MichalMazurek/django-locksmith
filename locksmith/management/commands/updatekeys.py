__author__ = 'michal'
from django.core.management.base import CommandError, BaseCommand
from django.conf import settings
from locksmith.models import Key


class Command(BaseCommand):
    can_import_settings = True
    args = ""
    help = "Creates keys from settings"

    def handle(self, *args, **kwargs):

        if hasattr(settings, "LOCKSMITH_KEYS"):
            for key_name in settings.LOCKSMITH_KEYS:
                try:
                    key = Key.objects.get(name=key_name)
                    self.stdout.write("Key exists %s, ignoring" % key_name)
                except Key.DoesNotExist:
                    key = Key(name=key_name)
                    key.save()
                    self.stdout.write("Created key %s" % key_name)
