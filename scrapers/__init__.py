from os import path

from fantasy_pros import scrape as fp_scrape
from roto_grinders import scrape as rg_scrape
from nfl_fantasy import scrape as nfl_scrape

scrape_dict = {
    'fanpros': fp_scrape,
    'rotogrinders': rg_scrape,
    'nfl_fantasy': nfl_scrape
}

CSV_FILE_PATH = path.join(path.split(path.split(path.realpath(__file__))[0])[0], 'data', '{}')

def scrape(source):
    return scrape_dict[source]()

GENERATE_COMMAND_LINE = [
    ['-source', 'data source to use', 'rotogrinders']
]


