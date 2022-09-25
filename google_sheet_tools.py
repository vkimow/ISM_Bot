class Tools:
    @staticmethod
    def get_cell_value(google_sheet, col, row):
        return google_sheet["values"][col][row]

    @staticmethod
    def set_cell_value(google_sheet, col, row, value):
        google_sheet["values"][col][row] = value

    @staticmethod
    def get_row_length(google_sheet):
        return len(google_sheet["values"][0])

    @staticmethod
    def get_col_length(google_sheet):
        return len(google_sheet["values"])
