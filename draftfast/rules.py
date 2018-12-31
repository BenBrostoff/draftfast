DRAFT_KINGS = 'DRAFT_KINGS'
FAN_DUEL = 'FAN_DUEL'


ROSTER_SIZE = {
    DRAFT_KINGS: {
        'NFL': 9,
        'NBA': 8,
        'WNBA': 6,
        'MLB': 10,
        'SOCCER': 8,
        'EL': 6,
        'NHL': 9,
    },
    FAN_DUEL: {
        'NFL': 9,
        'NBA': 9,
        'MLB': 9,
        'WNBA': 7,
        'NASCAR': 5,
        'PGA': 6,
    }
}


SALARY_CAP = {
    DRAFT_KINGS: {
        'NFL': 50_000,
        'NBA': 50_000,
        'WNBA': 50_000,
        'MLB': 50_000,
        'SOCCER': 50_000,
        'EL': 50_000,
        'NHL': 50_000,
    },
    FAN_DUEL: {
        'NFL': 60_000,
        'NBA': 60_000,
        'MLB': 35_000,
        'WNBA': 40_000,
        'NASCAR': 50_000,
        'PGA': 60_000,
    }
}


def get_nfl_positions(
    d_abbrev='DST',
):
    return [
        ['QB', 1, 1],
        ['RB', 2, 2],
        ['WR', 3, 3],
        ['TE', 1, 1],
        ['FLEX', 1, 1]  # RB, WR, TE
        [d_abbrev, 1, 1]
    ]


POSITIONS = {
    DRAFT_KINGS: {
        'NBA': [
            ['PG', 1, 1],
            ['SG', 1, 1],
            ['SF', 1, 1],
            ['PF', 1, 1],
            ['C', 1, 1],
            ['G', 1, 1],
            ['F', 1, 1],
            ['UTIL', 1, 1]  # any
        ],
        'WNBA': [
            ['G', 2, 2],
            ['F', 3, 3],
            ['UTIL', 1, 1]  # G, F
        ],
        'NFL': get_nfl_positions(),
        'MLB': [
            ['SP', 2, 2],
            ['C', 1, 1],
            ['1B', 1, 1],
            ['2B', 1, 1],
            ['3B', 1, 1],
            ['SS', 1, 1],
            ['OF', 3, 3],
        ],
        'SOCCER': [
            ['F', 2, 2],
            ['M', 2, 2],
            ['D', 2, 2],
            ['GK', 1, 1],
            ['UTIL', 1, 1]  # D, M, F
        ],
        'EL': [
            ['G', 2, 2],
            ['F', 3, 3],    # F, C
            ['UTIL', 1, 1]  # G, F, C
        ],
        'NHL': [
            ['C', 2, 2],
            ['W', 3, 3],    # LW, RW
            ['D', 2, 2],
            ['G', 1, 1],
            ['UTIL', 1, 1]  # LW, RW, C, D
        ]
    },
    FAN_DUEL: {
        'NBA': [
            ['PG', 2, 2],
            ['SG', 2, 2],
            ['SF', 2, 2],
            ['PF', 2, 2],
            ['C', 1, 1],
        ],
        'MLB': [
            ['P', 1, 1],
            ['1B', 1, 1],  # C, 1B
            ['2B', 1, 1],
            ['3B', 1, 1],
            ['SS', 1, 1],
            ['OF', 3, 3],
            ['UTIL', 1, 1]  # any
        ],
        'WNBA': [
            ['G', 3, 3],
            ['F', 4, 4],
        ],
        'NFL': get_nfl_positions(d_abbrev='D'),
        'NASCAR': [
            ['D', 5, 5],
        ],
        'PGA': [
            ['G', 6, 6],
        ],
    }
}


FLEX_POSITIONS = {
    DRAFT_KINGS: {
        'NBA': {
            'G': ('PG', 'SG'),
            'F': ('PG', 'SG', 'SF', 'PF'),
            'UTIL': ('PG', 'SG', 'SF', 'PF', 'C')
        },
        'WNBA': {
            'UTIL': ('G', 'F')
        },
        'NFL': {
            'FLEX': ('RB', 'WR', 'TE')
        },
        'SOCCER': {
            'UTIL': ('D', 'M', 'F')
        },
        'EL': {
            'F': ('F', 'C'),
            'UTIL': ('G', 'F', 'C')
        },
        'NHL': {
            'W': ('LW', 'RW'),
            'UTIL': ('LW', 'RW', 'C', 'D')
        }
    },
    FAN_DUEL: {
        'MLB': {
            '1B', ('C', '1B'),
            'UTIL': ('P', 'C', '1B', '2B', '3B', 'SS', 'OF')
        },
        'NFL': {
            'FLEX': ('RB', 'WR', 'TE')
        }
    }
}

class RuleSet(object):

    def __init__(self, site, league,
                 roster_size, position_limits,
                 flex_positions_allowed=None,
                 salary_max, salary_min=0,
                 general_position_limits=None,
                 offensive_positions=None,
                 defensive_positions=None,
                 game_type='classic'):
        self.site = site
        self.league = league
        self.roster_size = roster_size
        self.position_limits = position_limits
        self.flex_positions_allowed = flex_positions_allowed
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.offensive_positions = offensive_positions
        self.defensive_positions = defensive_positions
        self.game_type = game_type


DK_NBA_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='NBA',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['NBA'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['NBA'],
    position_limits=POSITIONS[DRAFT_KINGS]['NBA'],
    flex_positions_allowed=FLEX_POSITIONS[DRAFT_KINGS]['NBA'],
)

FD_NBA_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league='NBA',
    roster_size=ROSTER_SIZE[FAN_DUEL]['NBA'],
    salary_max=SALARY_CAP[FAN_DUEL]['NBA'],
    position_limits=POSITIONS[FAN_DUEL]['NBA'],
    flex_positions_allowed=FLEX_POSITIONS[FAN_DUEL]['NBA'],
)

DK_WNBA_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='WNBA',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['WNBA'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['WNBA'],
    position_limits=POSITIONS[DRAFT_KINGS]['WNBA'],
    flex_positions_allowed=FLEX_POSITIONS[DRAFT_KINGS]['WNBA'],
)

FD_WNBA_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league='WNBA',
    roster_size=ROSTER_SIZE[FAN_DUEL]['WNBA'],
    salary_max=SALARY_CAP[FAN_DUEL]['WNBA'],
    position_limits=POSITIONS[FAN_DUEL]['WNBA'],
    flex_positions_allowed=FLEX_POSITIONS[FAN_DUEL]['WNBA'],
)

DK_NFL_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='NFL',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['NFL'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['NFL'],
    position_limits=POSITIONS[DRAFT_KINGS]['NFL'],
    flex_positions_allowed=FLEX_POSITIONS[DRAFT_KINGS]['NFL'],
    offensive_positions=['QB', 'RB', 'WR', 'TE'],
    defensive_positions=['DST'],
)

FD_NFL_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league='NFL',
    roster_size=ROSTER_SIZE[FAN_DUEL]['NFL'],
    salary_max=SALARY_CAP[FAN_DUEL]['NFL'],
    flex_positions_allowed=FLEX_POSITIONS[FAN_DUEL]['NFL'],
    offensive_positions=['QB', 'RB', 'WR', 'TE'],
    defensive_positions=['D'],
)

FD_PGA_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league='PGA',
    roster_size=ROSTER_SIZE[FAN_DUEL]['PGA'],
    salary_max=SALARY_CAP[FAN_DUEL]['PGA'],
    position_limits=POSITIONS[FAN_DUEL]['PGA'],
)

FD_NASCAR_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league='NASCAR',
    roster_size=ROSTER_SIZE[FAN_DUEL]['NASCAR'],
    salary_max=SALARY_CAP[FAN_DUEL]['NASCAR'],
    position_limits=POSITIONS[FAN_DUEL]['NASCAR'],
)

DK_MLB_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='MLB',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['MLB'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['MLB'],
    position_limits=POSITIONS[DRAFT_KINGS]['MLB'],
    flex_positions_allowed=FLEX_POSITIONS[DRAFT_KINGS]['MLB'],
)

FD_MLB_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league='MLB',
    roster_size=ROSTER_SIZE[FAN_DUEL]['MLB'],
    salary_max=SALARY_CAP[FAN_DUEL]['MLB'],
    position_limits=POSITIONS[FAN_DUEL]['MLB'],
    flex_positions_allowed=FLEX_POSITIONS[FAN_DUEL]['MLB'],
)

DK_SOCCER_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='SOCCER',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['SOCCER'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['SOCCER'],
    position_limits=POSITIONS[DRAFT_KINGS]['SOCCER'],
    offensive_positions=['M', 'F'],
    defensive_positions=['GK', 'D'],
    flex_positions_allowed=FLEX_POSITIONS[DRAFT_KINGS]['SOCCER'],
)

DK_EURO_LEAGUE_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='EL',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['EL'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['EL'],
    position_limits=POSITIONS[DRAFT_KINGS]['EL'],
    flex_positions_allowed=FLEX_POSITIONS[DRAFT_KINGS]['EL'],
)

DK_NHL_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='NHL',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['NHL'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['NHL'],
    position_limits=POSITIONS[DRAFT_KINGS]['NHL'],
    offensive_positions=['C', 'W'],
    defensive_positions=['G', 'D'],
    flex_positions_allowed=FLEX_POSITIONS[DRAFT_KINGS]['NHL'],
)

DK_NBA_PICKEM_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='NBA',
    roster_size=6,
    salary_max=None,
    position_limits=None,
    game_type='pickem',
)
