## Introduction &middot; [![Build Status](https://travis-ci.org/BenBrostoff/draftfast.svg?branch=master)](https://travis-ci.org/BenBrostoff/draftfast) &middot; [![](https://draftfast.herokuapp.com/badge.svg)](https://draftfast.herokuapp.com/) &middot; [![](https://img.shields.io/badge/patreon-donate-yellow.svg)](https://www.patreon.com/user?u=8965834)

![](marketing/NFL_OPTIMIZED.png)

An incredibly powerful tool that automates and optimizes lineup building, allowing you to enter thousands of lineups in any DraftKings or FanDuel contest in the time it takes you to grab a coffee.

## Installation

Requires Python 3.6.

```bash
pip install draftfast
```

## Usage

Example usage ([you can experiment with these examples in repl.it](https://repl.it/@BenBrostoff/AllWarlikeDemoware)):

```python
from draftfast import rules
from draftfast.optimize import run
from draftfast.orm import Player
from draftfast.csv_parse import salary_download


# Create players
player_pool = [
    Player(name='A1', cost=5500, proj=55, pos='PG'),
    Player(name='A2', cost=5500, proj=55, pos='PG'),
    Player(name='A3', cost=5500, proj=55, pos='SG'),
    Player(name='A4', cost=5500, proj=55, pos='SG'),
    Player(name='A5', cost=5500, proj=55, pos='SF'),
    Player(name='A6', cost=5500, proj=55, pos='SF'),
    Player(name='A7', cost=5500, proj=55, pos='PF'),
    Player(name='A8', cost=5500, proj=55, pos='PF'),
    Player(name='A9', cost=5500, proj=55, pos='C'),
    Player(name='A10', cost=5500, proj=55, pos='C'),
]

roster = run(
    rule_set=rules.DK_NBA_RULE_SET,
    player_pool=player_pool,
)

# Or, alternatively, generate players from a CSV
players = salary_download.generate_players_from_csvs(
  salary_file_location='./salaries.csv',
  game=rules.DRAFT_KINGS,
)

roster = run(
  rule_set=rules.DK_NBA_RULE_SET,
  player_pool=players,
  verbose=True,
)
```

You can see more examples in the [`examples` directory](https://github.com/BenBrostoff/draftfast/tree/master/examples).

## Game Rules

Optimizing for a particular game is as easy as setting the `RuleSet` (see the example above). Game rules in the library are in the table below:

| League       | Site           | Reference  |
| ------------- |:-------------:| :-----:|
| NFL | DraftKings | `DK_NFL_RULE_SET` |
| NFL | FanDuel | `FD_NFL_RULE_SET` |
| NBA | DraftKings | `DK_NBA_RULE_SET` |
| NBA | FanDuel | `FD_NBA_RULE_SET` |
| MLB | DraftKings | `DK_MLB_RULE_SET` |
| MLB | FanDuel | `FD_MLB_RULE_SET` |
| WNBA | DraftKings | `DK_WNBA_RULE_SET` |
| WNBA | FanDuel | `FD_WNBA_RULE_SET` |
| PGA | FanDuel | `FD_PGA_RULE_SET` |
| NASCAR | FanDuel | `FD_NASCAR_RULE_SET` |


Note that you can also tune `draftfast` for any game of your choice even if it's not implemented in the library (PRs welcome!). Using the `RuleSet` class, you can generate your own game rules that specific number of players, salary, etc. Example:

```python
from draftfast import rules

nhl_rules = rules.RuleSet(
    site=rules.DRAFT_KINGS,
    league='NHL',
    roster_size='9',
    position_limits=[['C', 9, 9]],
    salary_max=50_000,
)
```

## CSV Upload

```python
from draftfast.csv_parse import uploaders

uploader = uploaders.DraftKingsNBAUploader(
    pid_file='./pid_file.csv',
)
uploader.write_rosters(rosters)

```

## Support and Consulting

DFS optimization is only one part of a sustainable strategy. Long-term DFS winners have the best: 

- Player projections
- Bankroll management
- Diversification in contests played
- Diversification across lineups (see `draftfast.exposure`)
- Research process
- 1 hour before gametime lineup changes
- ...and so much more

DraftFast provides support and consulting services that can help with all of these. [Let's get in touch today](mailto:ben.brostoff@gmail.com).

# Credits

Special thanks to [swanson](https://github.com/swanson/), who authored [this repo](https://github.com/swanson/degenerate), which was the inspiration for this one.
