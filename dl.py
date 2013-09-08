import re, requests

r = requests.get("http://www.oddschecker.com/football/champions-league/champions-league-group-a/winner",
                 cookies={"odds_type":"decimal"})

table = re.search("<table.*?eventTable.*?</table>", r.text, re.DOTALL).group()

sitesrow = re.search("<tr.*?eventTableHeader.*?</tr>", table, re.DOTALL).group()
sites = re.findall('<a.*?title="(.*?)"', sitesrow)

teamrows = re.findall(r'<tr class="eventTableRow.*?</tr>', table, re.DOTALL)
for row in teamrows:
    print re.findall("<td.*?>(.*?)<", row)
#names = [re.findall('_name">(.*?)<', t)[0] for t in teamrows]

