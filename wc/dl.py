import re, requests, csv, time

def download_wc_odds():
    teams = []
    url = "http://www.oddschecker.com/football/world-cup/winner"
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
        teams.append([name] + odds)

    return teams, sites

def download_group_odds():
    teams = []
    sites = []
    for group in (chr(ord('a') + x) for x in range(0,8)):
        url = "http://www.oddschecker.com/football/world-cup-groups/group-{}/world-cup-group-{}/winner".format(group, group)
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

    return teams, sites


if __name__=="__main__":
    #teams, sites = download_wc_odds()

    #t = str(time.time()).split(".")[0]
    #with file("raw/winner_odds%s.csv" % t, 'w') as outfile:
    #    w = csv.writer(outfile)
    #    w.writerow(['name'] + sites)
    #    for row in teams:
    #        w.writerow(row)

    teams, sites = download_group_odds()

    t = str(time.time()).split(".")[0]
    with file("raw/group_odds%s.csv" % t, 'w') as outfile:
        w = csv.writer(outfile)
        w.writerow(['name'] + sites)
        for row in teams:
            w.writerow(row)
