def add_constraints(query_args, remove):
    def filter_fn(player):
        kwargs = {'player': player, 'query_args': query_args}
        return _is_not_selected(player, remove) and \
            _is_above_projected_points(**kwargs) and \
            _is_below_cost(**kwargs) and \
            _is_below_proj_ownership_pct(**kwargs) and \
            not _is_banned_player(**kwargs) and \
            _is_selected_team(**kwargs)

    return filter_fn


def _is_not_selected(player, remove):
    return player.name not in remove


def _is_above_projected_points(player, query_args):
    return (player.proj >= int(query_args.lp) or player.pos in ['DST'])


def _is_below_cost(player, query_args):
    return player.cost <= int(query_args.ms)


def _is_below_proj_ownership_pct(player, query_args):
    return player.projected_ownership_pct <= int(query_args.po)


def _is_selected_team(player, query_args):
    if player.team is None:
        return False
    if not query_args.teams or player.pos in ['DST']:
        return True

    return player.team in query_args.teams


def _is_banned_player(player, query_args):
    if not query_args.banned:
        return False
    return player.name in query_args.banned
