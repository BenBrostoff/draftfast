from draftfast.constants.positions import (
    MLB_GENERAL_POSITIONS,
    NBA_GENERAL_POSITIONS,
    POSITIONS_BY_SITE_BY_LEAGUE,
)
from draftfast.settings import CustomRule
from draftfast.constants.roster_size import ROSTER_SIZE_BY_SITE_BY_SPORT
from draftfast.constants.salary_cap import SALARY_CAP_BY_SITE_BY_LEAGUE


DRAFT_KINGS = "DRAFT_KINGS"
FAN_DUEL = "FAN_DUEL"


class RuleSet(object):
    def __init__(
        self,
        site,
        league,
        roster_size,
        position_limits,
        salary_max,
        salary_min=0,
        general_position_limits=None,
        offensive_positions=None,
        defensive_positions=None,
        max_players_per_team=None,
        min_teams=None,
        min_matchups=None,
        position_per_team_rules=None,
        custom_rules=None,
        game_type="classic",
    ):
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
        self.min_matchups = min_matchups
        self.custom_rules = custom_rules

    def __eq__(self, other):
        if not other:
            return False

        return (
            self.site == other.site
            and self.league == other.league
            and self.game_type == other.game_type
        )


DK_NBA_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league="NBA",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["NBA"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["NBA"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["NBA"],
    general_position_limits=NBA_GENERAL_POSITIONS,
    min_matchups=2,
)

DK_NBA_SHOWDOWN_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league="NBA_SHOWDOWN",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["NBA_SHOWDOWN"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["NBA_SHOWDOWN"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["NBA_SHOWDOWN"],
    game_type="showdown",
    general_position_limits=[],
)

FD_NBA_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league="NBA",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[FAN_DUEL]["NBA"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[FAN_DUEL]["NBA"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[FAN_DUEL]["NBA"],
    general_position_limits=NBA_GENERAL_POSITIONS,
)

DK_WNBA_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league="WNBA",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["WNBA"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["WNBA"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["WNBA"],
    general_position_limits=NBA_GENERAL_POSITIONS,
    min_matchups=2,
)

FD_WNBA_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league="WNBA",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[FAN_DUEL]["WNBA"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[FAN_DUEL]["WNBA"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[FAN_DUEL]["WNBA"],
    general_position_limits=NBA_GENERAL_POSITIONS,
)

DK_NFL_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league="NFL",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["NFL"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["NFL"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["NFL"],
    offensive_positions=["QB", "RB", "WR", "TE"],
    defensive_positions=["DST"],
    general_position_limits=[],
    min_matchups=2,
)

FD_NFL_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league="NFL",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[FAN_DUEL]["NFL"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[FAN_DUEL]["NFL"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[FAN_DUEL]["NFL"],
    offensive_positions=["QB", "RB", "WR", "TE"],
    defensive_positions=["D"],
    general_position_limits=[],
)

DK_NFL_SHOWDOWN_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league="NFL_SHOWDOWN",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["NFL_SHOWDOWN"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["NFL_SHOWDOWN"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["NFL_SHOWDOWN"],
    offensive_positions=["CPT"],
    defensive_positions=["DST"],
    general_position_limits=[],
    game_type="showdown",
)

FD_NFL_MVP_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league="NFL_MVP",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[FAN_DUEL]["NFL_MVP"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[FAN_DUEL]["NFL_MVP"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[FAN_DUEL]["NFL_MVP"],
    offensive_positions=["CPT"],
    defensive_positions=["D"],
    general_position_limits=[],
    game_type="showdown",
)

FD_MLB_MVP_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league="MLB_MVP",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[FAN_DUEL]["MLB_MVP"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[FAN_DUEL]["MLB_MVP"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[FAN_DUEL]["MLB_MVP"],
    general_position_limits=[],
    game_type="showdown",
)

FD_NBA_MVP_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league="NBA_MVP",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[FAN_DUEL]["NBA_MVP"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[FAN_DUEL]["NBA_MVP"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[FAN_DUEL]["NBA_MVP"],
    general_position_limits=[],
    game_type="showdown",
)

FD_PGA_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league="PGA",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[FAN_DUEL]["PGA"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[FAN_DUEL]["PGA"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[FAN_DUEL]["PGA"],
    general_position_limits=[],
)

DK_PGA_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league="PGA",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["PGA"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["PGA"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["PGA"],
    general_position_limits=[],
)

DK_PGA_SHOWDOWN_CAPTAIN_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league="PGA_CAPTAIN",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["PGA_CAPTAIN"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["PGA_CAPTAIN"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["PGA_CAPTAIN"],
    general_position_limits=[],
    game_type="showdown",
)

FD_NASCAR_RULE_SET = RuleSet(
    site=FAN_DUEL,
    min_teams=1,
    league="NASCAR",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[FAN_DUEL]["NASCAR"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[FAN_DUEL]["NASCAR"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[FAN_DUEL]["NASCAR"],
    general_position_limits=[],
)

DK_NASCAR_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    min_teams=1,
    league="NASCAR",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["NASCAR"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["NASCAR"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["NASCAR"],
    general_position_limits=[],
)

DK_MLB_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league="MLB",
    # Can start two pitchers and 5 hitters
    max_players_per_team=7,
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["MLB"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["MLB"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["MLB"],
    general_position_limits=MLB_GENERAL_POSITIONS,
    min_matchups=2,
    position_per_team_rules=[[lambda pos: "P" not in pos, 5]],
)

FD_MLB_RULE_SET = RuleSet(
    site=FAN_DUEL,
    league="MLB",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[FAN_DUEL]["MLB"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[FAN_DUEL]["MLB"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[FAN_DUEL]["MLB"],
    min_teams=3,
    general_position_limits=[],

    # "Up to five players from same team, provided one is a pitcher."
    # Rules below take 5 and subtract the pitcher to end up in same place.
    # Ref:
    # https://support.fanduel.com/s/article/How-many-players-can-I-select-from-one-team
    position_per_team_rules=[
        [lambda pos: "P" not in pos, 4],
    ],

    # Handle C/1B minimums,
    custom_rules=[
        CustomRule(
            group_a=lambda p: p.pos in ['C', '1B'],
            group_b=lambda p: p,
            comparison=lambda sum, a, b: sum(a) == 1,
        )
    ]
)

DK_SOCCER_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league="SOCCER",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["SOCCER"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["SOCCER"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["SOCCER"],
    offensive_positions=["M", "F"],
    defensive_positions=["GK", "D"],
    general_position_limits=[],
)

DK_EURO_LEAGUE_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league="EL",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["EL"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["EL"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["EL"],
    general_position_limits=[],
)

DK_NHL_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league="NHL",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["NHL"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["NHL"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["NHL"],
    offensive_positions=["C", "W"],
    defensive_positions=["G", "D"],
    min_matchups=2,
    # Note min teams restriction is only for non-skaters,
    # and this logic is handled in Optimizer
    min_teams=3,
    general_position_limits=[],
)

DK_NHL_SHOWDOWN_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league="NHL_SHOWDOWN",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["NHL_SHOWDOWN"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["NHL_SHOWDOWN"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["NHL_SHOWDOWN"],
    offensive_positions=["C", "W"],
    defensive_positions=["G", "D"],
    general_position_limits=[],
    game_type="showdown",
)

DK_NBA_PICKEM_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league="NBA",
    roster_size=6,
    salary_max=None,
    position_limits=None,
    game_type="pickem",
)

DK_MLB_SHOWDOWN_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league="MLB_SHOWDOWN",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["MLB_SHOWDOWN"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["MLB_SHOWDOWN"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["MLB_SHOWDOWN"],
    general_position_limits=[],
    game_type="showdown",
)


DK_XFL_CLASSIC_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league="XFL",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["XFL"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["XFL"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["XFL"],
    general_position_limits=[],
)


DK_TEN_CLASSIC_RULE_SET = RuleSet(
    site=DRAFT_KINGS,
    league="TEN",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["TEN"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["TEN"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["TEN"],
    general_position_limits=[],
)

DK_CSGO_SHOWDOWN = RuleSet(
    site=DRAFT_KINGS,
    league="CSGO_SHOWDOWN",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["CSGO_SHOWDOWN"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["CSGO_SHOWDOWN"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["CSGO_SHOWDOWN"],
    game_type="showdown",
    general_position_limits=[],
    max_players_per_team=3,
)

DK_F1_SHOWDOWN = RuleSet(
    site=DRAFT_KINGS,
    league="F1_SHOWDOWN",
    roster_size=ROSTER_SIZE_BY_SITE_BY_SPORT[DRAFT_KINGS]["F1_SHOWDOWN"],
    salary_max=SALARY_CAP_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["F1_SHOWDOWN"],
    position_limits=POSITIONS_BY_SITE_BY_LEAGUE[DRAFT_KINGS]["F1_SHOWDOWN"],
    game_type="showdown",
    general_position_limits=[],
    max_players_per_team=2,
)
