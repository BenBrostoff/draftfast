ALL_POS = ['QB', 'RB', 'WR', 'TE', 'DST']
ALL_POS_TEAM = ['QB', 'RB1', 'RB2',
                'WR1', 'WR2', 'WR3', 'FLEX',
                'TE', 'DST']

COMBO_TEAM_LIMITS_NFL = []
ALL_NFL_TEAMS = [
 'GB',
 'MIN',
 'MIA',
 'CAR',
 'ATL',
 'OAK',
 'CIN',
 'NYJ',
 'DEN',
 'DET',
 'BAL',
 'NYG',
 'TEN',
 'NO',
 'DAL',
 'NE',
 'SEA',
 'CLE',
 'TB',
 'PIT',
 'CHI',
 'HOU',
 'WAS',
 'JAX',
 'KC',
 'PHI',
 'BUF',
 'IND',
 'ARI',
 'SF',
 'LA',
 'D/ST',
 'SD']

for team in ALL_NFL_TEAMS:
    COMBO_TEAM_LIMITS_NFL.append([team, 0, 1])

SALARY_CAP = 50000

ROSTER_SIZE = {
  'NFL': 9,
  'NBA': 8
}

POSITIONS = {
  'NBA': [
    ["PG", 1, 3],
    ["SG", 1, 3],
    ["SF", 1, 3],
    ["PF", 1, 3],
    ["C", 1, 2]
  ],

  'NFL': [
    ["QB", 1, 1],
    ["RB", 2, 3],
    ["WR", 3, 4],
    ["TE", 1, 2],
    ["DST", 1, 1]
  ]
}

DUO_TYPE = {
  'wr': [
    ["QB", 1, 1],
    ["WR", 1, 1]
  ],
  'te': [
    ["QB", 1, 1],
    ["TE", 1, 1]
  ]
}
