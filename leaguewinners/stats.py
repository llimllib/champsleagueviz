import glob, csv, re, shutil, time, mustache
import numpy as np

oddsfile = list(sorted(glob.glob('raw/odds*.csv')))[-1]
timestamp = re.search('s(.*?)\.', oddsfile).group(1)
with open(oddsfile) as infile:
    reader = csv.reader(infile)
    header = reader.next()
    teams = [row for row in reader]

fixed = []
for team in teams:
    t = team[0:2]
    for odd in team[2:]:
        if odd:
            o = float(odd)
            # betdaq lists some impossible odds. WTF?
            if o < 1: o = 1.
            t.append(o)
    fixed.append(t)

teams = fixed

summary = []
for team in teams:
    odds = team[2:]
    max_ = max(odds)
    min_ = min(odds)
    mean = np.mean(odds)
    median = np.median(odds)
    twentyfive = np.percentile(odds, 25)
    seventyfive = np.percentile(odds, 75)
    summary.append(team[:2] + [max_, min_, mean, median, twentyfive, seventyfive])

summaryfile = "raw/summary%s.csv" % timestamp
with file(summaryfile, 'w') as outfile:
    w = csv.writer(outfile)
    w.writerow(['name', 'country', 'max', 'min', 'mean', 'median', 'twentyfive', 'seventyfive'])
    for row in summary:
        w.writerow(row)

shutil.copy2(summaryfile, "summary.csv")

last_updated = time.strftime("%b %d %Y %H:%M")

context = {"last_updated": last_updated}
out = mustache.render(file("index.mustache.html").read(), context)
file("index.html", 'w').write(out)
