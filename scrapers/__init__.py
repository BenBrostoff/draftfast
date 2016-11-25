from fantasy_pros import scrape as fp_nfl_scrape
from roto_grinders_nfl import scrape as rg_nfl_scrape
from roto_grinders_nba import scrape as rg_nba_scrape
from nfl_fantasy import scrape as nfl_scrape

scrape_dict = {
    'nfl_fanpros': fp_nfl_scrape,
    'nfl_fantasy': nfl_scrape,
    'nfl_rotogrinders': rg_nfl_scrape,
    'nba_rotogrinders': rg_nba_scrape
}


def scrape(source):
    return scrape_dict[source]()
