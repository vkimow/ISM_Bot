import os
from google_parser import Parser
from config import Paths

def load(services, files_to_download):
    for root, dir, files in os.walk(Paths.resource):
        for file in files:
            os.remove(os.path.join(root, file))

    for file in files_to_download:
        file.download(services.drive)