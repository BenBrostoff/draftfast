def add_constraints(query_args, remove):
    def filter_fn(player):
        kwargs = {'player': player, 'query_args': query_args}
        return _is_not_selected(player, remove) and \
            _is_above_projected_points(**kwargs) and \
            _is_below_cost(**kwargs) and \
            _is_above_min_cost(**kwargs) and \
            _is_below_proj_ownership_pct(**kwargs) and \
            not _is_banned_player(**kwargs) and \
            _is_selected_team(**kwargs) and \
            _is_home(**kwargs) and \
            _is_within_avg(**kwargs) and \
            _is_above_min_avg(**kwargs)

    return filter_fn


def add_pickem_contraints(query_args):
    def filter_fn(player):
        if not query_args:
            return True
        # TODO - add team banning
        kwargs = {'player': player, 'query_args': query_args}
        return (
            _is_above_projected_points(**kwargs) and
            (not _is_banned_player(**kwargs)) and
            # _is_selected_team(**kwargs) and
            _is_within_avg(**kwargs) and
            _is_above_min_avg(**kwargs)
        )

    return filter_fn


def lock_override(fn):
    def override_fn(**kwargs):
        if kwargs['player'].lock:
            return True
        return fn(**kwargs)

    return override_fn


def _is_not_selected(player, remove):
    return player.name not in remove


@lock_override
def _is_above_projected_points(player, query_args):
    if query_args.lp is None:
        return True
    return player.proj >= int(query_args.lp) or player.pos in ['DST']


@lock_override
def _is_below_cost(player, query_args):
    if query_args.ms is None:
        return True
    return player.cost <= int(query_args.ms)


@lock_override
def _is_above_min_cost(player, query_args):
    if query_args.sp is None:
        return True
    return player.cost >= int(query_args.sp)


@lock_override
def _is_below_proj_ownership_pct(player, query_args):
    if query_args.po is None:
        return True
    return player.projected_ownership_pct <= int(query_args.po)


@lock_override
def _is_selected_team(player, query_args):
    if player.team is None:
        return False
    if not query_args.teams or player.pos in ['DST']:
        return True

    return player.team in query_args.teams


def _is_banned_player(player, query_args):
    if player.pos == 'DST' and query_args.banned:
        return player.name.strip() in [
            n.strip() for n in query_args.banned
        ]
    if not query_args.banned:
        return False
    return player.name in query_args.banned


@lock_override
def _is_home(player, query_args):
    if query_args.home:
        return player.is_home
    return True


@lock_override
def _is_within_avg(player, query_args):
    if player.v_avg is None or query_args.v_avg is None:
        return True
    return abs(player.v_avg) < abs(float(query_args.v_avg))


@lock_override
def _is_above_min_avg(player, query_args):
    if query_args.min_avg is None:
        return True
    return (player.average_score or 0) > query_args.min_avg
