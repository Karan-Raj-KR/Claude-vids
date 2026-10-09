"""Copy compositions/*.html into vertical/compositions/ with 1080x1920 roots."""
import glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dst = os.path.join(ROOT, "vertical", "compositions")
os.makedirs(dst, exist_ok=True)
for f in glob.glob(os.path.join(ROOT, "compositions", "*.html")):
    s = open(f).read().replace('data-width="1920" data-height="1080"', 'data-width="1080" data-height="1920"')
    open(os.path.join(dst, os.path.basename(f)), "w").write(s)
print("vertical scenes written")
