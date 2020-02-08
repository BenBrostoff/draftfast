import os
from draftfast.rules import DRAFT_KINGS, FAN_DUEL

upload_file = '{}/data/current-upload.csv'.format(os.getcwd())


def write_to_csv(writer, player_map, roster, game=DRAFT_KINGS,
                 league='NBA'):
    players = roster.sorted_players()

    ordered_possible = []
    if game == DRAFT_KINGS and league == 'EL':
        ordered_possible = [
            _on_position(players, ['G']),
            _on_position(players, ['G']),
            _on_position(players, ['F']),
            _on_position(players, ['F']),
            _on_position(players, ['F']),
            players
        ]
    elif game == DRAFT_KINGS and league == 'NFL':
        ordered_possible = [
            _on_position(players, ['QB']),
            _on_position(players, ['RB']),
            _on_position(players, ['RB']),
            _on_position(players, ['WR']),
            _on_position(players, ['WR']),
            _on_position(players, ['WR']),
            _on_position(players, ['TE']),

            # NFL Flex
            _on_position(players, ['TE', 'WR', 'RB']),
            _on_position(players, ['DST']),
        ]
    elif game == DRAFT_KINGS and league == 'XFL':
        ordered_possible = [
            _on_position(players, ['QB']),
            _on_position(players, ['RB']),
            _on_position(players, ['WR']),
            _on_position(players, ['WR']),
            _on_position(players, ['WR', 'RB']),
            _on_position(players, ['WR', 'RB']),
            _on_position(players, ['DST']),
        ]
    elif game == DRAFT_KINGS and league == 'SOCCER':
        ordered_possible = [
            _on_position(players, ['F']),
            _on_position(players, ['F']),
            _on_position(players, ['M']),
            _on_position(players, ['M']),
            _on_position(players, ['D']),
            _on_position(players, ['D']),
            _on_position(players, ['GK']),
            players
        ]
    elif game == DRAFT_KINGS and league == 'NHL':
        ordered_possible = [
            _on_position(players, ['C']),
            _on_position(players, ['C']),
            _on_position(players, ['W']),
            _on_position(players, ['W']),
            _on_position(players, ['W']),
            _on_position(players, ['D']),
            _on_position(players, ['D']),
            _on_position(players, ['G']),
            players
        ]
    elif game == DRAFT_KINGS:
        ordered_possible = [
            _on_position(players, ['PG']),
            _on_position(players, ['SG']),
            _on_position(players, ['SF']),
            _on_position(players, ['PF']),
            _on_position(players, ['C']),
            _on_position(players, ['SG', 'PG']),
            _on_position(players, ['SF', 'PF']),
            players
        ]
    elif game == FAN_DUEL:
        ordered_possible = [
            _on_position(players, ['PG']),
            _on_position(players, ['PG']),
            _on_position(players, ['SG']),
            _on_position(players, ['SG']),
            _on_position(players, ['SF']),
            _on_position(players, ['SF']),
            _on_position(players, ['PF']),
            _on_position(players, ['PF']),
            _on_position(players, ['C']),
        ]

    ordered_lineup = []
    counter = 0
    for ps in ordered_possible:
        counter += 1
        not_used_ps = [
            p for p in ps
            if p not in ordered_lineup
        ]
        ordered_lineup.append(not_used_ps[0])

    writer.writerow([
        p.get_player_id(player_map)
        for p in ordered_lineup
    ])


def _on_position(players, possible):
    return [p for p in players if p.pos in possible]
