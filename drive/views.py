from django.shortcuts import render
import json
from django.http import JsonResponse
from . import services

def getdata(request):
    if request.method == 'POST':
        result = 0
        try:
            jsonin=json.loads(request.body)
            result = services.get_data(jsonin['email'],jsonin['secureKey'],jsonin['folderID'],jsonin['mimeType'])
        except Exception:
            return JsonResponse({'status':'err','message':'Data given to server is invalid'})
        if result ==-1:
            return JsonResponse({'status' : 'err', 'message' : 'Invalid session, please login again'})
        elif result ==-2:
            return JsonResponse({'status' : 'err', 'message' : 'Invalid request'})
        elif result ==-3:
            return JsonResponse({'status' : 'err', 'message' : 'Some Error Occurred'})
        elif type(result) == list:
            return JsonResponse({'status' : 'okfolder', 'filelist': result})
        elif type(result) == str:
            return JsonResponse({'status' : 'okfile', 'filedata' : result})
        else:
            return JsonResponse({'status' : 'err', 'message' : 'Some Error Occurred'})
    else:
        return JsonResponse({'status':'err','message':'Bad request'})

def sendmail(request):
    if request.method == 'POST':
        result = 0
        try:
            jsonin=json.loads(request.body)
            if(jsonin['secureKey']=="Test67676hggfdc"):
                pass
            else:
                return JsonResponse({'status':'err','message':'Unauthorized access'})
            result = services.send_mail(jsonin['email'],jsonin['subject'],jsonin['message'])
        except Exception:
            return JsonResponse({'status':'err','message':'Data given to server is invalid'})
        if result ==-1:
            return JsonResponse({'status' : 'err', 'message' : 'Invalid session, please login again'})
        else:
            return JsonResponse({'status' : 'ok', 'message' : result})
    else:
        return JsonResponse({'status':'err','message':'Bad request'})
        
# def getaccess(request):
#     if request.method == 'POST':
#         result = 0
#         try:
#             jsonin=json.loads(request.body)
#             result = services.get_credentials_drive(jsonin['email'],jsonin['secureKey'])
#         except Exception:
#             return JsonResponse({'status':'err','message':'Data given to server is invalid'})
#         if result ==-1:
#             return JsonResponse({'status' : 'err', 'message' : 'Invalid session, please login again'})
#         if result ==-2:
#             return JsonResponse({'status' : 'err', 'message' : 'Some Error Occurred'})
#         elif type(result) == str:
#             return JsonResponse({'status' : 'ok', 'access' : result})
#         else:
#             return JsonResponse({'status' : 'err', 'message' : 'Some Error Occurred'})
#     else:
#         return JsonResponse({'status':'err','message':'Bad request'})

def senddata(request):
    if request.method == 'POST':
        result = 0
        try:
            jsonin=json.loads(request.body)
            result = services.send_data(jsonin['email'],jsonin['secureKey'],jsonin['folderID'],jsonin['mimeType'], jsonin['emailReceiver'])
        except Exception:
            return JsonResponse({'status':'err','message':'Data given to server is invalid'})
        if result == -1:
            return JsonResponse({'status' : 'err', 'message' : 'Invalid email'})
        elif result ==-2:
            return JsonResponse({'status' : 'err', 'message' : 'Invalid request'})
        elif result ==-3:
            return JsonResponse({'status' : 'err', 'message' : 'Invalid session, please login again'})
        elif result ==-4:
            return JsonResponse({'status' : 'err', 'message' : 'Some error occurred'})
        elif result ==1:
            return JsonResponse({'status' : 'ok', 'message' : 'We have received your request, You will shortly receive an email'})
        else:
            return JsonResponse({'status':'err', 'message':'Some error occurred'})
    else:
        return JsonResponse({'status':'err','message':'Bad request'})

def test(request):
    if request.method == 'GET':
        result = 0
        try:
            result = services.test()
        except Exception:
            return JsonResponse({'status':'err','message':'Data given to server is invalid'})
        return JsonResponse({'status':'ok', 'message':result})
    else:
        return JsonResponse({'status':'err','message':'Bad request'})
        