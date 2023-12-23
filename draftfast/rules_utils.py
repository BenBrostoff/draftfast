def get_nfl_positions(
    rb_min=2,
    wr_min=3,
    te_min=1,
    te_upper=2,
    d_abbrev="DST",
):
    return [
        ["QB", 1, 1],
        ["RB", rb_min, 3],
        ["WR", wr_min, 4],
        ["TE", te_min, te_upper],
        [d_abbrev, 1, 1],
    ]


def get_nfl_showdown_positions(dk: bool = False, fd: bool = False) -> list:
    if dk:
        ub = 5
    elif fd:
        ub = 4
    else:
        raise NotImplementedError

    return [["CPT", 1, 1], ["FLEX", ub, ub]]
