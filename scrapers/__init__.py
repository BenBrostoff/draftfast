from fantasy_pros import scrape as fp_nfl_scrape
from roto_grinders_nfl import scrape as rg_nfl_scrape
from roto_grinders_nba import scrape as rg_nba_scrape
from nfl_fantasy import scrape as nfl_scrape

scrape_dict = {
    'nfl_fanpros': {
        'method': fp_nfl_scrape,
        'readable': 'Fan Pros',
    },
    'nfl_fantasy': {
        'method': nfl_scrape,
        'readable': 'NFL.com',
    },
    'nfl_rotogrinders': {
        'method': rg_nfl_scrape,
        'readable': 'Rotogrinders',
    },
    'nba_rotogrinders': {
        'method': rg_nba_scrape,
        'readable': 'Rotogrinders',
    }
}


def scrape(source):
    return scrape_dict[source]['method']()
