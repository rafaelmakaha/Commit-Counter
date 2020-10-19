# Commit Counter

This project provides a python script to count contributors commits plus co-authored commits.

The idea came because Github contributors graphs does not includes co-authors on their statistics to build these graphs.

## Usage

To run the script you need to have your `git log` on a file, but remember to change to the correct branch that you want to work on:

```
git log \
    --pretty=format:'{%n  "commit": "%H",%n  "author": "%aN <%aE>",%n  "date": "%ad",%n  "message": "%B"%n},' \
    $@ | \
    perl -pe 'BEGIN{print "["}; END{print "]\n"}' | \
    perl -pe 's/},]/}]/' > log.json
```
Run the script
```
python3 commit_count.py
```

