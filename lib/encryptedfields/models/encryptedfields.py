from django.db import models
from ..encryptedfields import *

class EncryptionTestModelBase(models.Model):
    """
    a model to test the above mixin
    
    USAGE
    
    In an app's `models.py` include
    
        from lib.encryptedfields.models import EncryptionTestModelBase
        
        class EncryptionTestModel (EncryptionTestModelBase):
            pass
    """
    class Meta:
        abstract = True
    
    plaintextfield = models.TextField(unique=False, blank=True, null=True, default=None)
    encrtextfield = EncryptedTextField(unique=False, blank=True, null=True, default=None)
    
    plaincharfield = models.CharField(max_length=100, blank=True, null=True, default=None)
    encrcharfield = EncryptedCharField(max_length=100, blank=True, null=True, default=None)
    
    plainemailfield = models.EmailField(blank=True, null=True, default=None)
    encremailfield = EncryptedEmailField(blank=True, null=True, default=None)
