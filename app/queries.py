

BIGGEST_WINNERS = """SELECT bond, sum(prize), count(bond) from winning_bonds
                    group by bond
                    order by 2 desc
                    limit(100);"""

MOST_TIMES_WON = """SELECT bond, sum(prize), count(bond) from winning_bonds
                    group by bond
                    order by 3, 2 desc
                    limit(100);"""