import glob, shutil, re
def sanitize(f):
    ext = f[-4:]
    return re.sub("[\s\.]", "", f).lower()[:-3] + ext

for f in glob.glob("*.svg"):
    shutil.move(f, sanitize(f))
