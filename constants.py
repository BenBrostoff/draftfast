FFPRO = 'http://www.fantasypros.com/nfl/projections/'

ALL_POS = ['QB', 'RB', 'WR', 'TE', 'DST']
ALL_POS_TEAM = ['QB', 'RB1', 'RB2',
                'WR1', 'WR2', 'WR3', 'FLEX',
                'TE', 'DST']

COMBO_TEAM_LIMITS_NFL = []
ALL_NFL_TEAMS = [
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
 'STL',
 'CHI',
 'HOU',
 'WAS',
 'JAC',
 'KC',
 'PHI',
 'BUF',
 'IND',
 'ARI',
 'SF',
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

OPTIMIZE_COMMAND_LINE = [
  ['-s', 'scrape from FanPros', 'y'],
  ['-w', 'week of season', 1],
  ['-mp', 'missing players to allow', 100],
  ['-sp', 'salary threshold to ignore', 3000],
  ['-ms', 'max salary for player on roster', 10000],
  ['-i', 'iterations to run', 3],
  ['-lp', 'lowest acceptable projection', 0],
  ['-limit', 'disallow more than 1 player per team sans QB', 'n'],
  ['-duo', 'force a QB + WR/TE duo on specific team', 'n'],
  ['-teams', 'player must be on specified teams', None],
  ['-banned', 'player cannot be named players', None],
  ['-dtype', 'specify WR or TE in combo', 'wr'],
  ['-l', 'league', 'NFL'],
  ['-pids', 'Player id file (create upload file)', '']
]

MULTIPLE_ARGS_COMMAND = [
  '-teams',
  '-banned'
]
