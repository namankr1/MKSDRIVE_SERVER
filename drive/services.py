from httplib2 import Http
import os
import io
import threading
import json
import re
import base64
import mimetypes
from apiclient.discovery import build
from oauth2client import client, tools, file
from oauth2client.file import Storage
from apiclient import errors
from apiclient import http
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from . import models
from userprofile import models as usermodels
from django.conf import settings
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import email.encoders

mimetypes.init()
mimetypes.add_type('application/vnd.google-apps.audio', '.mp3')
mimetypes.add_type('application/vnd.google-apps.document', '.doc')

list_google_mimeType = [
    ["application/vnd.google-apps.audio",".mp3","text/plain"],
    ["application/vnd.google-apps.document",".doc","application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
    ["application/vnd.google-apps.drawing",".jpeg","image/jpeg"],
    ["application/vnd.google-apps.file",".txt","text/plain"],
    ["application/vnd.google-apps.form",".xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
    ["application/vnd.google-apps.fusiontable",".xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
    ["application/vnd.google-apps.map",".jpeg","image/jpeg"],
    ["application/vnd.google-apps.photo",".jpeg","image/jpeg"],
    ["application/vnd.google-apps.presentation",".pptx","application/vnd.openxmlformats-officedocument.presentationml.presentation"],
    ["application/vnd.google-apps.script",".txt","text/plain"],
    ["application/vnd.google-apps.site",".txt","text/plain"],
    ["application/vnd.google-apps.spreadsheet",".xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
    ["application/vnd.google-apps.unknown",".txt","text/plain"],
    ["application/vnd.google-apps.video",".mp4","text/plain"],
    ["application/vnd.google-apps.drive-sdk",".txt","text/plain"]
    ]
    
array_google_mimeType = [
    "application/vnd.google-apps.audio",
    "application/vnd.google-apps.document",
    "application/vnd.google-apps.drawing",
    "application/vnd.google-apps.file",
    "application/vnd.google-apps.form",
    "application/vnd.google-apps.fusiontable",
    "application/vnd.google-apps.map",
    "application/vnd.google-apps.photo",
    "application/vnd.google-apps.presentation",
    "application/vnd.google-apps.script",
    "application/vnd.google-apps.site",
    "application/vnd.google-apps.spreadsheet",
    "application/vnd.google-apps.unknown",
    "application/vnd.google-apps.video",
    "application/vnd.google-apps.drive-sdk",
    ]

for mime in list_google_mimeType:
    mimetypes.add_type(mime[0],mime[1])

SCOPES_DRIVE = 'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET_FILE_DRIVE = 'client_secret_drive.json'
APPLICATION_NAME = 'MKSDrive'

SCOPES_GMAIL = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE_GMAIL = 'client_secret_gmail.json'

def get_credentials_gmail():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_dir = settings.CREDENTIALS_DIR
    credential_path = os.path.join(credential_dir,'MKSDriveGmailCred.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        CLIENT_SECRET_FILE_GMAIL1 = os.path.join(settings.PROJECT_ROOT,CLIENT_SECRET_FILE_GMAIL)
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE_GMAIL1, SCOPES_GMAIL)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags=tools.argparser.parse_args(args=['--noauth_local_webserver']))
        print('Storing credentials to ' + credential_path)
    return credentials

def send_mail(email, subject, message):
    email = email.lower()
    try:
        message_data = CreateMessage(email,subject,message)
        return SendMessage("me", message_data)
    except Exception as e:
        print("Error in sending mail")
        print(e)
        return -1

def SendMessage(user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    credentials = get_credentials_gmail()
    service = build('gmail', 'v1', http=credentials.authorize(Http()))
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    #print ("Message Id:" + str(message['id']))
    return message
  except errors.HttpError as error:
    print ("An error occurred:" + str(error))
    return -1


def CreateMessage(to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """

  message_text = str(message_text) + "\nFor any other query please contact the undersigned.\n\n\nCheers,\nC.A. Manoj Sangal & Co.\n​D-4 Sector 61 Noida-201301\nPh.:0120-4214251; 9810502399\nEmail:-manojksangal@yahoo.com"
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = "Manoj Sangal<mksclients@gmail.com>"
  message['subject'] = subject
  #print(message)
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def CreateMessageWithAttachment(to, subject, message_text, file_dir,
                                filename):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file_dir: The directory containing the file to be attached.
    filename: The name of the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message_text = str(message_text) + "\nFor any other query please contact the undersigned.\n\n\nCheers,\nC.A. Manoj Sangal & Co.\n​D-4 Sector 61 Noida-201301\nPh.:0120-4214251; 9810502399\nEmail:-manojksangal@yahoo.com"
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = "Manoj Sangal<mksclients@gmail.com>"
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  #path = os.path.join(file_dir, filename)
  path = file_dir
  content_type, encoding = mimetypes.guess_type(path)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)

  if main_type == 'text':
    fp = open(path, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(path, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(path, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'application':
    fp = open(path, 'rb')
    msg = MIMEApplication(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(path, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    email.encoders.encode_base64(msg)
    fp.close()

  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def get_credentials_drive():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_dir = settings.CREDENTIALS_DIR
    credential_path = os.path.join(credential_dir,'MKSDriveCred.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        CLIENT_SECRET_FILE_DRIVE1 = os.path.join(settings.PROJECT_ROOT,CLIENT_SECRET_FILE_DRIVE)
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE_DRIVE1, SCOPES_DRIVE)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags=tools.argparser.parse_args(args=['--noauth_local_webserver']))
        print('Storing credentials to ' + credential_path)
    return credentials

def check_access(email,secure_key):
    email = email.lower()
    u=User.objects.filter(username=email)
    if len(u)==0:
        return -1
    profileobj=usermodels.Profile.objects.filter(user=u[0],secureKey=secure_key)
    if len(profileobj)==0:
        return -1
    else:
        return 1
    return -1
    
def get_data(email,secure_key,id,mimeType):
    email = email.lower()
    if check_access(email,secure_key)!=1 :
        return -1
    if id == "":
        return -2
    credentials = get_credentials_drive()
    service = build('drive', 'v3', http=credentials.authorize(Http()))
    if mimeType == "application/vnd.google-apps.folder":
        id = "\'"+id+"\'"
        return drive_list(service,id)
    else:
        return download_file_and_send_encoded(service,id)

def get_file_name_with_extension(file_name, mime_type):
    file_name = str(file_name)
    mime_type = str(mime_type)
    extension_list = mimetypes.guess_all_extensions(mime_type, strict=False)
    extension_filename_list = file_name.split(".")
    if len(extension_filename_list) > 1:
        extension_filename = "." + extension_filename_list[-1].lower()
    else:
        extension_filename=""
    if (extension_filename not in extension_list) and len(extension_list)>0:
        extension_list.sort()
        extension = extension_list[0]
        if extension is not None:
            file_name = file_name + extension

    return file_name
    
def get_google_mimeType(mime_type):
    mime_type = str(mime_type)
    if mime_type not in array_google_mimeType:
        return mime_type
    for mime in list_google_mimeType:
        if mime[0] == mime_type:
            return mime[2]
    return mime_type
    

def drive_list(service,parent_id):
    result = []
    page_token = None
    while True:
        try:
            param = {}
            param['orderBy'] = 'folder,name'
            param['pageSize'] = 500
            param['q'] = parent_id + " in parents and trashed = false"
            param['fields'] = "nextPageToken, files(id,name,mimeType,size)"
            if page_token:
                param['pageToken'] = page_token
            files = service.files().list(**param).execute()
            for file in files['files']:
                file["name"] = get_file_name_with_extension(file["name"], file["mimeType"])
                file["mimeType"] = get_google_mimeType(file["mimeType"])
                result.append(file)
            page_token = files.get('nextPageToken')
            if not page_token:
                break
        except Exception as e:
            print (e)
            return -3
    return result

def get_file_info(service, file_id):
    try:
        param = {}
        param['fileId'] = file_id
        param['fields'] = "id, name, mimeType, size, createdTime, modifiedTime"
        file_info = service.files().get(**param).execute()
        file_info["name"] = get_file_name_with_extension(file_info["name"],file_info["mimeType"])
    except Exception as e:
        print (e)
        return -1
    return file_info
    
def downoad_file_and_store(service, file_id):
    try:
        file_info = get_file_info(service, file_id)
        if(file_info == -1):
            return -1, -1
        download_dir = os.path.join(settings.TEMP_DOWNLOAD_PATH, file_id)
        path_download = os.path.join(download_dir,str(file_info["name"]))
        path_fileinfo = os.path.join(download_dir, "fileinfo")
        
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        else:
            try:
                if os.path.exists(path_fileinfo):
                    json_data = json.load(open(path_fileinfo))
                    if "modifiedTime" in json_data:
                        modified_time = json_data["modifiedTime"]
                    else:
                        modified_time = ""
                    if "createdTime" in json_data:
                        created_time = json_data["createdTime"]
                    else:
                        created_time = ""
                    if(created_time == file_info["createdTime"]  and modified_time == file_info["modifiedTime"] and os.path.exists(path_download) and os.path.getsize(path_download) == long(file_info["size"])):
                        return str(path_download), str(file_info["name"])
                    else:
                        pass
                else: 
                    pass
            except:
                pass
        if file_info["mimeType"] in array_google_mimeType:
            mimeTypeExport=""
            for mime in list_google_mimeType:
                if mime[0] == file_info["mimeType"]:
                    mimeTypeExport = mime[2]
                    break
            request = service.files().export_media(fileId=file_id, mimeType=mimeTypeExport)
        else:
            request = service.files().get_media(fileId=file_id)
        fh = open(path_download, 'wb')
        downloader = http.MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Downloaded "+str(file_info["name"])+" "+str(int(status.progress() * 100))+ "%")
        fh.close()
        json.dump(file_info, open(path_fileinfo, 'w+'))
        return str(path_download), str(file_info["name"])
    except Exception as e:
        print (e)
        return -1, -1

def download_file_and_send_encoded(service,file_id):
    try:
        path_download, _ = downoad_file_and_store(service, file_id)
        if type(path_download) == str and path_download != "":
            file = open(path_download, 'rb')
            file_data = file.read()
            encoded_data = base64.encodestring(file_data)
            # decoded_data = base64.decodestring(encoded_data)
            # file_data2= open(path_upload, 'wb')
            # file_data2.write(decoded_data)
            return encoded_data.decode('utf-8')
        else:
            return -3
    except Exception as e:
        print (e)
        return -3

# def download_file_and_send_path(service,file_id):
#     try:
#         path_download, _ = downoad_file_and_store(service, file_id)
#         if type(path_download) == str and path_download != "":
#             return path_download
#         else:
#             return -3
#     except Exception as e:
#         print (e)
#         return -3

def send_data(email,secure_key,id,mimeType, emailReceiver):
    email = email.lower()
    if re.compile('[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]+').match(emailReceiver):
        pass
    else:
        return -1
    if id == "":
        return -2
    if check_access(email,secure_key)!=1 :
        return -3
    credentials = get_credentials_drive()
    service = build('drive', 'v3', http=credentials.authorize(Http()))
    if mimeType != "application/vnd.google-apps.folder":
        return download_file_and_send_email(service,id,emailReceiver)
    else:
        return -2

def download_file_and_send_email(service, file_id, email):
    email = email.lower()
    try:
        thread = threading.Thread(target=download_file_and_send_email_utility, args=[service, file_id, email])
        thread.daemon = True                            # Daemonize thread
        thread.start()
        return 1
    except Exception as e:
        print (e)
        return -4
    return

def download_file_and_send_email_utility(service, file_id, email):
    email = email.lower()
    try:
        path_download, file_name = downoad_file_and_store(service, file_id)
        if type(path_download) == str and path_download != "":
            message_data = CreateMessageWithAttachment(email,"Your requested file "+ file_name, 
                "Please find attached the file "+ file_name+" as requested by you.",
                path_download, file_name)
            SendMessage("me",message_data)
            #send_mail(email,path_download)
        return
    except Exception as e:
        print (e)
        return
        
def test():
    # id = "\'1NN0wJ2hMHWyln-KgqqiZLybOH2q4Cix6\'"
    # folder_id ="0AO0A7oDlmt0DUk9PVA"
    # file_id = "1WbMDp05IO9MIlJvbmee53ZB2Kt7eOWYr"
    # file_id_google_docs = "1mteq1rcYXJW8LsNELbY3zP8-3zyUMAYvgoGusGngwBg"
    # email = "namankr1@gmail.com"
    # secure_key = "QTK3Z3AVRWQFD4PNEG1UDAGR745CHESZ"
    # credentials = get_credentials_drive()
    # service = build('drive', 'v3', http=credentials.authorize(Http()))
    # return drive_list(service,id)
    message1 = CreateMessage("mksclients@gmail.com","Test Mail", "Test Mail")
    return SendMessage("me",message1)
