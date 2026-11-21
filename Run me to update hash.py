import re, hashlib, base64
p = "bible_converter.html"
s = open(p, encoding="utf-8").read()
script = re.search(r"<script>(.*?)</script>", s, re.S).group(1)
h = base64.b64encode(hashlib.sha256(script.encode()).digest()).decode()
s = re.sub(r"sha256-[A-Za-z0-9+/=]+", "sha256-" + h, s, count=1)
open(p, "w", encoding="utf-8").write(s)
print("Updated hash:", h)