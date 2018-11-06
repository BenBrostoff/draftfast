'''
Converts nfl stats to DraftKings scoring
'''

DK_OFF_SCORING_MULTIPLIERS = {
    'PASS-TD': 4,
    'PASS-YD': 0.04,
    'INT': -1,
    'RUSH-TD': 6,
    'RUSH-YD': 0.1,
    'REC-TD': 6,
    'REC-YD': 0.1,
    'REC': 1,
    'MISC-TD': 6,
    'FL': -1,
    '2PT': 2
}

DK_DEF_SCORING_MULTIPLIERS = {
    'SACK': 1,
    'INT': 2,
    'FR': 2,
    'TD': 6,
    'SAFETY': 2,
    'BLOCKED_KICK': 2,
    '2PT': 2
}


def generate_empty_stat_dict(pos):
    stat_dict = {}
    if pos.upper() in ('QB', 'RB', 'WR', 'TE'):
        for key in ('PASS-TD',
                    'PASS-YD',
                    'INT',
                    'RUSH-TD',
                    'RUSH-YD',
                    'REC-TD',
                    'REC-YD',
                    'REC',
                    'MISC-TD',
                    'FL',
                    '2PT'):
            stat_dict[key] = 0
    else:
        for key in ('SACK',
                    'INT',
                    'FR',
                    'TD',
                    'SAFETY',
                    'BLOCKED_KICK',
                    '2PT'):
            stat_dict[key] = 0
    return stat_dict


def points_allowed_score(points_allowed):
    if points_allowed == 0:
        score = 10
    elif points_allowed <= 6:
        score = 7
    elif points_allowed <= 13:
        score = 4
    elif points_allowed <= 20:
        score = 1
    elif points_allowed <= 27:
        score = 0
    elif points_allowed <= 34:
        score = -1
    else:
        score = -4
    return score


def offensive_conditional_points(stat_dict):
    return (3 if stat_dict['PASS-YD'] >= 300 else 0) + \
           (3 if stat_dict['RUSH-YD'] >= 100 else 0) + \
           (3 if stat_dict['REC-YD'] >= 100 else 0)


def calculate_ppr(pos, stat_dict):
    projected_points = 0
    if pos.upper() in ('QB', 'RB', 'WR', 'TE'):
        for key, val in list(stat_dict.items()):
            projected_points += val * DK_OFF_SCORING_MULTIPLIERS[key]
        projected_points += offensive_conditional_points(stat_dict)
    else:
        for key, val in list(stat_dict.items()):
            if key != 'POINTS_ALLOWED':
                projected_points += val * DK_DEF_SCORING_MULTIPLIERS[key]
        projected_points += points_allowed_score(stat_dict['POINTS_ALLOWED'])
    return round(projected_points, 2)
