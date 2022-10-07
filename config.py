from importlib.resources import path
from pathlib import Path
import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

class SpreadsheetIds:
    main = '1T36DM8mLYkgg7-vYCpEtD_FIP7CKdf61r45UkUE49BI'

class BotTokens:
    main = '5600845189:AAHnJX5AZl3mKz7V6agQndnVyvYFq6cfjNM'

class Paths:
    resource = 'resource'
    actions = resource + '/actions'
    backgrounds = resource + '/backgrounds'
    specialists = resource + '/specialists'
    anatomy = resource + '/anatomy'

class Resources:
    class Photos:
        def background(name):
            return f'{Paths.backgrounds}/{name}.jpg'
        def organ(name):
            return f'{Paths.anatomy}/{name}.jpg'
        def specialist(name):
            return f'{Paths.specialists}/{name}.jpg'
        def action(name_with_extension):
            return f'{Paths.actions}/{name_with_extension}'
