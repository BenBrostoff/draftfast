ALL_POS = ['QB', 'RB', 'WR', 'TE', 'DST']
ALL_POS_TEAM = ['QB', 'RB1', 'RB2',
                'WR1', 'WR2', 'WR3', 'FLEX',
                'TE', 'DST']

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

POSITION_LIMITS_WR_MAX = [
  ["QB", 1],
  ["RB", 2],
  ["WR", 4],
  ["TE", 1],
  ["DST",  1]
]


POSITION_LIMITS_QB_MAX = [
  ["QB", 2],
  ["RB", 2],
  ["WR", 3],
  ["TE", 1],
  ["DST",  1]
]

POSITION_LIMITS_RB_MAX = [
  ["QB", 2],
  ["RB", 3],
  ["WR", 3],
  ["TE", 1],
  ["DST",  1]
]

POSITION_LIMITS_TE_MAX = [
  ["QB", 2],
  ["RB", 2],
  ["WR", 3],
  ["TE", 2],
  ["DST",  1]
]

POSITION_LIMITS_DST_MAX = [
  ["QB", 2],
  ["RB", 2],
  ["WR", 3],
  ["TE", 1],
  ["DST",  2]
]

ALL_LINEUPS = [
    POSITION_LIMITS_WR_MAX,
    POSITION_LIMITS_QB_MAX,
    POSITION_LIMITS_RB_MAX,
    POSITION_LIMITS_TE_MAX,
    POSITION_LIMITS_DST_MAX
]