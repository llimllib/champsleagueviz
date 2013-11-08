import re, requests, csv, time

teams = []
for group in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']:
    r = requests.get("http://www.oddschecker.com/football/europa-league/europa-league-group-%s/winner" % group,
                     cookies={"odds_type":"decimal"})


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
