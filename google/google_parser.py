
class Parser:
    @staticmethod
    def get_google_sheets_properties(service, spreadsheet_id):
        sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        return sheet_metadata.get('sheets')


    @staticmethod
    def get_google_sheet(service, spreadsheet_id, sheet_name, start_col = '', end_col = '', start_row = '', end_row = '', major_dimension = 'ROWS'):
        range = f"{sheet_name}!{start_col}{start_row}:{end_col}{end_row}"
        return service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range,
            majorDimension=major_dimension
        ).execute()

    @staticmethod
    def set_google_sheet(service, spreadsheet_id, sheet_name, values, start_col = '', end_col = '', start_row = '', end_row = '', major_dimension = 'ROWS'):
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f"{sheet_name}!{start_col}{start_row}:{end_col}{end_row}",
                    "majorDimension": major_dimension,
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
