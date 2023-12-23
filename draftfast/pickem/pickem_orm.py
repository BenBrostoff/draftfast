from draftfast.orm import Player
from terminaltables import AsciiTable

T1 = "T1"
T2 = "T2"
T3 = "T3"
T4 = "T4"
T5 = "T5"
T6 = "T6"

TIERS = [
    T1,
    T2,
    T3,
    T4,
    T5,
    T6,
]


class TieredLineup(object):
    def __init__(self, players):
        assert len(players) == 6, "Must have six players"
        for idx, p in enumerate(players):
            if p.tier != TIERS[idx]:
                raise Exception(
                    "Player {} is not in tier {} but in tier {}".format(
                        p.name, TIERS[idx], p.tier
                    )
                )

        [
            self.T1,
            self.T2,
            self.T3,
            self.T4,
            self.T5,
            self.T6,
        ] = players

    def __repr__(self):
        table_data = [
            [
                "Name",
                "Tier",
                "Matchup",
                "Projected",
                "vs Avg",
                "Locked",
            ]
        ]
        for p in self.players:
            table_data.append(p.to_table_row())
        return (
            AsciiTable(table_data).table
            + "\n"
            + "Total: {}".format(self.total)
        )

    @property
    def players(self):
        return [
            self.T1,
            self.T2,
            self.T3,
            self.T4,
            self.T5,
            self.T6,
        ]

    @property
    def total(self):
        return sum([p.proj for p in self.players])


class TieredPlayer(Player):
    def __init__(self, tier, **kwargs):
        self.tier = tier
        super(TieredPlayer, self).__init__(**kwargs)

    def to_table_row(self):
        return [
            self.name,
            self.tier,
            self.matchup,
            self.proj,
            self.v_avg,
            "LOCK" if self.lock else "",
        ]
