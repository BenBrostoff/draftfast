def calculate_fanpros_ppr(row, pos):
    row = [x.text for x in row]
    projected_score = 0
    if pos.upper() == 'QB':
        projected_score += (0.04 * float(row[3])) + (4 * float(row[4])) + (3 if float(row[3]) >= 300 else 0) + (-1 * float(row[5])) + (0.1 * float(row[7])) + (6 * float(row[8])) + (3 if float(row[7]) >= 100 else 0) + (-1 * float(row[9]))
    elif pos.upper() == 'RB' or pos.upper() == 'WR':
        projected_score += (0.1 * float(row[2])) + (6 * float(row[3])) + (3 if float(row[2]) >= 100 else 0) + (1 * float(row[4])) + (0.1 * float(row[5])) + (6 * float(row[6])) + (3 if float(row[5]) >= 100 else 0) + (-1 * float(row[7]))
    elif pos.upper() == 'TE':
        projected_score += (1 * float(row[1])) + (0.1 * float(row[2])) + (6 * float(row[3])) + (3 if float(row[2]) >= 100 else 0) + (-1 * float(row[4]))
    elif pos.upper() == 'DST':
        points_allowed = float(row[8])
        if points_allowed == 0:
            projected_score += 10
        elif points_allowed <= 6:
            projected_score += 7
        elif points_allowed <= 13:
            projected_score += 4
        elif points_allowed <= 20:
            projected_score += 1
        elif points_allowed <= 27:
            pass
        elif points_allowed <= 34:
            projected_score += -1
        else:
            projected_score += -4
        projected_score += (1 * float(row[1])) + (2 * float(row[2])) + (2 * float(row[3])) + (6 * float(row[5])) + (2 * float(row[7]))
    return round(projected_score, 2)
