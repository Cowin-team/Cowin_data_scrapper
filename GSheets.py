# importing the required libraries
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheets:
    def __init__(self, creds_file = 'creds.json'):

        # define the scope
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

        # add credentials to the account
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)

        # authorize the clientsheet 
        self.client = gspread.authorize(creds)

    def get_sheet(self, sheet_name):
        # get the instance of the Spreadsheet
        sheet = self.client.open(sheet_name)

        # get the first sheet of the Spreadsheet
        sheet_instance = sheet.get_worksheet(0)
        # get all the records of the data
        records_data = sheet_instance.get_all_records()
        # convert the json to dataframe
        records_df = pd.DataFrame.from_dict(records_data)

        # view the top records
        print(records_df.head())

        return records_df
        
    def update(self, data):
        
        # get the instance of the Spreadsheet
        sheet = self.client.open(data["Sheet Name"])

        # get the first sheet of the Spreadsheet
        sheet_instance = sheet.get_worksheet(0)
        # get all the records of the data
        records_data = sheet_instance.get_all_records()
        # convert the json to dataframe
        records_df = pd.DataFrame.from_dict(records_data)
        
        # print(records_df)
        index_list = records_df[(records_df['Name'] == data['Name'])].index

        # # check if the data already exists
        if (len(index_list)):
            isDiff = False
            row = records_df[records_df['Name'] == data['Name']]
            row_cols = row.columns
            for col in row_cols:
                if col in data.keys():
                    # Check if there is a diff between the data and the sheet for this row
                    if row[col].values[0] != data[col]:
                        row[col] = data[col]
                        isDiff = True
            
            if isDiff:
                sheet_instance.delete_row(int(index_list[0])+2)
                    # Update the row values of the sheets with the diff
                sheet_instance.insert_row(row.values[0].tolist(), index=int(index_list[0])+2)
        else:
            sheet_columns = list(records_df.columns)
            row_values = []
            for key in sheet_columns:
                if key in data.keys():
                    row_values.append(data[key])
                else:
                    row_values.append(None)
            
            # Delete the old row and push the new one
            print(sheet_instance.insert_row(row_values, index=len(records_df.index)+2))
        # print(sheet_instance.get_col_values())
        
    def get_all_sheets(self):
        titles_list = []
        for spreadsheet in self.client.openall():
            print(spreadsheet.title)
            titles_list.append(spreadsheet.title)
            
        return titles_list

if __name__ == "__main__":
    sheets = GoogleSheets()
    data = {
            "Sheet Name": "Thanjavur Beds",
            "Name":"Fake",
            "URL":"https://www.google.com/maps/place/Thanjavur+Medical+College/@10.7580923,79.1035782,17z/data=!4m9!1m2!2m1!1sThanjavur+Medical+College!3m5!1s0x3baabf337761a613:0x69900b85db55755e!8m2!3d10.7586!4d79.1066!15sChlUaGFuamF2dXIgTWVkaWNhbCBDb2xsZWdlWiwKD21lZGljYWwgY29sbGVnZSIZdGhhbmphdnVyIG1lZGljYWwgY29sbGVnZZIBDm1lZGljYWxfc2Nob29ssAEA",
            "COVID Beds": 226,
            "Oxygen Beds":372,
            "ICU": 200,
            "LAST UPDATED": "2021-05-03 15:24:37"
        }
    
    sheets.update(data,)