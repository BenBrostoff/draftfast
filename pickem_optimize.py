import scrapers
import dke_exceptions as dke
from pickem.pickem_command_line import get_args
from pickem.pickem_optimize import optimize, get_all_players

if __name__ == '__main__':
    args = get_args()
    if args.scrape:
        try:
            scrapers.scrape(args.source)
        except KeyError:
            raise dke.InvalidProjectionSourceException(
                'You must choose from the following data sources {}.'
                .format(scrapers.scrape_dict.keys())
            )

    all_players = get_all_players(
        args.salary_file,
        args.projection_file,
        args.use_averages,
    )
    print(optimize(all_players, args))
