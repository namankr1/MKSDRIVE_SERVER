from django.shortcuts import render
import json
from django.contrib.auth import logout
from django.http import JsonResponse
from . import services
# Create your views here.

def checkversion(request):
    if request.method=='POST':
        try:
            return JsonResponse({'status':'ok', 'message': 'version2'})
        except Exception:
            return JsonResponse({'status':'err', 'message': 'Data given to server is invalid'})
    else:
        return JsonResponse({'status':'err', 'message': 'Bad Request'})
        
def signup(request):
    if request.method=='POST':
        result = 0
        try:
            print(request.body)
            jsonin=json.loads(request.body)
            print(jsonin)
            if(jsonin['key'] == "Mksupdatecnkncklsdnclnsdcasdfcsdc"):
                pass
            else:
                return JsonResponse({'status':'err', 'message': 'Invalid access.'})
            result = services.userSignup(jsonin['firstName'],jsonin['lastName'],jsonin['phone'],jsonin['password'],jsonin['email'],jsonin['pan'],jsonin['aadhar'],jsonin['gender'],jsonin['address'],jsonin['state'],jsonin['zipcode'])
        except Exception:
            return JsonResponse({'status':'err', 'message': 'Data given to server is invalid'})
        if result == -1:
            return JsonResponse({'status':'err', 'message': 'Email is invalid'})
        elif result == -2:
            return JsonResponse({'status':'err', 'message': 'Name field input contains characters other than space and letters'})
        elif result == -4:
            return JsonResponse({'status':'err', 'message': 'Phone number is invalid'})
        elif result == -5:
            return JsonResponse({'status':'err', 'message': 'Password is too short'})
        elif result == -6:
            return JsonResponse({'status':'err', 'message': 'Password is too short'})
        elif result == -7:
            return JsonResponse({'status':'err', 'message': 'User already registered'})
        elif result == -8:
            return JsonResponse({'status':'err', 'message': 'Server encountered problem in registration'})
        elif result == -9:
            return JsonResponse({'status':'err', 'message': 'Some error occurred in sending mail. Please retry'})
        elif result==1:
            return JsonResponse({'status':'ok', 'message': 'User is successfully registered'})
        else:
            return JsonResponse({'status':'err', 'message': 'Server encountered problem'})
    else:
        return JsonResponse({'status':'err', 'message': 'Bad Request'})
        
def signin(request):
    if request.method=='POST':
        result = 0
        try:
            jsonin=json.loads(request.body)
            result = services.userSignin(jsonin['email'],jsonin['password'],request);
        except Exception:
            return JsonResponse({'status':'err', 'message': 'Data given to server is invalid'})
        if result == -1:
            return JsonResponse({'status':'err', 'message': 'Email is invalid'})
        elif result == -2:
            return JsonResponse({'status':'err', 'message': 'Password is too short'})
        elif result == -3:
            return JsonResponse({'status':'err', 'message': 'User is not registered'})
        elif result == -4:
            return JsonResponse({'status':'err', 'message': 'User account is disabled'})
        elif result == -5:
            return JsonResponse({'status':'err', 'message': 'Password is incorrect'})
        else:
            return JsonResponse({'status':'ok', 'profile': result})
    else:
        return JsonResponse({'status':'err', 'message': 'Bad Request'})

def verifyOTP(request):
    if request.method=='POST':
        result = 0
        try:
            jsonin=json.loads(request.body)
            result = services.verifyOTP(jsonin['email'],jsonin['otp'])
        except Exception:
            return JsonResponse({'status':'err', 'message': 'Data given to server is invalid'})
        if result == -1:
            return JsonResponse({'status':'err', 'message': 'Email is invalid'})
        elif result == -2:
            return JsonResponse({'status':'err', 'message': 'OTP is invalid'})
        elif result == -3:
            return JsonResponse({'status':'err', 'message': 'User is not registered'})
        elif result == -4:
            return JsonResponse({'status':'err', 'message': 'There is no OTP to verify for this email'})
        elif result == -5:
            return JsonResponse({'status':'err', 'message': 'OTP is incorrect'})
        elif result == 1:
            return JsonResponse({'status':'ok', 'message': 'OTP verified successfully'})
        else:
            return JsonResponse({'status':'err', 'message': 'Server encountered problem'})
    else:
        return JsonResponse({'status':'err', 'message': 'Bad Request'})

def signout(request):
    logout(request)
    return JsonResponse({'status':'ok','message':'Signed out successfully'})

def sendOTP(request):
    if request.method == 'POST':
        result=0
        try:
            jsonin = json.loads(request.body)
            result = services.sendOTP(jsonin['email'])
        except Exception:
            return JsonResponse({'status':'err', 'message': 'Data given to server is invalid'})
        if result==1:
            return JsonResponse({'status':'ok', 'message': 'OTP sent'})
        elif result == -8:
            return JsonResponse({'status':'err', 'message': 'User is not registered'})
        elif result == -9:
            return JsonResponse({'status':'err', 'message': 'Some error occurred in sending mail. Please retry'})
        else:
            return JsonResponse({'status':'err', 'message': 'Server encountered problem'})
    else:
        return JsonResponse({'status':'err', 'message': 'Bad Request'})

def changepassword(request):
    if request.method == 'POST':
        result=0
        try:
            jsonin = json.loads(request.body)
            result = services.changePassword(jsonin['email'],jsonin['oldpassword'],jsonin['newpassword'])
        except Exception:
            return JsonResponse({'status':'err', 'message': 'Data given to server is invalid'})
        if result == -1:
            return JsonResponse({'status':'err', 'message': 'Email is invalid'})
        elif result == -2:
            return JsonResponse({'status':'err', 'message': 'User is not registered'})
        elif result == -3:
            return JsonResponse({'status':'err', 'message': 'Current password is incorrect'})
        elif result == -4:
            return JsonResponse({'status':'err', 'message': 'New password is too short'})
        elif result == 1:
            return JsonResponse({'status':'ok', 'message': 'Successfully changed password'})
        else:
            return JsonResponse({'status':'err', 'message': 'Server encountered problem'})
    else:
        return JsonResponse({'status':'err', 'message': 'Bad Request'})

def forgotpassword(request):
    if request.method == 'POST':
        result = 0
        try:
            jsonin = json.loads(request.body)
            result = services.forgotPassword(jsonin['email'],jsonin['otp'],jsonin['newpassword'])
        except Exception:
            return JsonResponse({'status':'err', 'message': 'Data given to server is invalid'})
        if result == -1:
            return JsonResponse({'status':'err', 'message': 'Email is invalid'})
        elif result == -2:
            return JsonResponse({'status':'err', 'message': 'OTP is invalid'})
        elif result == -3:
            return JsonResponse({'status':'err', 'message': 'User is not registered'})
        elif result == -4:
            return JsonResponse({'status':'err', 'message': 'There is no OTP to verify for this email'})
        elif result == -5:
            return JsonResponse({'status':'err', 'message': 'OTP is incorrect'})
        elif result == 1:
            return JsonResponse({'status':'ok', 'message': 'Successfully changed password'})
        else:
            return JsonResponse({'status':'err', 'message': 'Server encountered problem'})
    else:
        return JsonResponse({'status':'err', 'message': 'Bad Request'})

def updatefolderid(request):
    if request.method == 'POST':
        result=0
        try:
            jsonin = json.loads(request.body)
            if(jsonin['key'] == "Mksupdatecnkncklsdnclnsdcasdfcsdc"):
                pass
            else:
                return JsonResponse({'status':'err', 'message': 'Invalid access.'})
            result = services.updateFolderID(jsonin['email'],jsonin['newfolderid'])
        except Exception:
            return JsonResponse({'status':'err', 'message': 'Data given to server is invalid'})
        if result == -1:
            return JsonResponse({'status':'err', 'message': 'Email is invalid'})
        elif result == -2:
            return JsonResponse({'status':'err', 'message': 'User is not registered'})
        elif result == 1:
            return JsonResponse({'status':'ok', 'message': 'Successfully updated folderId'})
        else:
            return JsonResponse({'status':'err', 'message': 'Server encountered problem'})
    else:
        return JsonResponse({'status':'err', 'message': 'Bad Request'})
        
def getprofile(request):
    if request.method=='POST':
        result = 0
        try:
            jsonin=json.loads(request.body)
            result = services.getprofile(jsonin['email'],jsonin['secureKey']);
        except Exception:
            return JsonResponse({'status':'err', 'message': 'Data given to server is invalid'})
        if result == -1:
            return JsonResponse({'status':'err', 'message': 'Email is invalid'})
        elif result == -2:
            return JsonResponse({'status':'err', 'message': 'Invalid session, please login again'})
        elif result == -3:
            return JsonResponse({'status':'err', 'message': 'User is not registered'})
        else:
            return JsonResponse({'status':'ok', 'profile': result})
    else:
        return JsonResponse({'status':'err', 'message': 'Bad Request'})