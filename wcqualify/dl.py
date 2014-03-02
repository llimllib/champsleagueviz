import requests, csv, time
from bs4 import BeautifulSoup

def download_group_odds():
    teams = []
    sites = []
    for group in (chr(ord('a') + x) for x in range(0,8)):
        urltemplate = "http://www.oddschecker.com/football/world-cup/group-{}/to-qualify"
        url = urltemplate.format(group)
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
            teams.append([name, group] + odds)

    return teams, sites


if __name__=="__main__":
    teams, sites = download_group_odds()

    t = str(time.time()).split(".")[0]
    with file("raw/group_odds%s.csv" % t, 'w') as outfile:
        w = csv.writer(outfile)
        w.writerow(['name'] + sites)
        for row in teams:
            w.writerow(row)
