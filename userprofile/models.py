from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10,null=True,default="0000000000", blank=True)
    email = models.EmailField(max_length=254)
    pan = models.CharField(max_length=10,null=True,default="AAAAA0000A", blank=True)
    aadhar = models.CharField(max_length=16,null=True,default="0000000000000000", blank=True)
    gender = models.CharField(max_length=1,null=True,default="O", blank=True)
    address = models.CharField(max_length=100,null=True,default="XX", blank=True)
    state = models.CharField(max_length=100,null=True,default="XX", blank=True)
    zipcode = models.CharField(max_length=6,null=True,default="000000", blank=True)
    folderID = models.CharField(max_length=150,null=True,default="", blank=True)
    secureKey = models.CharField(max_length=32,null=True,default="", blank=True)

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email
    
class OTPRecord(models.Model):
    otp = models.CharField(max_length=6)
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.profile.email

    def __unicode__(self):
        return self.profile.email
