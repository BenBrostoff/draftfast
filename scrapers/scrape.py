from draft_kings_fun.scrapers import scrape_dict


def scrape_all():
    scrape_dict['fanpros'](file_name='fantasy_pros-projections.csv')
    scrape_dict['rotogrinders'](file_name='rotogrinders-projections.csv')
    scrape_dict['nfl_fantasy'](file_name='nfl_fantasy-projections.csv')


if __name__ == "__main__":
    scrape_all()
