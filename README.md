## Introduction &middot; [![Build Status](https://travis-ci.org/BenBrostoff/draft-kings-fun.svg?branch=master)](https://travis-ci.org/BenBrostoff/draft-kings-fun) &middot; [![](https://draftfast.herokuapp.com/badge.svg)](https://draftfast.herokuapp.com/) &middot; [![](https://img.shields.io/badge/patreon-donate-yellow.svg)](https://www.patreon.com/user?u=8965834)

![](marketing/NFL_OPTIMIZED.png)

This is an incredibly powerful tool that can automate lineup building, allowing you to enter thousands of lineups in any DK contest in the time it takes you to grab a coffee. Works for NFL, NBA, WNBA and MLB on either DraftKings or FanDuel.

This project allows you to create an unlimited amount of optimized DraftKings lineups based on any projection source of your choice. You can use this repo as a command line application, or import functionality as needed to build your own scripts to construct thousands of DraftKings lineups each week and upload them in seconds using their [CSV upload tool](https://www.draftkings.com/lineup/upload). Examples of how to do the latter are provided in the `examples` directory.

Special thanks to [swanson](https://github.com/swanson/), who authored [this repo](https://github.com/swanson/degenerate), which mine is heavily based off of.

Pre-reqs:

* Python 3
* `pip install -r requirements.txt`

## Installation

```bash
pip install draftfast
```

## Usage

Example usage ([you can experiment with these examples in repl.it](https://repl.it/@BenBrostoff/AllWarlikeDemoware)):

```python
from draftfast import rules
from draftfast.optimize import beta_run
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

roster = beta_run(
    rule_set=rules.DK_NBA_RULE_SET,
    players=player_pool,
)

# Or, alternatively, generate players from a CSV
players = salary_download.generate_players_from_csvs(
  salary_file_location='./salaries.csv',
  game=rules.DRAFT_KINGS,
)

roster = beta_run(
  rule_set=rules.DK_NBA_RULE_SET,
  players=players,
  verbose=True,
)
```
