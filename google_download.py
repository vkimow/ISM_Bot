from enum import IntEnum
import io
from urllib.parse import urlparse
from googleapiclient.http import MediaIoBaseDownload

def download_google_drive_file(service, file_id, full_path):
    request = service.files().get_media(fileId = file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)
    done = False

    while not done:
        status, done = downloader.next_chunk()
        print(f'Progress: {status.progress() * 100} | {full_path}')

    fh.seek(0)

    with open(full_path, 'wb') as f:
        f.write(fh.read())
        f.close()

def get_drive_id_from_url(drive_url):
    splited = drive_url.split('/')
    return splited[5]

class DownloadStatus(IntEnum):
    NotDownloaded = 0
    Downloading = 1
    Downloaded = 2

class Downloadable:
    def __init__(self, file_id_or_link, path, name, extension):
        parsed = urlparse(file_id_or_link)
        if(parsed.scheme == 'https'):
            if(parsed.hostname != 'drive.google.com'):
                return

            file_id_or_link = parsed.path.split('/')[3]

        self.file_id = file_id_or_link
        self.path = path
        self.name = name
        self.extension = extension
        self.status = DownloadStatus.NotDownloaded
        self.progress = 0

    def download(self, service):
        self.status = DownloadStatus.Downloading
        download_google_drive_file(service, self.file_id, self.get_full_path())
        self.status = DownloadStatus.Downloaded
        self.progress = 1

    def get_full_name(self):
        return f'{self.name}.{self.extension}'

    def get_full_path(self):
        return f'{self.path}/{self.get_full_name()}'
