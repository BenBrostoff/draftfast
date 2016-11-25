import csv
import data_cleaning_constants as cons

new_rows = []
dk_csv = 'data/current-salaries.csv'

with open(dk_csv, 'rb') as f:
    reader = csv.reader(f)
    for idx, row in enumerate(reader):
        new_row = row
        for player in cons.DUPLICATES:
            if player['name'] in row:
                if player['team'] not in row:
                    print "Skipping non-key duplicate %s" % player['name']
                    new_row = None

        for player in cons.RENAMES:
            if player['dk_name'] in row:
                print "Changed name for %s in CSV" % player['rename']
                new_row = [player['rename'] if x == player['dk_name']
                           else x for x in row]

        if new_row:
            new_rows.append(new_row)


with open(dk_csv, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(new_rows)
