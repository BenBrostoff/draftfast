import csv

new_rows = []
dups = ['David Johnson', 'Ryan Griffin']
dk_csv = 'data/current-salaries.csv'

with open(dk_csv, 'rb') as f:
    reader = csv.reader(f)
    for idx, row in enumerate(reader):     
        new_row = row
        for player in dups:
            if player in row:
                print "Altered duplicate %s in CSV" % player
                # A hack, let's refactor at some point
                new_row = [player + str(idx) if x == player \
                           else x for x in row]  
        new_rows.append(new_row)    

with open(dk_csv, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(new_rows)