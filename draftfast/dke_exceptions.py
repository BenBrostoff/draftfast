class MissingPlayersException(Exception):
    pass


class InvalidNFLTeamException(Exception):
    pass


class InvalidCSVUploadFileException(Exception):
    pass


MISSING_ERROR = """
Got {} projections out of {} total players.

You are allowing {} players to be missing from your
projections compared to the total players DraftKings
will allow you to play. You can change this allowance
via the mp flag.
"""

CSV_ERROR = """
You must provide the following fields
in your projection CSV: {}
"""
