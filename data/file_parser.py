from collections import namedtuple
import datetime as dt
import re
from typing import List, Tuple, Union
import string


def year_month_from_file(filename) -> Tuple[int, int]:
    year = filename[-8:-4]
    month = filename[-10:-8]
    return int(year), int(month)


class BondDataParser:

    def __init__(self, filename: str, year: int, month: int):
        self.filename = filename
        self.date = dt.date(year=year, month=month, day=1)
        self._prize_regex = re.compile(r'£(?P<prize>[\d\-,]+)')
        self._bond_pattern = re.compile(r'(?P<num>[\d\-A-Z]{4,})')
        self._valid_chars = set(string.ascii_uppercase)

    def _is_divider(self, line: str) -> bool:
        if 'drawn for prize' in line.lower():
            return True
        return False

    def _current_prize(self, line: str) -> Union[int, None]:
        prize = re.search(self._prize_regex, line)
        if prize:
            return int(prize.group('prize').replace(',', ''))
        return None

    def _extract_bonds(self, line: str) -> List[str]:
        bonds = re.findall(self._bond_pattern, line)
        cleaned_bonds = []
        for val in bonds:
            if 'VIII' == val:
                continue
            elif any(i in val for i in self._valid_chars):
                cleaned_bonds.append(val)
        return cleaned_bonds

    def _can_extract_bonds(self, line: str) -> bool:
        lowered = line.lower()
        if 'page no' in lowered:
            return False
        if 'part' in lowered:
            return False
        if 'prizes of' in lowered:
            return False
        return False

    def winning_bonds(self, *args, **kwargs) -> List[namedtuple]:
        winner = namedtuple('winner', 'num prize date')
        with open(self.filename, 'r') as result_file:
            current_prize: Union[int, None] = None
            headers_passed = False
            for line in result_file:
                if 'NUMBERS DRAWN FOR PRIZES IN THE MONTHLY DRAW' in line:
                    headers_passed = True
                if self._is_divider(line):
                    prize = self._current_prize(line)
                    current_prize = prize if prize else None
                if current_prize and headers_passed:
                    if self._extract_bonds(line):
                        bonds = self._extract_bonds(line)
                        for bond in bonds:
                            yield winner(bond, current_prize, self.date)


if __name__ == '__main__':
    res = year_month_from_file('PWREP_01062018.txt')
    print(res)
    b = BondDataParser('PWREP_01062018.txt', 2018, 6)
    for b in b.winning_bonds():
        print(b.num)