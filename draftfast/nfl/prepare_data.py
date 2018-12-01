import csv
import data_cleaning_constants as cons

new_rows = []
dk_csv = 'data/current-salaries.csv'

with open(dk_csv, 'r') as f:
    reader = csv.reader(f)
    for idx, row in enumerate(reader):
        new_row = row
        for player in cons.DUPLICATES:
            if player['name'] in row:
                if player['team'] in row:
                    print(
                        'Skipping non-key duplicate {} on {}'
                        .format(player['name'], player['team'])
                    )
                    new_row = None
        if new_row:
            new_rows.append(new_row)


with open(dk_csv, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(new_rows)
