serve:
	python -m SimpleHTTPServer

push:
	git checkout gh-pages
	git rebase -s recursive -X theirs master
	git push --force
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
