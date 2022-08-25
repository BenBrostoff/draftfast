DRAFT_KINGS = 'DRAFT_KINGS'
FAN_DUEL = 'FAN_DUEL'


ROSTER_SIZE = {
    DRAFT_KINGS: {
        'NFL': 9,
        'NFL_SHOWDOWN': 6,
        'MLB_SHOWDOWN': 6,
        'NBA': 8,
        'NBA_SHOWDOWN': 6,
        'WNBA': 6,
        'MLB': 10,
        'SOCCER': 8,
        'EL': 6,
        'NHL': 9,
        'NHL_SHOWDOWN': 6,
        'XFL': 7,
        'TEN': 6,
        'PGA': 6,
        'PGA_CAPTAIN': 6,
        'CSGO_SHOWDOWN': 6,
        'NASCAR': 6,
        'F1_SHOWDOWN': 6,
    },
    FAN_DUEL: {
        'NFL': 9,
        'NFL_MVP': 5,
        'MLB_MVP': 5,
        'NBA_MVP': 5,
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
        'NFL_SHOWDOWN': 50_000,
        'NBA': 50_000,
        'NBA_SHOWDOWN': 50_000,
        'WNBA': 50_000,
        'MLB': 50_000,
        'SOCCER': 50_000,
        'EL': 50_000,
        'NHL': 50_000,
        'NHL_SHOWDOWN': 50_000,
        'MLB_SHOWDOWN': 50_000,
        'XFL': 50_000,
        'TEN': 50_000,
        'PGA': 50_000,
        'PGA_CAPTAIN': 50_000,
        'CSGO_SHOWDOWN': 50_000,
        'NASCAR': 50_000,
        'F1_SHOWDOWN': 50_000,
    },
    FAN_DUEL: {
        'NFL': 60_000,
        'NFL_MVP': 60_000,
        'MLB_MVP': 35_000,
        'NBA_MVP': 60_000,
        'NBA': 60_000,
        'MLB': 35_000,
        'WNBA': 40_000,
        'NASCAR': 50_000,
        'PGA': 60_000,
    }
}


def get_nfl_positions(
    rb_min=2,
    wr_min=3,
    te_min=1,
    te_upper=2,
    d_abbrev='DST',
):
    return [
        ['QB', 1, 1],
        ['RB', rb_min, 3],
        ['WR', wr_min, 4],
        ['TE', te_min, te_upper],
        [d_abbrev, 1, 1]
    ]


def get_nfl_showdown_positions(dk: bool = False, fd: bool = False) -> list:
    if dk:
        ub = 5
    elif fd:
        ub = 4
    else:
        raise NotImplementedError

    return [
        ['CPT', 1, 1],
        ['FLEX', ub, ub]
    ]


POSITIONS = {
    DRAFT_KINGS: {
        'NBA': [
            ['PG', 1, 3],
            ['SG', 1, 3],
            ['SF', 1, 3],
            ['PF', 1, 3],
            ['C', 1, 2]
        ],
        'NBA_SHOWDOWN': [
            ['CPT', 1, 1],
            ['FLEX', 5, 5],
        ],
        'WNBA': [
            ['PG', 1, 3],
            ['SG', 1, 3],
            ['SF', 1, 4],
            ['PF', 1, 4],
        ],
        'NFL': get_nfl_positions(),
        'NFL_SHOWDOWN': get_nfl_showdown_positions(dk=True),
        'MLB': [
            ['SP', 0, 2],
            ['RP', 0, 2],
            ['C', 1, 1],
            ['1B', 1, 1],
            ['2B', 1, 1],
            ['3B', 1, 1],
            ['SS', 1, 1],
            ['OF', 3, 3],
        ],
        'SOCCER': [
            ['F', 2, 3],
            ['M', 2, 3],
            ['D', 2, 3],
            ['GK', 1, 2],
        ],
        'EL': [
            ['G', 2, 3],
            ['F', 3, 4],
        ],
        'NHL': [
            ['C', 2, 3],
            ['W', 3, 4],
            ['D', 2, 3],
            ['G', 1, 1],
        ],
        'NHL_SHOWDOWN': [
            ['FLEX', 6, 6],
        ],
        'MLB_SHOWDOWN': [
            ['CPT', 1, 1],
            ['FLEX', 5, 5],
        ],
        'XFL': [
            ['QB', 1, 1],
            ['RB', 1, 3],
            ['WR', 2, 4],
            ['DST', 1, 1]
        ],
        'TEN': [
            ['P', 6, 6],
        ],
        'PGA': [
            ['G', 6, 6],
        ],
        'PGA_CAPTAIN': [
            ['CPT', 1, 1],
            ['G', 5, 5],
        ],
        'CSGO_SHOWDOWN': [
            ['CPT', 1, 1],
            ['FLEX', 5, 5],
        ],
        'F1_SHOWDOWN': [
            ['CPT', 1, 1],
            ['D', 4, 4],
            ['CNSTR', 1, 1],
        ],
        'NASCAR': [
            ['D', 6, 6],
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
            ['1B', 1, 2],  # TODO - allow C or 1B
            ['2B', 1, 2],
            ['3B', 1, 2],
            ['SS', 1, 2],
            ['OF', 3, 4],
        ],
        'MLB_MVP': [
            ['MVP', 1, 1],
            ['STAR', 1, 1],
            ['UTIL', 3, 3],
        ],
        'NBA_MVP': [
            ['MVP', 1, 1],
            ['STAR', 1, 1],
            ['PRO', 1, 1],
            ['UTIL', 2, 2],
        ],
        'WNBA': [
            ['G', 3, 3],
            ['F', 4, 4],
        ],
        'NFL': get_nfl_positions(d_abbrev='D'),
        'NFL_MVP': get_nfl_showdown_positions(fd=True),
        'NASCAR': [
            ['D', 5, 5],
        ],
        'PGA': [
            ['G', 6, 6],
        ],
    }
}

NBA_GENERAL_POSITIONS = [
    ['G', 3, 4],
    ['F', 3, 4],
    ['C', 1, 2],
]
MLB_GENERAL_POSITIONS = [
    ['P', 2, 2],
]
WNBA_GENERAL_POSITIONS = [
    ['G', 2, 3],
    ['F', 3, 4],
]


class RuleSet(object):
    def __init__(self, site, league,
                 roster_size, position_limits,
                 salary_max, salary_min=0,
                 general_position_limits=None,
                 offensive_positions=None, defensive_positions=None,
                 max_players_per_team=None,
                 min_teams=None,
                 position_per_team_rules=None,
                 game_type='classic'):
        self.site = site
        self.league = league
        self.roster_size = roster_size
        self.position_limits = position_limits
        self.general_position_limits = general_position_limits
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.offensive_positions = offensive_positions
        self.defensive_positions = defensive_positions
        self.game_type = game_type
        self.max_players_per_team = max_players_per_team or (roster_size - 1)
        self.position_per_team_rules = position_per_team_rules
        self.min_teams = min_teams


DK_NBA_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='NBA',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['NBA'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['NBA'],
    position_limits=POSITIONS[DRAFT_KINGS]['NBA'],
    general_position_limits=NBA_GENERAL_POSITIONS,
)

DK_NBA_SHOWDOWN_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='NBA_SHOWDOWN',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['NBA_SHOWDOWN'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['NBA_SHOWDOWN'],
    position_limits=POSITIONS[DRAFT_KINGS]['NBA_SHOWDOWN'],
    game_type='showdown',
    general_position_limits=[],
)

FD_NBA_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league='NBA',
    roster_size=ROSTER_SIZE[FAN_DUEL]['NBA'],
    salary_max=SALARY_CAP[FAN_DUEL]['NBA'],
    position_limits=POSITIONS[FAN_DUEL]['NBA'],
    general_position_limits=NBA_GENERAL_POSITIONS,
)

DK_WNBA_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='WNBA',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['WNBA'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['WNBA'],
    position_limits=POSITIONS[DRAFT_KINGS]['WNBA'],
    general_position_limits=NBA_GENERAL_POSITIONS,
)

FD_WNBA_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league='WNBA',
    roster_size=ROSTER_SIZE[FAN_DUEL]['WNBA'],
    salary_max=SALARY_CAP[FAN_DUEL]['WNBA'],
    position_limits=POSITIONS[FAN_DUEL]['WNBA'],
    general_position_limits=NBA_GENERAL_POSITIONS,
)

DK_NFL_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='NFL',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['NFL'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['NFL'],
    position_limits=POSITIONS[DRAFT_KINGS]['NFL'],
    offensive_positions=['QB', 'RB', 'WR', 'TE'],
    defensive_positions=['DST'],
    general_position_limits=[],
)

FD_NFL_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league='NFL',
    roster_size=ROSTER_SIZE[FAN_DUEL]['NFL'],
    salary_max=SALARY_CAP[FAN_DUEL]['NFL'],
    position_limits=POSITIONS[FAN_DUEL]['NFL'],
    offensive_positions=['QB', 'RB', 'WR', 'TE'],
    defensive_positions=['D'],
    general_position_limits=[],
)

DK_NFL_SHOWDOWN_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='NFL_SHOWDOWN',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['NFL_SHOWDOWN'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['NFL_SHOWDOWN'],
    position_limits=POSITIONS[DRAFT_KINGS]['NFL_SHOWDOWN'],
    offensive_positions=['CPT'],
    defensive_positions=['DST'],
    general_position_limits=[],
    game_type='showdown',
)

FD_NFL_MVP_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league='NFL_MVP',
    roster_size=ROSTER_SIZE[FAN_DUEL]['NFL_MVP'],
    salary_max=SALARY_CAP[FAN_DUEL]['NFL_MVP'],
    position_limits=POSITIONS[FAN_DUEL]['NFL_MVP'],
    offensive_positions=['CPT'],
    defensive_positions=['D'],
    general_position_limits=[],
    game_type='showdown',
)

FD_MLB_MVP_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league='MLB_MVP',
    roster_size=ROSTER_SIZE[FAN_DUEL]['MLB_MVP'],
    salary_max=SALARY_CAP[FAN_DUEL]['MLB_MVP'],
    position_limits=POSITIONS[FAN_DUEL]['MLB_MVP'],
    general_position_limits=[],
    game_type='showdown',
)

FD_NBA_MVP_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league='NBA_MVP',
    roster_size=ROSTER_SIZE[FAN_DUEL]['NBA_MVP'],
    salary_max=SALARY_CAP[FAN_DUEL]['NBA_MVP'],
    position_limits=POSITIONS[FAN_DUEL]['NBA_MVP'],
    general_position_limits=[],
    game_type='showdown',
)

FD_PGA_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league='PGA',
    roster_size=ROSTER_SIZE[FAN_DUEL]['PGA'],
    salary_max=SALARY_CAP[FAN_DUEL]['PGA'],
    position_limits=POSITIONS[FAN_DUEL]['PGA'],
    general_position_limits=[],
)

DK_PGA_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='PGA',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['PGA'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['PGA'],
    position_limits=POSITIONS[DRAFT_KINGS]['PGA'],
    general_position_limits=[],
)

DK_PGA_SHOWDOWN_CAPTAIN_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='PGA_CAPTAIN',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['PGA_CAPTAIN'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['PGA_CAPTAIN'],
    position_limits=POSITIONS[DRAFT_KINGS]['PGA_CAPTAIN'],
    general_position_limits=[],
    game_type='showdown',
)

FD_NASCAR_RULE_SET = RuleSet(
    site=FAN_DUEL,
    min_teams=1,
    league='NASCAR',
    roster_size=ROSTER_SIZE[FAN_DUEL]['NASCAR'],
    salary_max=SALARY_CAP[FAN_DUEL]['NASCAR'],
    position_limits=POSITIONS[FAN_DUEL]['NASCAR'],
    general_position_limits=[],
)

DK_NASCAR_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    min_teams=1,
    league='NASCAR',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['NASCAR'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['NASCAR'],
    position_limits=POSITIONS[DRAFT_KINGS]['NASCAR'],
    general_position_limits=[],
)

DK_MLB_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='MLB',
    # Can start two pitchers and 5 hitters
    max_players_per_team=7,
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['MLB'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['MLB'],
    position_limits=POSITIONS[DRAFT_KINGS]['MLB'],
    general_position_limits=MLB_GENERAL_POSITIONS,
    min_teams=3,
    position_per_team_rules=[[lambda pos: 'P' not in pos, 5]],
)

FD_MLB_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league='MLB',
    roster_size=ROSTER_SIZE[FAN_DUEL]['MLB'],
    salary_max=SALARY_CAP[FAN_DUEL]['MLB'],
    position_limits=POSITIONS[FAN_DUEL]['MLB'],
    general_position_limits=[],
)

DK_SOCCER_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='SOCCER',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['SOCCER'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['SOCCER'],
    position_limits=POSITIONS[DRAFT_KINGS]['SOCCER'],
    offensive_positions=['M', 'F'],
    defensive_positions=['GK', 'D'],
    general_position_limits=[],
)

DK_EURO_LEAGUE_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='EL',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['EL'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['EL'],
    position_limits=POSITIONS[DRAFT_KINGS]['EL'],
    general_position_limits=[],
)

DK_NHL_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='NHL',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['NHL'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['NHL'],
    position_limits=POSITIONS[DRAFT_KINGS]['NHL'],
    offensive_positions=['C', 'W'],
    defensive_positions=['G', 'D'],
    general_position_limits=[],
)

DK_NHL_SHOWDOWN_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='NHL_SHOWDOWN',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['NHL_SHOWDOWN'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['NHL_SHOWDOWN'],
    position_limits=POSITIONS[DRAFT_KINGS]['NHL_SHOWDOWN'],
    offensive_positions=['C', 'W'],
    defensive_positions=['G', 'D'],
    general_position_limits=[],
    game_type='showdown',
)

DK_NBA_PICKEM_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='NBA',
    roster_size=6,
    salary_max=None,
    position_limits=None,
    game_type='pickem',
)

DK_MLB_SHOWDOWN_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='MLB_SHOWDOWN',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['MLB_SHOWDOWN'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['MLB_SHOWDOWN'],
    position_limits=POSITIONS[DRAFT_KINGS]['MLB_SHOWDOWN'],
    general_position_limits=[],
    game_type='showdown'
)


DK_XFL_CLASSIC_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='XFL',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['XFL'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['XFL'],
    position_limits=POSITIONS[DRAFT_KINGS]['XFL'],
    general_position_limits=[],
)


DK_TEN_CLASSIC_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league='TEN',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['TEN'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['TEN'],
    position_limits=POSITIONS[DRAFT_KINGS]['TEN'],
    general_position_limits=[],
)

DK_CSGO_SHOWDOWN = RuleSet(
    site=DRAFT_KINGS,
    league='CSGO_SHOWDOWN',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['CSGO_SHOWDOWN'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['CSGO_SHOWDOWN'],
    position_limits=POSITIONS[DRAFT_KINGS]['CSGO_SHOWDOWN'],
    game_type='showdown',
    general_position_limits=[],
    max_players_per_team=3,
)

DK_F1_SHOWDOWN = RuleSet(
    site=DRAFT_KINGS,
    league='F1_SHOWDOWN',
    roster_size=ROSTER_SIZE[DRAFT_KINGS]['F1_SHOWDOWN'],
    salary_max=SALARY_CAP[DRAFT_KINGS]['F1_SHOWDOWN'],
    position_limits=POSITIONS[DRAFT_KINGS]['F1_SHOWDOWN'],
    game_type='showdown',
    general_position_limits=[],
    max_players_per_team=2,
)
