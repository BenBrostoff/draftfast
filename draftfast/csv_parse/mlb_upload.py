import os
import subprocess
import csv
from itertools import islice

from draftfast import dke_exceptions as dke

upload_file = "{}/data/current-upload.csv".format(os.getcwd())


def create_upload_file():
    subprocess.call(["touch", upload_file])
    with open(upload_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "P",
                "P",
                "C",
                "1B",
                "2B",
                "3B",
                "SS",
                "OF",
                "OF",
                "OF",
            ]
        )


def map_pids(pid_file):
    player_map = {}
    with open(pid_file, "r") as f:
        n = 0
        fields = None
        for line in f.readlines():
            n += 1
            if "TeamAbbrev" in line:  # line with field names was found
                fields = line.split(",")
                break

        if not fields:
            raise dke.InvalidCSVUploadFileException(
                "Check that you're using the DK CSV upload template, "
                + "which can be found at "
                + "https://www.draftkings.com/lineup/upload."
            )

        f.close()
        f = islice(open(pid_file, "r"), n, None)
        reader = csv.DictReader(f, fieldnames=fields)
        for line in reader:
            player_map[line["Name"] + " " + line["Position"]] = line["ID"]

    return player_map


def update_upload_csv(player_map, roster):
    sorted_players = roster.sorted_players()
    with open(upload_file, "a") as f:
        writer = csv.writer(f)
        writer.writerow([p.get_player_id(player_map) for p in sorted_players])
