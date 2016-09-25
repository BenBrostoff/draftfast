from fantasy_pros import scrape as fp_scrape
from roto_grinders import scrape as rg_scrape
from nfl_fantasy import scrape as nfl_scrape

def scrape_all():
    for key, val in scrape_dict:
        if key != 'all':
            val()

scrape_dict = {
    'fanpros': fp_scrape,
    'rotogrinders': rg_scrape,
    'nfl_fantasy': nfl_scrape,
    'all': scrape_all
}

def scrape(source):
    return scrape_dict[source]()
