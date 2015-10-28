function get_current_week {
    rm data/dk-salaries-current-week.csv
    mv ~/Downloads/DKSalaries.csv data/dk-salaries-current-week.csv
}

get_current_week
python manage-dups.py