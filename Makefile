serve:
	python -m SimpleHTTPServer

push:
	git checkout gh-pages
	git rebase master
	git push
	git checkout master

.PHONY: serve push
