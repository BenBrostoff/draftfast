[![Build Status](https://travis-ci.org/BenBrostoff/draft-kings-fun.png)](https://travis-ci.org/BenBrostoff/draft-kings-fun)

## Introduction

Special thanks to _swanson, who authored [this repo](https://github.com/swanson/degenerate), which mine is heavily based off of. I currently use data from [Fantasy Pros](http://www.fantasypros.com/) as the criteria to optimize on.

Pre-reqs:

* [ortools](https://developers.google.com/optimization/installing?hl=en)

To run, download your desired week's salaries on DraftKings. For Mac users, this file will make its way into <code>~/Downloads/</code> as <code>DKSalaries.csv</code>. The script <code> new_week.sh</code> will move this file into its proper location if you're using a Mac (simply <code>bash new_week.sh</code>); otherwise, please do this step manually. It will also handle duplicate names in the CSV that would normally cause <code> ortools </code> to crash (currently only David Johnson has a shared name in the NFL).

If you're not a Mac user, after downloading the CSV data and placing it in its proper location:

<pre><code>python manage-dups.py</pre></code>

Next, pass in the current week to the script, scrape data from FantasyPros and allow for some mismatched data between the two sources:
<pre><code>python optimize.py -mp 100 -s y</pre></code>

One important note here is that passing in <code>y</code> for the scrape option will create <code>fantasy-pros.csv</code>. However, once you've scraped once, there's no need to do again.

## Optimization Options

Force a QB/WR or QB/TE combination from a particular team. For instance, if I wanted a guaranteed Cam Newton / Greg Olsen duo:

<pre><code>python optimize.py -mp 100 -duo CAR -dtype TE</pre></code>

Another example pairing DeAndre Hopkins and Brian Hoyer:

<pre><code>python optimize.py -mp 100 -duo HOU -dtype WR</pre></code>

Limit same team representation except for QB / skill player combos. Example:

<pre><code>python optimize.py -mp 100 -limit y</pre></code>

Run the optimizer multiple times and continually eliminate pre-optimized players from the lineup. For instance, to run three different iterations and generate three different sets of players:

<pre><code>python optimize.py -i 3</pre></code>

At any time, you can get a list of all possible options via:

<pre><code>python optimize.py --help</pre></code>

## Generating CSV for uploading multiple lineups to DraftKings

DraftKings allows uploading up to 500 lineups using a single CSV file. [You can learn more about DraftKings' support for lineup uploads here.](https://playbook.draftkings.com/news/draftkings-lineup-upload-tool) This tool supports
generating an uploadable CSV file containing the generated optimized lineups.

To use this feature:

1. Download the weekly salaries CSV from DraftKings
(containing player name, DK-estimated points, salary, etc).
2. Run `bash new_week.sh`.
3. Download the [CSV upload template](https://www.draftkings.com/lineup/upload) and get the file location (probably something like `~/Downloads/DKSalaries.csv`). *Note - this file has the same name as the weekly salaries CSV when downloaded from DraftKings, which can be confusing.*
4. Run `python optimize.py -pids <upload_tpl_location>`.
5. Upload the newly generated file to DraftKings from `data/current-upload.csv`.

I find this feature is extremely useful for "saving" lineups in DraftKings - one nice workflow is to run the optimizer always with the `--pids` flag and continually upload the lineups to DK.

## Projected Ownership Percentages (Experimental)

Projected ownership percentages as of this writing could be downloaded from [DFS Cafe](https://dfsreport.com/draftkings-ownership-percentages). If you download the CSV, you can filter on projected ownership percentage. For example, only include players below 15% owned.

```
python optimize.py -po_location 'data/ownership.csv' -po 15
```

## NBA

More to come here, but an NBA option exists for NBA contests. Currently it uses average PPG provided by DraftKings to optimize on:

<pre><code>python optimize.py -l NBA -s n</pre></code>

To do:

* Require QB to have at least one WR on team in lineup 
* More data
* Find better way of combining data sets on name
* Add virtualenv / automate dependencies installation
* Improve NBA combination testing
* Testing
