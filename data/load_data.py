import asyncio
import glob
import os
from typing import List

from app.models import db, WinningBond
from data.file_parser import BondDataParser, year_month_from_file


async def load_data(files: List[str], conn: str) -> None:
    await db.set_bind(conn)
    try:
        await db.gino.create_all()
    except Exception as e:
        print(e)
    for file in files:
        year, month = year_month_from_file(file)
        parser = BondDataParser(file, year, month)
        for bond in parser.winning_bonds():
            insert = await WinningBond.create(bond=bond.num, date=bond.date, prize=bond.prize)
            print(insert)
    return


def run_multiple(files: List[str], conn: str) -> None:
    tasks = [load_data([file], conn) for file in files]
    work_groups = asyncio.gather(*tasks)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(work_groups)
    finally:
        loop.close()


if __name__ == '__main__':
    connection_string = os.getenv('DATABASE_CONNECTION')
    files = glob.glob('*.txt')
    run_multiple(files, connection_string)