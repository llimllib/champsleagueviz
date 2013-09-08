import re, requests

for group in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
    r = requests.get("http://www.oddschecker.com/football/champions-league/champions-league-group-%s/winner" % group,
                     cookies={"odds_type":"decimal"})

    table = re.search("<table.*?eventTable.*?</table>", r.text, re.DOTALL).group()

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
