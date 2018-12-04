from draftfast.pickem.pickem_command_line import get_args
from draftfast.pickem.pickem_optimize import optimize, get_all_players

if __name__ == '__main__':
    args = get_args()
    all_players = get_all_players(
        args.salary_file,
        args.projection_file,
        args.use_averages,
    )
    print(optimize(all_players, args))
