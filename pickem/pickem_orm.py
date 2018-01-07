from orm import Player
from terminaltables import AsciiTable

TIER_1 = 'T1'
TIER_2 = 'T2'
TIER_3 = 'T3'
TIER_4 = 'T4'
TIER_5 = 'T5'
TIER_6 = 'T6'

TIERS = [
    TIER_1,
    TIER_2,
    TIER_3,
    TIER_4,
    TIER_5,
    TIER_6,
]


class TieredLineup(object):

    def __init__(self, players):
        assert len(players) == 6, 'Must have six players'
        for idx, p in enumerate(players):
            if p.tier != TIERS[idx]:
                raise Exception(
                    'Player {} is not in tier {} but in tier {}'.format(
                        p.name, TIERS[idx], p.tier
                    )
                )

        self.players = players
        [
            self.TIER_1,
            self.TIER_2,
            self.TIER_3,
            self.TIER_4,
            self.TIER_5,
            self.TIER_6,
        ] = players

    def __repr__(self):
        table_data = [[
            'Name',
            'Tier',
            'Matchup',
            'Projected',
            'vs Avg',
        ]]
        for p in self.players:
            table_data.append(p.to_table_row())
        return (
            AsciiTable(table_data).table +
            '\n' +
            'Total: {}'.format(self.total)
        )

    @property
    def total(self):
        return sum([p.proj for p in self.players])


class TieredPlayer(Player):

    def __init__(self, tier, **kwargs):
        self.tier = tier
        super(TieredPlayer, self).__init__(
            **kwargs
        )

    def to_table_row(self):
        return [
            self.name,
            self.tier,
            self.matchup,
            self.proj,
            self.v_avg,
        ]
