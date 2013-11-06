import re, requests, csv, time

teams = []
for group in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
    url = "http://www.oddschecker.com/football/champions-league/champions-league-group-%s/to-qualify" % group
    print "getting url %s" % url
    r = requests.get(url, cookies={"odds_type":"decimal"})

    try:
        table = re.search("<table.*?eventTable.*?</table>", r.text, re.DOTALL).group()
    except AttributeError:
        print "unable to parse url %s" % url
        continue

    sitesrow = re.search("<tr.*?eventTableHeader.*?</tr>", table, re.DOTALL).group()
    sites = re.findall('<a.*?title="(.*?)"', sitesrow)

    teamrows = re.findall(r'<tr class="eventTableRow.*?</tr>', table, re.DOTALL)
    for row in teamrows:
        cols = re.findall("<td.*?>(.*?)<", row)
        name = cols[1]

        # normalize PSG name
        if 'Paris' in name:
            name = "PSG"

        odds = []
        for c in cols[3:]:
            if not c: odds.append(None)
            else:     odds.append(float(c))
        assert len(odds) == len(sites)
        print name, odds
        teams.append([name, group] + odds)

t = str(time.time()).split(".")[0]
with file("raw/odds%s.csv" % t, 'w') as outfile:
    w = csv.writer(outfile)
    w.writerow(['name', 'group'] + sites)
    for row in teams:
        w.writerow(row)
