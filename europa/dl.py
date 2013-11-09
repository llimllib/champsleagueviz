import re, requests, csv, time

def parse_team(teamrow):
    cols = re.findall("<td.*?>(.*?)<", teamrow)
    name = cols[1]
    odds = []
    for c in cols[3:]:
        if not c: odds.append(None)
        else:
            try:
                odds.append(float(c))
            except ValueError:
                print "can't parse col c {0}, skipping".format(c)
                odds.append(None)
    assert len(odds) == len(sites)
    print name, odds
    return [name, group] + odds

def parse_teamrows(teamrows):
    teams = []
    for teamrow in teamrows:
        teams.append(parse_team(teamrow))
    return teams

teams = []
for group in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']:
    url = "http://www.oddschecker.com/football/europa-league/europa-league-group-%s/winner" % group
    print "getting %s" % url
    r = requests.get(url, cookies={"odds_type":"decimal"})

    try:
        table = re.search("<table.*?eventTable.*?</table>", r.text, re.DOTALL).group()
    except AttributeError:
        print "unable to parse url %s" % url
        continue

    sitesrow = re.search("<tr.*?eventTableHeader.*?</tr>", table, re.DOTALL).group()
    sites = re.findall('<a.*?title="(.*?)"', sitesrow)

    teamrows = re.findall(r'<tr class="eventTableRow.*?</tr>', table, re.DOTALL)
    teams += parse_teamrows(teamrows)
    print teams

t = str(time.time()).split(".")[0]
with file("raw/odds%s.csv" % t, 'w') as outfile:
    w = csv.writer(outfile)
    w.writerow(['name', 'group'] + sites)
    for row in teams:
        w.writerow(row)
