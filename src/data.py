from pdb import set_trace as stop
import os
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from dotenv import dotenv_values

import pandas as pd
import pyodbc

def get_project_root() -> Path:
    """Return path to the src folder"""
    return Path(__file__).parent.resolve().parent

# load variables from .env file into dictionary
config = dotenv_values(get_project_root() / ".env")


QUERY_TEMPLATE = """
SELECT
    top(100)
    callDate
    ,callType
    ,disposition
FROM
    tel.callSessions WITH(NOLOCK)
WHERE
    callDate BETWEEN '{date}' AND DATEADD(day, 1, '{date}')
"""


def generate(from_date: str, to_date: str):
    """"""
    # path where all the downloaded csv files are stored
    download_dir = Path(config['DATA_DIR']) / 'downloads'
    if not download_dir.exists():
        # create it if does not exist yet
        os.makedirs(download_dir)

    # list of days we want to download data for
    dates = [d.strftime("%Y-%m-%d") for d in pd.date_range(from_date, to_date)]

    for date in dates:

        # fetch data from db for this date
        data = get_data_from_db(date=date)

        # save data in a csv file
        output_path = download_dir / f'{date}.csv'
        data.to_csv(output_path, index=False)

    # concatenate data for all dates
    all_data = pd.concat([pd.read_csv(download_dir / f'{date}.csv') for date in dates])

    # and save it as csv file
    file_path = Path(config['DATA_DIR']) / f'training_data_{from_date}_{to_date}.csv'
    all_data.to_csv(file_path, index=False)


def get_data_from_db(date: str) -> pd.DataFrame:

    # replace {date} in QUERY_TEMPLATE
    query = QUERY_TEMPLATE.format(date=date)

    # open connection with DB
    conn = pyodbc.connect(
        server=config['SERVER'],
        database=config['DATABASE'],
        user=config['USER'],
        password=config['PASSWORD'],
        port=config['PORT'],
        driver=config['DRIVER']
    )

    # run query and get data from DB into pandas dataframe
    df = pd.read_sql_query(query, conn)

    # close connection
    conn.close()

    return df


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--from', dest='from_date', type=str, required=True)
    parser.add_argument('--to', dest='to_date', type=str, required=True)
    args = parser.parse_args()

    generate(args.from_date, args.to_date)