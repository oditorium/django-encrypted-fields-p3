# django-encrypted-fields-p3
_like django-encrypted-fields, but for Python 3_

## Manual Installation

After installing the Heroku [Toolbelt](https://toolbelt.heroku.com/) run the following commands:

    git clone https://github.com/oditorium/django-encrypted-fields-p3.git
    cd django-encrypted-fields-p3
    heroku create
    heroku config:set HEROKU=1
    git push heroku +master

### Setup

Once the installation is finished, create a superuser by doing

    heroko run ./manage.py createsuperuser


### Installation Button

You can directly deploy this repo in Heroku by clicking the button below
(you will have to create a free account)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Provided you have set up your heroku toolchain you can create a superuser by doing

    heroko run ./manage.py createsuperuser --app <appname> 
    
*NOTE*: you will currently have to add `HEROKU=1` manually to the Heroku environment
variables. 

## Usage

### encryptedfields

The relevant code is contained in `lib/encryptedfields` (and there mainly in `crypter.py` 
and `encryptedfields`). In order to use this library, first add `lib/encryptedfields` 
to your project (as `lib/encryptedfields`!), but do _not_ register it as an app.

If you want to use encrypted fields in a model, include code akin to the following code
into your model

    # models.py
    from django.db import models
    from lib.encryptedfields import * 
    
    class MyModel(models.Model):
    
        textfield  = EncryptedTextField(unique=False, blank=True, null=True, default=None)
        charfield  = EncryptedCharField(max_length=100, blank=True, null=True, default=None)
        emailfield = EncryptedEmailField(blank=True, null=True, default=None)
        ...
        

In your settings file add

    # settings.py
    ENCRYPTED_FIELDS_SECRET_KEY = "secret key string with at least 32 bytes of entropy"

or, better

    # settings.py
    import os
    ENCRYPTED_FIELDS_SECRET_KEY = os.getenv('ENCRYPTED_FIELDS_SECRET_KEY')
    
The fields `encrtextfield`, `encrcharfield`, and `encremailfield` will then be transparently encrypted 
with the static key from `settings.ENCRYPTED_FIELDS_SECRET_KEY`

### crypter

You can also use `Crypter` on a standalone basis. The API is very similar to the one of KeyCzar,
with the exception that the original format is preserved (ie, strings remain strings, and bytes remain
bytes)

	from crypter import Crypter
	secret_key = "secret key string with at least 32 bytes of entropy"
	...
	cr = Crypter(secret_key)
	ciphert = cr.Encrypt("123")
	ciphert2 = cr.Encrypt(b"123")
	...
	cr = Crypter(secret_key)
	cr.Decrypt(ciphert) # "123"
	cr.Decrypt(ciphert2) # b"123"


## Credit, Contributions, and License

Credit goes to the developers of [Keyczar](https://github.com/google/keyczar) 
for the original encryption code, and to [Aron Jones](https://github.com/defrex) who wrote the original [django-encrypted-fields](https://github.com/defrex/django-encrypted-fields). I hope they
at some point get around moving their libraries to Python 3, because their code
is so much more comprehensive than mine!

Contributions welcome. Send us a pull request! The code is licensed under MPL 2.0 (see the LICENSE file).


## Change Log

The code uses [semantic versioning](http://semver.org/) (hence the high version number as I changed
the format a number of times; it does not mean that the code is particularly robust!)

- **crypter v2.1**, **encryptedfields v2.1** initial check-in



[djslack]: https://github.com/oditorium/django-slack/commit/7872d385e7b7243365ecf1429c2b86a0ac7d4ece