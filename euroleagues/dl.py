import re, requests, csv, time

teams = []
for group in ['germany/bundesliga/german-bundesliga',
              'spain/la-liga-primera/spanish-la-liga-primera',
              'english/premier-league',
              'france/ligue-1/french-ligue-1']:
    url = "http://www.oddschecker.com/football/%s/winner" % group
    print "getting %s" % url
    r = requests.get(url, cookies={"odds_type":"decimal"})

    table = re.search("<table.*?eventTable.*?</table>", r.text, re.DOTALL).group()

    sitesrow = re.search("<tr.*?eventTableHeader.*?</tr>", table, re.DOTALL).group()
    # big tables dupe the sites list, so only get uniques
    sites = list(set(re.findall('<a.*?title="(.*?)"', sitesrow)))

    teamrows = re.findall(r'<tr class="eventTableRow.*?</tr>', table, re.DOTALL)
    for row in teamrows:
        cols = re.findall("<td.*?>(.*?)<", row)
        name = cols[1]

        if 'any other' in name.lower(): continue

        odds = []
        for c in cols[3:]:
            if not c or '-' in c: odds.append(None)
            else:                 odds.append(float(c))
        assert len(odds) == len(sites)
        teams.append([name, group] + odds)

t = str(time.time()).split(".")[0]
with file("raw/odds%s.csv" % t, 'w') as outfile:
    w = csv.writer(outfile)
    w.writerow(['name', 'group'] + sites)
    for row in teams:
        w.writerow(row)
