from draftfast.rules_utils import get_nfl_positions, get_nfl_showdown_positions


POSITIONS_BY_SITE_BY_LEAGUE = {
    "DRAFT_KINGS": {
        "NBA": [
            ["PG", 1, 3],
            ["SG", 1, 3],
            ["SF", 1, 3],
            ["PF", 1, 3],
            ["C", 1, 2],
        ],
        "NBA_SHOWDOWN": [
            ["CPT", 1, 1],
            ["FLEX", 5, 5],
        ],
        "WNBA": [
            ["PG", 1, 3],
            ["SG", 1, 3],
            ["SF", 1, 4],
            ["PF", 1, 4],
        ],
        "NFL": get_nfl_positions(),
        "NFL_SHOWDOWN": get_nfl_showdown_positions(dk=True),
        "MLB": [
            ["SP", 0, 2],
            ["RP", 0, 2],
            ["C", 1, 1],
            ["1B", 1, 1],
            ["2B", 1, 1],
            ["3B", 1, 1],
            ["SS", 1, 1],
            ["OF", 3, 3],
        ],
        "SOCCER": [
            ["F", 2, 3],
            ["M", 2, 3],
            ["D", 2, 3],
            ["GK", 1, 2],
        ],
        "EL": [
            ["G", 2, 3],
            ["F", 3, 4],
        ],
        "NHL": [
            ["C", 2, 3],
            ["W", 3, 4],
            ["D", 2, 3],
            ["G", 1, 1],
        ],
        "NHL_SHOWDOWN": [
            ["FLEX", 6, 6],
        ],
        "MLB_SHOWDOWN": [
            ["CPT", 1, 1],
            ["FLEX", 5, 5],
        ],
        "XFL": [["QB", 1, 1], ["RB", 1, 3], ["WR", 2, 4], ["DST", 1, 1]],
        "TEN": [
            ["P", 6, 6],
        ],
        "PGA": [
            ["G", 6, 6],
        ],
        "PGA_CAPTAIN": [
            ["CPT", 1, 1],
            ["G", 5, 5],
        ],
        "CSGO_SHOWDOWN": [
            ["CPT", 1, 1],
            ["FLEX", 5, 5],
        ],
        "F1_SHOWDOWN": [
            ["CPT", 1, 1],
            ["D", 4, 4],
            ["CNSTR", 1, 1],
        ],
        "NASCAR": [
            ["D", 6, 6],
        ],
    },
    "FAN_DUEL": {
        "NBA": [
            ["PG", 2, 2],
            ["SG", 2, 2],
            ["SF", 2, 2],
            ["PF", 2, 2],
            ["C", 1, 1],
        ],
        "MLB": [
            ["P", 1, 1],
            ["C", 0, 1],
            ["1B", 0, 1],
            ["2B", 1, 2],
            ["3B", 1, 2],
            ["SS", 1, 2],
            ["OF", 3, 4],
        ],
        "MLB_MVP": [
            ["MVP", 1, 1],
            ["STAR", 1, 1],
            ["UTIL", 3, 3],
        ],
        "NBA_MVP": [
            ["MVP", 1, 1],
            ["STAR", 1, 1],
            ["PRO", 1, 1],
            ["UTIL", 2, 2],
        ],
        "WNBA": [
            ["G", 3, 3],
            ["F", 4, 4],
        ],
        "NFL": get_nfl_positions(d_abbrev="D"),
        "NFL_MVP": get_nfl_showdown_positions(fd=True),
        "NASCAR": [
            ["D", 5, 5],
        ],
        "PGA": [
            ["G", 6, 6],
        ],
    },
}

NBA_GENERAL_POSITIONS = [
    ["G", 3, 4],
    ["F", 3, 4],
    ["C", 1, 2],
]

MLB_GENERAL_POSITIONS = [
    ["P", 2, 2],
]

WNBA_GENERAL_POSITIONS = [
    ["G", 2, 3],
    ["F", 3, 4],
]
