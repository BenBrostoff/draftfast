from os import listdir, path
import csv

CUR_PROJ = 'current-projections.csv'

def combine_projections():
    all_projections = filter(lambda x: x.split('-')[0] == 'current' and x != CUR_PROJ , listdir('data'))
    if len(all_projections) > 0:
        hold = {}
        for proj_file in all_projections:
            with open(path.join('data', proj_file), 'rb') as csvfile:
                csvdata = csv.DictReader(csvfile)
                for idx, row in enumerate(csvdata):
                    if idx > 0:
                        if row['playername'] in hold:
                            hold[row['playername']].append(row['points'])
                        else:
                            hold[row['playername']] = [row['points']]
    proj_dict = {k: v for k, v in hold.iteritems() if len(hold[k]) == len(all_projections)}
    hold = []
    for key, val in proj_dict.items():
        hold.append([key, round(sum(map(lambda x: float(x), val)) / len(val), 2)])
    return hold

def write_combined_projections():
    projections = [['playername', 'points']]
    projections.extend(combine_projections())
    with open(path.join('data', CUR_PROJ), 'w') as proj:
        w = csv.writer(proj, delimiter=',')
        w.writerows(projections)
