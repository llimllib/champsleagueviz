serve:
	python -m SimpleHTTPServer

push:
	git checkout gh-pages
	git rebase master
	git push --force
	git checkout master

update:
	python dl.py
	python stats.py
	git add raw/*
	git commit -m "update data" raw/* summary.csv
	make push

.PHONY: serve push
