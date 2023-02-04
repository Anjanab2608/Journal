from __future__ import print_function
import httplib2
import os,io

from apiclient import discovery
from oauth2client import tools as tools
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import requests
import re
import shutil
import datetime
#os.add_dll_directory(r"C:\Users\Anu\anaconda3\DLLs")

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Journal'

authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

def listFiles(size):
    results = drive_service.files().list(
        pageSize=size,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
#listFiles(5)

#############Download_Image###########
counter = 0
def resize_image(filepath, new_file_path, max_size):
    with Image.open(filepath) as img:
        width, height = img.size
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        date_taken = img._getexif().get(36867)
        if date_taken:
            date_taken = datetime.datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S')
            new_file_path = '{}_{}'.format(date_taken.strftime('%Y%m%d_%H%M%S'), new_file_path)
        else:
            pass
        img.save(new_file_path)

def download_file(real_file_id,filepath):
    request = drive_service.files().get_media(fileId=real_file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(F'Download {int(status.progress() * 100)}.')
    with io.open(filepath,'wb') as f:
        file.seek(0)
        f.write(file.read())
#download_file('1rwJtsA0noHueLV_kOl4Is4crWPFkimvH','tornado.jpg')

def uploadFile(filename,filepath,mimetype):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print(F'File ID: {file.get("id")}')

#uploadFile('Huricane.jpg','Huricane.jpg','image/jpg')

def create_folder(name):
    file_metadata = {
    'name': 'name_required',
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata, fields='id'
                                      ).execute()
    print(F'Folder ID: "{file.get("id")}".')
# create_folder("Its me")

def search_file(size, query):
    #q = query i.e. the condition which use for serhing the file/folder
    files = []
    page_token = None
    while True:
        response = drive_service.files().list(q= query,
                                        spaces='drive',
                                        fields='nextPageToken, '
                                               'files(id, name)',
                                        pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            print(F'Found file: {file.get("name")}, {file.get("id")}')
        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
#search_file(10,"name contains 'weather'")
