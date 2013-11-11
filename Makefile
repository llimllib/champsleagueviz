serve:
	python -m SimpleHTTPServer

deploy:
	ssh llimllib@hubvan.com "cd champsleagueviz && git pull"

push:
	-git branch -D gh-pages
	git checkout -b gh-pages
	git push -f -u origin gh-pages
	git checkout master

update:
	python dl.py
	python stats.py
	cd leaguewinners && make update
	cd europa && make update
	cd nfl && make update
	cd qualify && make update
	git add raw/*
	git commit -m "update champsleague data" raw/* summary.csv index.html
	git push
	make push

.PHONY: serve push deploy update
