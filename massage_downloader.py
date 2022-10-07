import os
from google_parser import Parser
from config import Paths

def load(services, files_to_download):
    def create_folder(folder_path):
        if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    create_folder(Paths.resource)
    create_folder(Paths.actions)
    create_folder(Paths.anatomy)
    create_folder(Paths.backgrounds)
    create_folder(Paths.specialists)

    for root, dir, files in os.walk(Paths.resource):
        for file in files:
            os.remove(os.path.join(root, file))

    for file in files_to_download:
        file.download(services.drive)