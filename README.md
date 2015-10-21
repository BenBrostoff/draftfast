Special thanks to _swanson, who authored [this repo](https://github.com/swanson/degenerate), which mine is heavily based off of. I currently use data from [Fantasy Pros](http://www.fantasypros.com/) as the criteria to optimize on.

Pre-reqs:

* [ortools](https://developers.google.com/optimization/installing?hl=en)

To run, pass in the current week to the script and scrape data from FantasyPros:
<pre><code>python optimize.py -w 1</pre></code>

Arguments can also be passed to run the optimizer multiple times and continually eliminate pre-optimized players from the lineup. For instance, to run three different iterations and generate three different sets of players:

<pre><code>python optimize.py -w 1 -i 3</pre></code>

To do:

* Require QB to have at least one WR on team in lineup 
* More data
* Find better way of combining data sets on name



	

