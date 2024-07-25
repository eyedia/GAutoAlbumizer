from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
import json
import os.path
import argparse
import logging
import datetime
from pathlib import Path
import pandas as pd 

class GooglePhotoUploader:

    def __init__(self, config):
        self.name = 'self'
        self.config = config
        self.log_file = "{0}\{1}".format(config.getConfig("log_dir"), datetime.datetime.now().strftime('mylogfile_%H_%M_%d_%m_%Y.log'))          

    def auth(self, scopes):
        flow = InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json',
        scopes=scopes)

        flow.run_local_server()    
        credentials = flow.credentials
        
        return credentials

    def get_authorized_session(self, auth_token_file):

        scopes=['openid', 'https://www.googleapis.com/auth/photoslibrary',
                'https://www.googleapis.com/auth/photoslibrary.sharing']

        cred = None

        if auth_token_file:
            try:
                cred = Credentials.from_authorized_user_file(auth_token_file, scopes)
            except OSError as err:
                logging.debug("Error opening auth token file - {0}".format(err))
            except ValueError:
                logging.debug("Error loading auth tokens - Incorrect format")


        if not cred:
            cred = self.auth(scopes)

        session = AuthorizedSession(cred)

        if auth_token_file:
            try:
                self.save_cred(cred, auth_token_file)
            except OSError as err:
                logging.debug("Could not save auth tokens - {0}".format(err))

        return session


    def save_cred(self, cred, auth_file):

        cred_dict = {
            'token': cred.token,
            'refresh_token': cred.refresh_token,
            'id_token': cred.id_token,
            'scopes': cred.scopes,
            'token_uri': cred.token_uri,
            'client_id': cred.client_id,
            'client_secret': cred.client_secret
        }

        with open(auth_file, 'w') as f:
            print(json.dumps(cred_dict), file=f)

    # Generator to loop through all albums

    def getAlbums(self, session, appCreatedOnly=False):

        params = {
                'excludeNonAppCreatedData': appCreatedOnly
        }

        while True:

            albums = session.get('https://photoslibrary.googleapis.com/v1/albums', params=params).json()

            logging.info("Server response: {}".format(albums))

            if 'albums' in albums:

                for a in albums["albums"]:
                    yield a

                if 'nextPageToken' in albums:
                    params["pageToken"] = albums["nextPageToken"]
                else:
                    return

            else:
                return

    def create_or_retrieve_album(self, session, album_title):

        # Find albums created by this app to see if one matches album_title

        for a in self.getAlbums(session):        
            if a["title"].lower() == album_title.lower():
                album_id = a["id"]
                logging.info("Uploading into EXISTING photo album -- \'{0}\'".format(album_title))
                return album_id

         # No matches, create new album

        create_album_body = json.dumps({"album":{"title": album_title}})
        #print(create_album_body)
        resp = session.post('https://photoslibrary.googleapis.com/v1/albums', create_album_body).json()

        logging.debug("Server response: {}".format(resp))

        if "id" in resp:
            logging.info("Uploading into NEW photo album -- \'{0}\'".format(album_title))
            return resp['id']
        else:
            logging.error("Could not find or create photo album '\{0}\'. Server Response: {1}".format(album_title, resp))
            return None

    def upload_photos(self, session, album_name, photo_file_list):

        album_id = self.create_or_retrieve_album(session, album_name) if album_name else None

        # interrupt upload if an upload was requested but could not be created
        if album_name and not album_id:
            return

        session.headers["Content-type"] = "application/octet-stream"
        session.headers["X-Goog-Upload-Protocol"] = "raw"

        for photo_file_name in photo_file_list:

                try:
                    photo_file = open(photo_file_name, mode='rb')
                    photo_bytes = photo_file.read()
                except OSError as err:
                    logging.error("Could not read file \'{0}\' -- {1}".format(photo_file_name, err))
                    continue

                session.headers["X-Goog-Upload-File-Name"] = os.path.basename(photo_file_name)

                logging.info("Uploading photo -- \'{}\'".format(photo_file_name))

                upload_token = session.post('https://photoslibrary.googleapis.com/v1/uploads', photo_bytes)

                if (upload_token.status_code == 200) and (upload_token.content):

                    create_body = json.dumps({"albumId":album_id, "newMediaItems":[{"description":"","simpleMediaItem":{"uploadToken":upload_token.content.decode()}}]}, indent=4)

                    resp = session.post('https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate', create_body).json()

                    logging.debug("Server response: {}".format(resp))

                    if "newMediaItemResults" in resp:
                        status = resp["newMediaItemResults"][0]["status"]
                        if status.get("code") and (status.get("code") > 0):
                            logging.error("Could not add \'{0}\' to library -- {1}".format(os.path.basename(photo_file_name), status["message"]))
                        else:
                            logging.info("Added \'{}\' to library and album \'{}\' ".format(os.path.basename(photo_file_name), album_name))
                    else:
                        logging.error("Could not add \'{0}\' to library. Server Response -- {1}".format(os.path.basename(photo_file_name), resp))

                else:
                    logging.error("Could not upload \'{0}\'. Server Response - {1}".format(os.path.basename(photo_file_name), upload_token))

        try:
            del(session.headers["Content-type"])
            del(session.headers["X-Goog-Upload-Protocol"])
            del(session.headers["X-Goog-Upload-File-Name"])
        except KeyError:
            pass


    def upload(self, album, photos):

        logging.basicConfig(format='%(asctime)s %(module)s.%(funcName)s:%(levelname)s:%(message)s',
                        datefmt='%m/%d/%Y %I_%M_%S %p',
                        filename=self.log_file,
                        level=logging.INFO)

        session = self.get_authorized_session(self.config.getConfig("auth_token_file"))
        self.upload_photos(session, album, photos)        
        #As a quick status check, dump the albums and their key attributes
        #print("{:<50} | {:>8} | {} ".format("PHOTO ALBUM","# PHOTOS", "IS WRITEABLE?"))
        # for a in getAlbums(session):
        #    print("{:<50} | {:>8} | {} ".format(a["title"],a.get("mediaItemsCount", "0"), str(a.get("isWriteable", False))))



    def uploadOneMetaData(self, meta_file_name):     
        print(meta_file_name)  
        df = pd.read_csv(meta_file_name, header=None)        
        df = df.reset_index()

        if not df.empty:
            self.upload(df[0].iloc[0], df[1].to_numpy())
        else:
            print(f"{meta_file_name} is empty, skipping it.")       


    def uploadAll(self):
        if not os.path.exists("client_secrets.json"):
            print("client_secrets.json is missing! Please contact developer.")
            return
        
        input_dir = self.config.getConfig("meta_album_dir")
        for p in Path(input_dir).glob('*.csv'):
            meta_file_name = "{0}\\{1}".format(input_dir, p.name)  
            self.uploadOneMetaData(meta_file_name)