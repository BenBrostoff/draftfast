#/bin/bash

function get_current_week {
    mv ~/Downloads/DKSalaries.csv data/current-salaries.csv
}

get_current_week
python nfl/prepare_data.py
