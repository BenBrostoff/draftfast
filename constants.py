FFPRO = 'http://www.fantasypros.com/nfl/projections/'

ALL_POS = ['QB', 'RB', 'WR', 'TE', 'DST']
ALL_POS_TEAM = ['QB', 'RB1', 'RB2',
                'WR1', 'WR2', 'WR3', 'FLEX',
                'TE', 'DST']

COMBO_TEAM_LIMITS_NFL = []
all_nfl_teams = [
 'MIN',
 'MIA',
 'CAR',
 'ATL',
 'OAK',
 'CIN',
 'NYJ',
 'DEN',
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

for team in all_nfl_teams:
  COMBO_TEAM_LIMITS_NFL.append([team, 0, 1])

SALARY_CAP = 50000

ROSTER_SIZE = {
  'NFL': 9,
  'NBA': 8
}

POSITIONS = {
  'NBA' : [
    ["PG", 1, 3],
    ["SG", 1, 3],
    ["SF", 1, 3],
    ["PF", 1, 3],
    ["C", 1, 2]
  ],

  'NFL' : [
    ["QB", 1, 1],
    ["RB", 2, 3],
    ["WR", 3, 4],
    ["TE", 1, 2],
    ["DST", 1, 1]
  ]
}

DUO_TYPE = {
  'wr' : [
    ["QB", 1, 1],
    ["WR", 1, 1]
  ],
  'te' : [
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
  ['-dtype', 'specify WR or TE in combo', 'wr'],
  ['-l', 'league', 'NFL']
]

COMMAND_LINE = [
    ['-qbd', 'depth of qbs to search through', 4],
    ['-qbp', 'price limit on QB', 100000],
    ['-rbd', 'depth of qbs to search through', 10],
    ['-rbp', 'avg price limit on RBs', 7500],
    ['-wrd', 'depth of qbs to search through', 20],
    ['-wrp', 'avg price limit on WR', 6500],
    ['-flexd', 'depth of flex to search through', 4],
    ['-flexp', 'price limit on flex', 8000],
    ['-ted', 'depth of TE to search through', 4],
    ['-tep', 'price limit on TE', 4000],
    ['-dd', 'depth of defense to search through', 4],
    ['-dp', 'price limit on defense', 4000],
    ['-wrk', 'processes enabled - ' +
             'you will still exhaust memory if you ' +
             'stray far from depth defaults', 2]    
]