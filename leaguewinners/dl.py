import re, requests, csv, time
from bs4 import BeautifulSoup

teams = []
for country, urlpart in [('Germany', 'germany/bundesliga/german-bundesliga'),
                         ('Spain', 'spain/la-liga-primera/spanish-la-liga-primera'),
                         ('England', 'english/premier-league'),
                         ('France', 'france/ligue-1/french-ligue-1'),
                         ('Italy', 'italy/serie-a/italy-serie-a'),
                         ('Scotland', 'scottish/premiership'),
                         ('Holland', 'other/netherlands/eredivisie/holland-eredivisie'),
                         ('Portugal', 'other/portugal/primeira-liga/portuguese-super-liga'),
                         ('Turkey', 'other/turkey/super-lig/turkish-super-league')]:
    url = "http://www.oddschecker.com/football/%s/winner" % urlpart
    print "getting %s" % url
    r = requests.get(url, cookies={"odds_type":"decimal"})

    soup = BeautifulSoup(r.text)
    table = soup.find(attrs={"class":"eventTable"})
    sitesrow = table.find_all("tr", {"class": "eventTableHeader"})
    sitelinks = sitesrow[0].find_all(lambda t: t.has_attr("title"))
    sites = [t["title"] for t in sitelinks]

    teamrows = table.find_all(attrs={"class": "eventTableRow"})
    for row in teamrows:
        cols = [t.text for t in row.find_all("td")]
        name = cols[1]

        if 'any other' in name.lower(): continue

        odds = []
        isanodd = lambda t: (t.name=="td" and t.has_attr("class") and
                             ('o' in t.attrs["class"] or
                              'oi' in t.attrs["class"] or
                              'oo' in t.attrs["class"]))
        rawodds = [t.text for t in row.find_all(isanodd)]
        for o in rawodds:
            if not o or '-' in o: odds.append(None)
            else:                 odds.append(float(o))
        assert len(odds) == len(sites), "{} {}".format(odds, sites)
        teams.append([name, country] + odds)

t = str(time.time()).split(".")[0]
with file("raw/odds%s.csv" % t, 'w') as outfile:
    w = csv.writer(outfile)
    w.writerow(['name', 'country'] + sites)
    for row in teams:
        w.writerow(row)
