ALL_POS = ('QB', 'RB', 'WR', 'TE', 'DST')
SALARY_CAP = 50000

ROSTER_SIZE = {
    'NFL': 9,
    'NBA': 8,
    'WNBA': 6,
}


def get_nfl_positions(
    rb_min=2,
    wr_min=3,
    te_min=1,
    te_upper=2
):
    return [
        ["QB", 1, 1],
        ["RB", rb_min, 3],
        ["WR", wr_min, 4],
        ["TE", te_min, te_upper],
        ["DST", 1, 1]
    ]


POSITIONS = {
    'NBA': [
        ["PG", 1, 3],
        ["SG", 1, 3],
        ["SF", 1, 3],
        ["PF", 1, 3],
        ["C", 1, 2]
      ],
    'WNBA': [
        ['PG', 1, 3],
        ['SG', 1, 3],
        ['SF', 1, 4],
        ['PF', 1, 4],
    ],
    'NFL': get_nfl_positions()
}

NBA_GENERAL_POSITIONS = [
    ['G', 3, 4],
    ['F', 3, 4],
    ['C', 1, 2],
]

WNBA_GENERAL_POSITIONS = [
    ['G', 2, 3],
    ['F', 3, 4],
]

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

DK_TO_NFL_DRAFTKINGS = {
    'Panthers': 'Carolina Panthers',
    'Buccaneers': 'Tampa Bay Buccaneers',
    'Dolphins': 'Miami Dolphins',
    'Bears': 'Chicago Bears',
    'Raiders': 'Oakland Raiders',
    'Patriots': 'New England Patriots',
    'Vikings': 'Minnesota Vikings',
    'Eagles': 'Philadelphia Eagles',
    '49ers': 'San Francisco 49ers',
    'Bengals': 'Cincinnati Bengals',
    'Bills': 'Buffalo Bills',
    'Broncos': 'Denver Broncos',
    'Browns': 'Cleveland Browns',
    'Cardinals': 'Arizona Cardinals',
    'Chargers': 'San Diego Chargers',
    'Chiefs': 'Kansas City Chiefs',
    'Colts': 'Indianapolis Colts',
    'Cowboys': 'Dallas Cowboys',
    'Falcons': 'Atlanta Falcons',
    'Giants': 'New York Giants',
    'Jaguars': 'Jacksonville Jaguars',
    'Jets': 'New York Jets',
    'Lions': 'Detroit Lions',
    'Packers': 'Green Bay Packers',
    'Rams': 'Los Angeles Rams',
    'Ravens': 'Baltimore Ravens',
    'Redskins': 'Washington Redskins',
    'Saints': 'New Orleans Saints',
    'Seahawks': 'Seattle Seahawks',
    'Steelers': 'Pittsburgh Steelers',
    'Texans': 'Houston Texans',
    'Titans': 'Tennessee Titans'
}
