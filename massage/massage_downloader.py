import os
from google.google_parser import Parser
from config import Paths

class MassageDownloader:
    def __init__(self, services):
        self.services = services

    def load(self, files_to_download):
        def create_folder(folder_path):
            if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

        create_folder(Paths.remote)
        create_folder(Paths.actions)
        create_folder(Paths.backgrounds)
        create_folder(Paths.specialists)

        for root, dir, files in os.walk(Paths.remote):
            for file in files:
                os.remove(os.path.join(root, file))

        for file in files_to_download:
            file.download(self.services.drive)
