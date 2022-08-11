from __future__ import print_function

import os.path
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSheet:
    # ID csv документу з url
    SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = None

    def __init__(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print('flow')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

    def updateRangeValues(self, range, values):
        data = [{
            'range': range,
            'values': values
        }]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID,
                                                                  body=body).execute()
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))


def main():
    gs = GoogleSheet()
    # назва листу та поля в які додаватимуться записи
    test_range = 'result!A382:J382'
    # Данні для запису 1 запис == 1 поле
    test_values = [
        ['Модель', 'Ціна', 'Стан', 'Дата публікації', 'Місто', 'Район', 'Координати', "Им'я", 'Компанія', 'Лінк'],
    ]
    gs.updateRangeValues(test_range, test_values)


if __name__ == '__main__':
    main()