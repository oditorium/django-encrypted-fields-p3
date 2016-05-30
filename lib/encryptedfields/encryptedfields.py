"""
allowing encrypted text fields in Django

NOTE
- fields defined are `EncryptedTextField`, EncryptedCharField, EncryptedEmailField
- it requires ENCRYPTED_FIELDS_SECRET_KEY to be set in settings

COPYRIGHT

Copyright (c) Stefan LOESCH, oditorium 2016. All rights reserved.
Licensed under the Mozilla Public License, v. 2.0 <https://mozilla.org/MPL/2.0/>

ORIGINAL SOURCE

- Copyright (c) 2013 Aron Jones
    https://github.com/defrex/django-encrypted-fields/blob/master/encrypted_fields/fields.py
- Licensed under the MIT License
    https://github.com/defrex/django-encrypted-fields/blob/master/LICENCE.txt
- Retrieved 30 May 2016, commit 680f1cb39


REFERENCES
https://docs.djangoproject.com/en/1.9/howto/custom-model-fields/
http://stackoverflow.com/questions/29551367/is-there-a-django-1-7-replacement-for-souths-add-introspection-rules

"""
__version__ = "2.1"
__version_dt__ = "2015-05-30"
import os
import types

import django
from django.db import models
from django.conf import settings
from .crypter import *


#########################################################
## HELPERS
    
# CRYPTO WRAPPER
class _CryptoWrapper(object):
    """
    Simple wrapper to standardize initialization of crypter object and allow for others to extend as needed
    
    - `secret_key` should be a sufficient-entropy string 
	- if secret_key is None, ENCRYPTED_FIELDS_SECRET_KEY must be defined in settings
    """
    def __init__(self, secret_key=None, *args, **kwargs):
        if secret_key == None: 
            secret_key = settings.ENCRYPTED_FIELDS_SECRET_KEY
        self._crypter = Crypter(secret_key)

    encrypt = lambda self, cleartext:  self._crypter.Encrypt(cleartext)
    decrypt = lambda self, ciphertext: self._crypter.Decrypt(ciphertext)



#################################################################################################
## ENCRYPTED FIELD MIXIN
class EncryptedFieldException(Exception): pass

class EncryptedFieldMixin(object):
    """
    encrypt/decrypt data that is being marshalled in/out of the database into application Django model fields
    """

    enforce_max_length = True
    prefix = b""                    # that parameter is not currently supported; keep b""
    decrypt_only = False            # that flag is not currently supported; keep False

    def __init__(self, secret_key=None, *args, **kwargs):
        #print ("__init__: {}".format(secret_key))
        self._crypter = _CryptoWrapper(secret_key)
        super(EncryptedFieldMixin, self).__init__(*args, **kwargs)

    crypter = lambda self: self._crypter
    get_internal_type = lambda self: 'TextField' # why not BinaryField???

    def deconstruct(self):
        name, path, args, kwargs = super(EncryptedFieldMixin, self).deconstruct()
        #if self.secret_key != Crypter.default_secret_key(): kwargs['secret_key'] = self.secret_key
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, context):
        #print ("from_db_value: {}".format(value))
        return self.to_python(value)

    def to_python(self, value):
        #print ("to_python: {}".format(value))
        #if value is None or not isinstance(value, types.StringTypes): return value
        if value is None: return value
        try: value = self.crypter().decrypt(value)
        except CrypterError: pass
        if isinstance(value, bytes): value = value.decode()
        return super(EncryptedFieldMixin, self).to_python(value)

    def get_prep_value(self, value):
        print ("get_prep_value: {}".format(value))
        value = super(EncryptedFieldMixin, self).get_prep_value(value)
        if value is None or value == '': return value
        # if isinstance(value, str): value = value.encode()
        # else: value = str(value)
        #return self.prefix + self.crypter().encrypt(value)
        value = value.encode()
        #print ("unencrypted: {}".format(value))
        value = self.crypter().encrypt(value)
        #print ("encrypted: {}".format(value))
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        #print ("get_db_prep_value: {}".format(value))
        if not prepared:
            value = self.get_prep_value(value)
            if self.enforce_max_length:
                if value and hasattr(self, 'max_length') and self.max_length and len(value) > self.max_length:
                    raise ValueError( 'Field {0} max_length={1} encrypted_len={2}'.format(self.name,self.max_length,len(value)) )
        return value

#################################################################################################
## FIELDS

# ENCRYPTED TEXT FIELD
class EncryptedTextField(EncryptedFieldMixin, models.TextField): pass

# ENCRYPTED CHAR FIELD
class EncryptedCharField(EncryptedFieldMixin, models.CharField): pass

# ENCRYPTED EMAIL FIELD
class EncryptedEmailField(EncryptedFieldMixin, models.EmailField): pass


# class EncryptedDateTimeField(EncryptedFieldMixin, models.DateTimeField): pass
# class EncryptedDateField(EncryptedFieldMixin, models.DateField): pass
# class EncryptedIntegerField(EncryptedFieldMixin, models.IntegerField): pass
# class EncryptedFloatField(EncryptedFieldMixin, models.FloatField): pass
# class EncryptedBooleanField(EncryptedFieldMixin, models.BooleanField): pass

    
    
    
