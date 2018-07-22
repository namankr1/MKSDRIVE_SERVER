from . import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail, EmailMessage
import random
import json,urllib
import re
import threading
import string
import random
from drive import services

def sendOTP(email):
    email = email.lower()
    u=User.objects.filter(username=email)
    if len(u)==0:
        return -8
    profileobj=models.Profile.objects.filter(user=u[0])
    models.OTPRecord.objects.filter(profile=profileobj[0]).delete()
    token = random.randrange(100000, 1000000, 1)
    #token=112233
    otp = models.OTPRecord(otp=token,profile=profileobj[0]);
    otp.save()
    thread = threading.Thread(target=send_mail, args=[email, token])
    thread.daemon = True                            # Daemonize thread
    thread.start()
    return 1
    
def send_mail(email, token):
    email = email.lower()
    try:
        return services.send_mail(email, "One Time Password (OTP) for your MKSDrive account", "Hi,\nUse " + str(token) +" as One Time Password (OTP) to log in to your MKSDrive account. Please do not share this OTP with anyone for security reasons.")
    except Exception as e:
        print(e)
        return -9

def userSignup(firstName,lastName,phone,password,email,pan,aadhar,gender,address,state,zipcode):
    #email checking
    email = email.lower()
    if re.compile('[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]+').match(email):
        pass
    else:
        return -1
    if all(x.isalpha() or x.isspace() for x in firstName):
        pass
    else:
        return -2
    if all(x.isalpha() or x.isspace() for x in lastName):
        pass
    else:
        return -2
    if (not phone.isdigit()) or len(phone)!=10:
        return -4
    if len(password)<8:
        return -5
    if len(gender) > 1:
        if gender.lower() == "male":
            gender = "M"
        elif gender.lower() == "female":
            gender = "F"
        else:
            gender = "O"
    u=User.objects.filter(username=email)
    if len(u)>0:
        return -7
    user = User.objects.create_user(username = email, password = password,first_name=firstName,last_name=lastName,is_active=False)
    user.save()
    profileobj = models.Profile(user=user,phone=phone,email=email,pan=pan,aadhar=aadhar,gender=gender,address=address,state=state,zipcode=zipcode)
    profileobj.save();
    #sendOTP(email)
    return 1

def userSignin(email, password, request):
    email = email.lower()
    if re.compile('[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]+').match(email):
        pass
    else:
        return -1
    if len(password)<8:
        return -2
    u=User.objects.filter(username=email)
    if len(u)==0:
        return -3
    if u[0].check_password(password):
        if u[0].is_active:
            secure_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
            login(request,u[0])
            models.Profile.objects.filter(user=u[0]).update(secureKey=secure_key)
            profileobj=models.Profile.objects.filter(user=u[0])
            jsonout={}
            jsonout['name']=profileobj[0].user.get_full_name()
            jsonout['phone']=profileobj[0].phone
            jsonout['email']=profileobj[0].email
            jsonout['pan']=profileobj[0].pan
            jsonout['aadhar']=profileobj[0].aadhar
            jsonout['gender']=profileobj[0].gender
            jsonout['address']=profileobj[0].address
            jsonout['state']=profileobj[0].state
            jsonout['zipcode']=profileobj[0].zipcode
            jsonout['folderID']=profileobj[0].folderID
            jsonout['secureKey']=profileobj[0].secureKey
            return jsonout
        else:
            return -4
    else:
        return -5

def verifyOTP(email,token):
    email = email.lower()
    if re.compile('[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]+').match(email):
        pass
    else:
        return -1
    if len(token)!=6:
        return -2
    u=User.objects.filter(username=email)
    if len(u)==0:
        return -3
    profileobj=models.Profile.objects.filter(user=u[0])
    otpobj = models.OTPRecord.objects.filter(profile=profileobj[0])
    if len(otpobj)==0:
        return -4
    else:
        if otpobj[0].otp==token:
            otpobj[0].delete()
            u[0].is_active=True
            u[0].save()
            return 1
        else:
            return -5

def changePassword(email,oldpassword,newpassword):
    email = email.lower()
    if re.compile('[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]+').match(email):
        pass
    else:
        return -1
    u=User.objects.filter(username=email)
    if len(u)==0:
        return -2
    if len(newpassword)<8:
        return -4
    profileobj=models.Profile.objects.filter(user=u[0])
    if(u[0].check_password(oldpassword)):
        u[0].set_password(newpassword)
        u[0].is_active=True
        u[0].save()
        return 1
    else:
        return -3

def forgotPassword(email,otp,newpassword):
    email = email.lower()
    resultotp = verifyOTP(email,otp)
    if resultotp == 1:
        u=User.objects.filter(username=email)
        if len(u)==0:
            return -3
        profileobj=models.Profile.objects.filter(user=u[0])
        u[0].set_password(newpassword)
        u[0].save()
        return 1
    else:
        return resultotp
        
def updateFolderID(email, newFolderID):
    email = email.lower()
    if re.compile('[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]+').match(email):
        pass
    else:
        return -1
    u=User.objects.filter(username=email)
    if len(u)==0:
        return -2
    models.Profile.objects.filter(user=u[0]).update(folderID=newFolderID)
    return 1

def getprofile(email, secure_key):
    email = email.lower()
    if re.compile('[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]+').match(email):
        pass
    else:
        return -1
    u=User.objects.filter(username=email)
    if len(u)==0:
        return -3
    profileobj=models.Profile.objects.filter(user=u[0])
    if profileobj[0].secureKey != secure_key:
        return -2
    jsonout={}
    jsonout['name']=profileobj[0].user.get_full_name()
    jsonout['phone']=profileobj[0].phone
    jsonout['email']=profileobj[0].email
    jsonout['pan']=profileobj[0].pan
    jsonout['aadhar']=profileobj[0].aadhar
    jsonout['gender']=profileobj[0].gender
    jsonout['address']=profileobj[0].address
    jsonout['state']=profileobj[0].state
    jsonout['zipcode']=profileobj[0].zipcode
    return jsonout