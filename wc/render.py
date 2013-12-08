import mustache, time

last_updated = time.strftime("%b %d %Y %H:%M")

context = {"last_updated": last_updated}
out = mustache.render(file("index.mustache.html").read(), context)
file("index.html", 'w').write(out)
