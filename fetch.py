from datetime import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from data import Block
from data import Course
from data import DayPattern
from data import Room
from data import Time
from data import ModelBuilderInput


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '11PsAQoazA3Jr799Nj4BPON4mANbjSsKjVizXh1cKK1M'
COURSES_TO_SCHEDULE_RANGE = 'Courses to Schedule!A2:J'
ROOMS_RANGE = 'Rooms!A2:B'
BLOCKS_RANGE = 'Blocks!A2:C'
OCCUPIED_TIMES_RANGE = 'Occupied Times!A2:D'
CONFIG_RANGE = 'Config!A2:B'


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


def get_sheets():
    """ Query Google Sheets and return each sheet in a different dict entry. """
    sheets_api = SheetsApi(SPREADSHEET_ID)

    courses_rows = sheets_api.get(COURSES_TO_SCHEDULE_RANGE)
    rooms_rows = sheets_api.get(ROOMS_RANGE)
    blocks_rows = sheets_api.get(BLOCKS_RANGE)
    occupied_times_rows = sheets_api.get(OCCUPIED_TIMES_RANGE)
    config_rows = sheets_api.get(CONFIG_RANGE)

    return {
        'courses': courses_rows,
        'rooms': rooms_rows,
        'blocks': blocks_rows,
        'occupied_times': occupied_times_rows,
        'config': config_rows,
    }


def convert_course(row):
    """ Convert a row of the courses sheet to our internal representation.

    Schema:

    [0]: course_id: str
    [1]: day_pattern: str
    [2]: block: int
    [3]: enrollment: int
    [4]: lecture hours per week: int
    [5]: lab hours per week: int
    [6]: # weeks: float
    [7]: min minutes per day: int
    [8]: total lecture minutes per week: int
    [9]: total lab minutes per week: int
    """
    return Course(
        course_id=str(row[0]),
        day_pattern=DayPattern.parse(row[1]),
        desired_block=int(row[2]),
        enrollment=int(row[3]),
        lecture_minutes_per_day=int(row[7]),
        lab_minutes_per_week=int(row[9]),
    )


def str_to_time(timestr: str) -> Time:
    time = datetime.strptime(timestr, "%H:%M:%S %p").time()
    return Time(hour=time.hour, minute=time.minute)


def convert_block(row):
    """ Convert a row of the blocks sheet to our internal representation.

    Schema:

    [0]: id: int
    [1]: start_time: str
    [2]: end_time: str
    """
    return Block(
        block_id=int(row[0]),
        start_time=str_to_time(row[1]),
        end_time=str_to_time(row[2]),
    )


def convert_room(row):
    """ Convert a row of the rooms sheet to our internal representation.

    Schema:

    [0]: room name: str
    [1]: seats: int
    """
    return Room(
        room_name=row[0],
        seats=int(row[1]),
    )


def convert_occupied_time(row):
    # TODO: add hard-blockers occupying rooms at certain times
    pass


def convert_all_sheets(sheets):
    converters = {
        'courses': convert_course,
        'rooms': convert_room,
        'blocks': convert_block,
        'occupied_times': convert_occupied_time,
    }

    converted = {}

    for key, converter in converters.items():
        converted[key] = [
            converter(row) for row in sheets[key]
        ]

    return ModelBuilderInput(
        courses=converted['courses'],
        rooms=converted['rooms'],
        blocks=converted['blocks'],
    )


def fetch_and_convert_data():
    return convert_all_sheets(get_sheets())


def print_rows(sheet):
    for row in sheet:
        print(', '.join(str(x) for x in row))


if __name__ == '__main__':
    sheets = get_sheets()

    # raw sheet representation
    for name, sheet in sheets.items():
        print_rows(sheet)

    # converted representation
    for name, data in convert_all_sheets(sheets).items():
        print(name)
        for obj in data:
            print(obj)
