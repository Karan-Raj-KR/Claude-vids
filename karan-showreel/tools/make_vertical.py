"""Copy compositions/*.html into vertical/compositions/ with 1080x1920 roots.
Run after editing any scene (tools/scenes.py writes the 16:9 originals)."""
import glob, os, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dst = os.path.join(ROOT, "vertical", "compositions")
if os.path.islink(dst):
    os.unlink(dst)
os.makedirs(dst, exist_ok=True)
for f in glob.glob(os.path.join(ROOT, "compositions", "*.html")):
    s = open(f).read().replace('data-width="1920" data-height="1080"', 'data-width="1080" data-height="1920"')
    open(os.path.join(dst, os.path.basename(f)), "w").write(s)
comp = os.path.join(ROOT, "compositions", "components")
if os.path.isdir(comp):
    shutil.copytree(comp, os.path.join(dst, "components"), dirs_exist_ok=True)
print("vertical scenes:", len(glob.glob(os.path.join(dst, "*.html"))))
