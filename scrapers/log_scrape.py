def log_scrape_wrapper(func):
    def inner(*args):
        print('Scraping {}...'.format(args[0]))
        func(*args)
        print('Scrape complete \n****************')

    return inner
