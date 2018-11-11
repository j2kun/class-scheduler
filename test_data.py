from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '11PsAQoazA3Jr799Nj4BPON4mANbjSsKjVizXh1cKK1M'
COURSES_TO_SCHEDULE_RANGE = 'Courses to Schedule!A:J'
ROOMS_RANGE = 'Rooms!A:B'
BLOCKS_RANGE = 'Blocks!A:C'
OCCUPIED_TIMES_RANGE = 'Occupied Times!A:D'
CONFIG_RANGE = 'Config!A:B'


class SheetsApi:
    def __init__(self, spreadsheet_id):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('sheets', 'v4', http=creds.authorize(Http()))

        self.api = service.spreadsheets()
        self.spreadsheet_id = spreadsheet_id

    def get(self, range_expr):
        print("Fetching '{}'".format(range_expr))
        values = self.api.values().get(
            spreadsheetId=self.spreadsheet_id,
            range=range_expr
        ).execute().get('values', [])

        if not values:
            raise Exception("Could not find values for {}".format(range_expr))

        return values


def print_rows(sheet):
    for row in sheet:
        print(', '.join(str(x) for x in row))


def print_spreadsheet():
    """Prints spreadsheet for diagnostics."""
    sheets_api = SheetsApi(SPREADSHEET_ID)

    courses_rows = sheets_api.get(COURSES_TO_SCHEDULE_RANGE)
    rooms_rows = sheets_api.get(ROOMS_RANGE)
    blocks_rows = sheets_api.get(BLOCKS_RANGE)
    occupied_times_rows = sheets_api.get(OCCUPIED_TIMES_RANGE)
    config_rows = sheets_api.get(CONFIG_RANGE)

    print_rows(courses_rows)
    print_rows(rooms_rows)
    print_rows(blocks_rows)
    print_rows(occupied_times_rows)
    print_rows(config_rows)

if __name__ == '__main__':
    print_spreadsheet()
