#!/usr/bin/env python3

import pytz
import gspread
from itertools import count
from os import environ as ENV
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials as Credentials

SCOPE = ['https://www.googleapis.com/auth/drive']
TOKEN = 'token.json'
SPREADSHEET_TITLE = ENV['GSHEET_SPREADSHEET_TITLE']
SPREADSHEET_INSTANCE = int(ENV['GSHEET_SPREADSHEET_INSTANCE'])
PROBLEM_NAME = ENV['PROBLEM_NAME']
USER_LOGIN = ENV['USER_LOGIN']
TIMEZONE = pytz.timezone('Europe/Moscow')


def main():
    print('[INFO]   Reading creditionals')
    creditionals = Credentials.from_json_keyfile_name(TOKEN, SCOPE)
    print('[INFO]   Reading creditionals success')

    print('[INFO]   Logging to Google')
    client = gspread.authorize(creditionals)
    print('[INFO]   Log in success')

    print('[INFO]   Opening spreadsheet')
    sheet = client.open(SPREADSHEET_TITLE)
    print('[INFO]   Open success')

    print('[INFO]   Getting worksheet')
    sheet_instance = sheet.get_worksheet(SPREADSHEET_INSTANCE)
    print('[INFO]   Get success')

    print('[INFO]   Getting problem column')
    for col in count(start=8):
        cell_value = sheet_instance.cell(row=3, col=col).value
        print(f'[INFO]   Looking at cell (3, {col}) = "{cell_value}"')
        if cell_value is None:
            print('[ERROR]  No such problem name in spreadsheet')
            raise Exception('No such problem name in spreadsheet')
        elif cell_value == PROBLEM_NAME:
            print(f'[INFO]   Found problem column = "{col}"')
            problem_col = col
            break

    print('[INFO]   Getting problem score')
    problem_score = sheet_instance.cell(row=1, col=problem_col).value
    assert problem_score is not None
    print(f'[INFO]   Problem score = "{problem_score}"')
    problem_score = int(problem_score)

    print('[INFO]   Getting problem deadline')
    problem_deadline = sheet_instance.cell(row=2, col=problem_col).value
    assert problem_deadline is not None
    print(f'[INFO]   Problem deadline raw = "{problem_deadline}"')
    problem_deadline = datetime.strptime(
        problem_deadline, '%d/%m/%y %H:%M').astimezone(TIMEZONE)
    print(f'[INFO]   Problem deadline = "{problem_deadline}"')

    print('[INFO]   Getting user row')
    for row in count(start=4):
        cell_value = sheet_instance.cell(row=row, col=4).value
        print(f'[INFO]   Looking at cell (3, {col}) = "{cell_value}"')
        if cell_value is None:
            print('[ERROR]  No such user login in spreadsheet')
            raise Exception(
                'No such user login')
        elif cell_value == USER_LOGIN:
            print(f'[INFO]   Found user row = "{row}"')
            user_row = row
            break

    print('[INFO]   Getting current score in sheet')
    sheet_score = sheet_instance.cell(row=user_row, col=problem_col).value
    print(f'[INFO]   Current score in sheet = "{sheet_score}"')
    if sheet_score is None:
        sheet_score = 0
    else:
        sheet_score = int(sheet_score)

    current_time = datetime.now(TIMEZONE)
    print(f'[INFO]   Time in Moscow according to server = "{current_time}"')
    if current_time > problem_deadline:
        week = timedelta(days=7)
        if (current_time - problem_deadline) > week:
            current_score = int(problem_score / 2)
        else:
            current_score = int(problem_score *
                                (1 - (current_time - problem_deadline).total_seconds() /
                                 week.total_seconds()))
    else:
        current_score = int(problem_score)
    print(f'[INFO]   New score with deadline = "{current_score}"')

    if sheet_score < 0:
        update_value = sheet_score
    else:
        update_value = str(int(max(sheet_score, current_score)))
    print(f'[INFO]   Update value = "{update_value}"')

    print('[INFO]   Updating value in sheet')
    sheet_instance.update_cell(
        row=user_row, col=problem_col, value=update_value)
    print('[INFO]   Update value in sheet success')


if __name__ == '__main__':
    main()
