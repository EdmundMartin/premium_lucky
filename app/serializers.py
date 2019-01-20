

def bond_history_serializer(bonds):
    total_won, prize_count = 0, 0
    all_wins = {}
    for b in bonds:
        current_date = b.date.strftime('%m/%d/%Y')
        total_won += b.prize
        prize_count += 1
        if b.date in all_wins:
            all_wins[current_date].append(b.prize)
        else:
            all_wins[current_date] = b.prize
    print(all_wins, total_won, prize_count)
    return {'win_history': all_wins, 'total_won': total_won, 'prize_count': prize_count}