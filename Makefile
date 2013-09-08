serve:
	python -m SimpleHTTPServer

push:
	git checkout gh-pages
	git rebase master
	git push --force
	git checkout master

.PHONY: serve push
