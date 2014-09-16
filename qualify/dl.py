import re, requests, csv, time
from bs4 import BeautifulSoup

teams = []
for group in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
    try:
        url = "http://www.oddschecker.com/football/champions-league/champions-league-group-%s/to-qualify" % group
        print "getting {}".format(url)
        soup = BeautifulSoup(requests.get(url, cookies={"odds_type":"decimal"}).text)

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
            teams.append([name, group] + odds)
    except:
        print "Unexpected error. skipping"
        traceback.print_exc()

t = str(time.time()).split(".")[0]
with file("raw/odds%s.csv" % t, 'w') as outfile:
    w = csv.writer(outfile)
    w.writerow(['name', 'group'] + sites)
    for row in teams:
        w.writerow(row)
