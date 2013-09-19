serve:
	python -m SimpleHTTPServer

push:
	git branch -D gh-pages
	git checkout -b gh-pages
	git push -f -u origin gh-pages
	git checkout master

update:
	python dl.py
	python stats.py
	cd leaguewinners && make update
	cd nfl && make update
	git add raw/*
	git commit -m "update champsleague data" raw/* summary.csv
	git push
	make push

.PHONY: serve push
