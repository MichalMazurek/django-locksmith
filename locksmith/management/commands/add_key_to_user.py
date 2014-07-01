__author__ = 'michal'
from django.core.management.base import CommandError, BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
from locksmith.models import Key, LocksmithMixin, KeyChain
import datetime
from optparse import make_option

class Command(BaseCommand):
    can_import_settings = True
    help = "Adds keys to users"
    args = "<key key key ...>"
    option_list = BaseCommand.option_list + (
        make_option("--user-pk", dest="user_pk"),
        make_option("--expiration-date", dest="expiration_date",
                    help="Keychain expiration date, format: YYYY-MM-DD")

    )
    def add_arguments(self, parser):

        parser.add_argument("keys", nargs="+", type=str)

        parser.add_argument('--user-pk',
                            dest="user_pk", type=int,
                            help="Primary key of user")

        parser.add_argument('--expiration-date', dest="expiration_date",
                            help="Keychain expiration date, format: 2014-12-31"
        )

    def handle(self, *args, **kwargs):
        User = get_user_model()
        """:type: LocksmithMixin """

        try:
            user = User.objects.get(pk=kwargs["user_pk"])
            """:type: LocksmithMixin """
        except User.DoesNotExist:
            self.stderr.write("User with pk %s does not exist"
                              % kwargs['user_pk'])

            return ""

        if user.keychain is None:
            keychain = KeyChain()
            keychain.expiration_date = datetime.datetime.strptime(
                kwargs["expiration_date"], "%Y-%m-%d").date()
            keychain.save()
            user.keychain = keychain
            user.save()

        keychain = user.keychain
        """:type: KeyChain"""

        for key_name in args:
            try:
                key = Key.objects.get(name=key_name)
                keychain.keys.add(key)
                self.stdout.write("Adding key '%s' to '%s'" %
                                  (key_name, user.get_full_name()))
            except Key.DoesNotExist:
                self.stderr("Key '%s' does not exist" % key_name)

        keychain.save()
