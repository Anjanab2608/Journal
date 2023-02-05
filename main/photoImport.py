from __future__ import print_function

import datetime
import io
import os

import httplib2
from PIL import Image
from apiclient import discovery
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from oauth2client import tools, client
from oauth2client.file import Storage

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class Auth:
    def __init__(self,
                 SCOPES,
                 CLIENT_SECRET_FILE,
                 APPLICATION_NAME,
                 GOOGLE_CRED_FILE
                 ):
        self.SCOPES = SCOPES
        self.CLIENT_SECRET_FILE = CLIENT_SECRET_FILE
        self.APPLICATION_NAME = APPLICATION_NAME
        self.GOOGLE_CRED_FILE = GOOGLE_CRED_FILE

    def getCredentials(self):
        """Gets valid user credentials from storage.
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
        Returns:
            Credentials, the obtained credential.
        """
        cwd_dir = os.getcwd()
        credential_dir = os.path.join(cwd_dir, self.CLIENT_SECRET_FILE)
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(cwd_dir,
                                       self.GOOGLE_CRED_FILE)
        print(credential_path)
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials


class Credential:
    def __init__(
            self,
            google_cred,
            app_name,
            client_secret,
            scope):

        auth = Auth(
            GOOGLE_CRED_FILE=google_cred,
            APPLICATION_NAME=app_name,
            CLIENT_SECRET_FILE=client_secret,
            SCOPES=scope)

        credentials = auth.getCredentials()
        http = credentials.authorize(httplib2.Http())
        self.drive_service = discovery.build('drive', 'v3', http=http)

    def listFiles(self, size):
        results = self.drive_service.files().list(
            pageSize=size, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print('{0} ({1})'.format(item['name'], item['id']))

    # Download_Image
    def download_file(self,
                      real_file_id,
                      filepath):
        request = self.drive_service.files().get_media(fileId=real_file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print('Downloading...{0:.2f}'.format(status.progress() * 100))
        with io.open(filepath, 'wb') as f:
            file.seek(0)
            f.write(file.read())

    def resize_image(self,
                     img_path,
                     date_format,
                     max_size):
        counter = 1
        today_date = datetime.datetime.today().strftime(date_format)
        with Image.open(img_path) as img:
            width, height = img.size
            if width > height:
                new_width = max_size
                new_height = int(height * (max_size / width))
            else:
                new_width = max_size
                new_height = int(height * (max_size / width))
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
            new_file_path = '{}_{}.jpg'.format(today_date, counter)
            img.save(new_file_path)
            counter += 1

    def create_folder(self, filepath):
        file_metadata = {
            'name': filepath,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.drive_service.files().create(body=file_metadata, fields='id').execute()
        print(F'Folder ID: "{file.get("id")}".')

    def uploadFile(self, filename, filepath, mimetype):
        file_metadata = {'name': filename}
        media = MediaFileUpload(filepath,
                                mimetype=mimetype)
        file = self.drive_service.files().create(body=file_metadata,
                                                 media_body=media,
                                                 fields='id').execute()
        print(F'File ID: {file.get("id")}')

    def search_file(self, query):
        # q = query i.e. the condition which use for searching the file/folder
        files = []
        page_token = None
        while True:
            response = self.drive_service.files().list(q=query,
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
