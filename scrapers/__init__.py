from fantasy_pros import scrape as fp_scrape
from roto_grinders import scrape as rg_scrape

scrape_dict = {
    'fanpros': fp_scrape,
    'rotogrinders': rg_scrape
}


def scrape(source):
    return scrape_dict[source]()
