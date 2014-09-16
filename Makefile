serve:
	python -m SimpleHTTPServer

deploy:
	ssh llimllib@hubvan.com "cd champsleagueviz && git pull"

push:
	-git branch -D gh-pages
	git checkout -b gh-pages
	git push -f -u origin gh-pages
	git checkout master

updatecl:
	python dl.py
	python stats.py
	git add raw/*
	git commit -m "update champsleague data" raw/* summary.csv index.html
	git push

update:
	-cd leaguewinners && make update
	-cd europa && make update
	-cd nfl && make update
	-cd nba && make update
	-cd qualify && make update
	-cd wc && make update
	-cd wcqualify && make update
	-make updatecl
	make push

.PHONY: serve push deploy update updatecl
