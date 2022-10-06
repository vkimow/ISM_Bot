import io
import os
from turtle import down
from googleapiclient.http import MediaIoBaseDownload
class Parser:
    @staticmethod
    def get_google_sheet(service, spreadsheet_id, sheet_name, start_col = '', end_col = '', start_row = '', end_row = ''):
        range = f"{sheet_name}!{start_col}{start_row}:{end_col}{end_row}"
        return service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range,
            majorDimension='ROWS'
        ).execute()

    @staticmethod
    def set_google_sheet(service, spreadsheet_id, sheet_name, values, start_col = '', end_col = '', start_row = '', end_row = ''):
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f"{sheet_name}!{start_col}{start_row}:{end_col}{end_row}",
                    "majorDimension": "ROWS",
                    "values": values}
                ]
            }
        ).execute()

    @staticmethod
    def clear_google_sheet(service, spreadsheet_id, sheet_name, values, start_col = '', end_col = '', start_row = '', end_row = ''):
        range = f"{sheet_name}!{start_col}{start_row}:{end_col}{end_row}"
        body = {}
        service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=range, body=body).execute()

    @staticmethod
    def download_google_drive_file(service, file_id, path, name):
        request = service.files().get_media(fileid = file_id)
        fh = io.BytesIO
        downloader = MediaIoBaseDownload(fd=fh, request=request)

        done = False

        while not done:
            status, done = downloader.next_chunk()
            print('Download progress: {}'.format(status.progress() * 100))

        fh.seek(0)

        with open(os.path.join(path, name), 'wb') as f:
            f.write(fh.read())
            f.close()


    @staticmethod
    def get_row(google_sheet, row):
        return google_sheet["values"][row]

    @staticmethod
    def get_cell_value(google_sheet, col, row):
        return google_sheet["values"][row][col]

    @staticmethod
    def set_cell_value(google_sheet, col, row, value):
        google_sheet["values"][row][col] = value

    @staticmethod
    def get_col_length(google_sheet):
        return len(google_sheet["values"][0])

    @staticmethod
    def get_row_length(google_sheet):
        return len(google_sheet["values"])
