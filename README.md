django-locksmith
================

Simple way for restricting access to views

Quick Start
-----------

1. Add 'locksmith' to installed apps in your settings.py:
```python
INSTALLED_APPS = (
    ...
    'locksmith'
)
```
2. Configure your key names in settings.py:
```python
LOCKSMITH_KEYS = (
    'articles',
    'users'
)
```

3. Update your keys (you can do it every time you add a key)
```bash
./manage.py updatekeys
```
4. Update your custom user model, add locksmith mixin:
```python
class User(locksmith.models.LocksmithMixin, models.Model):
...
```
5. Add key to users keychain (currently no admin interface):
```python
from locksmith.models import Keychain, Key
...
user = Users.objects.get(pk=1) # your user
# create keychain for this user
keychain = Keychain(expiration_date="2020-12-31")
keychain.save()
user.keychain = keychain

user.keychain.add(Key.objects.get(name='articles')
```
5. Configure your views
```python
from locksmith.decorators import key_required
...
@key_required('articles')
def action(request, *args, **kwargs):
```

And that's it!
