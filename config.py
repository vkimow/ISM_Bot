from importlib.resources import path
from pathlib import Path
import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

class SpreadsheetIds:
    main = '1T36DM8mLYkgg7-vYCpEtD_FIP7CKdf61r45UkUE49BI'

class BotTokens:
    main = '5600845189:AAHnJX5AZl3mKz7V6agQndnVyvYFq6cfjNM'

def create_google_service():
    CREDENTIALS_FILE = 'creds.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    return discovery.build('sheets', 'v4', http=httpAuth)


class Paths:
    resource = 'resource'
    actions = resource + '/actions'
    backgrounds = resource + '/backgrounds'

class Resources:
    action = Paths.actions + '/action.png'
    def background(name):
        return f'{Paths.backgrounds}/{name}.jpg'
