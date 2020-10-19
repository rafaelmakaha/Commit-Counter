'''
Use this command to send git log to json file
git log \
    --pretty=format:'{%n  "commit": "%H",%n  "author": "%aN <%aE>",%n  "date": "%ad",%n  "message": "%B"%n},' \
    $@ | \
    perl -pe 'BEGIN{print "["}; END{print "]\n"}' | \
    perl -pe 's/},]/}]/' > log.json
'''
import os
import json
import re
import datetime

# Add script to filter log.json
    # filters for:
        # \n\n -> empty
        # \n" -> "
        # \nCo-author -> empty
# Add path to git repo


content = []
with open('log.json') as fp:
    data = json.load(fp)

contr = {}

# Sprint start and finish dates
sprint_number = 5
start_date = datetime.date(2020, 10, 1)
finish_date = datetime.date(2020, 10, 8)

# Iterates over all commits
for item in data:
    # gets commit date
    commit_date = datetime.datetime.strptime(item['date'],"%a %b %d %H:%M:%S %Y %z").date()
    # filters commits by date
    if commit_date > start_date and commit_date <= finish_date:
        # if commit is a merge, doesn't count
        if "merge" in item["message"].lower():
            continue
        # adds new contrib
        if not item['author'] in contr:
            contr[item['author']] = 1
        contr[item['author']] += 1
        m = item['message']
        co = re.findall('authored-by: [\w\s]+ <[a-zA-Z0-9.@]*>',m)
        if co:
            for c in co:
                aux = c.replace('authored-by: ','')
                if not aux in contr:
                    contr[aux] = 1
                contr[aux] += 1


ans = {}
for key in contr.keys():
    email = key[key.find('<')+1:key.find('>')]
    nome = key[:key.find('<')]
    if not email in ans.keys():
        ans[email] = [nome,contr[key]]
    else:
        ans[email] = [ans[email][0],ans[email][1]+contr[key]]

for a in ans:
    print(a,ans[a])

import matplotlib.pyplot as plt
import numpy as np

objects = []
values = []
for a in ans:
    objects.append(ans[a][0])
    values.append(ans[a][1])
y_pos = np.arange(len(objects))
plt.bar(y_pos, values, align='center', alpha=0.5)
# plt.figure(figsize=(20, 3))  # width:20, height:3
# plt.bar(y_pos, values, align='edge', width=0.3)
plt.xticks(y_pos, objects)
plt.ylabel('Commits')
plt.title(f'Sprint {sprint_number}')

plt.show()