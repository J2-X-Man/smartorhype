#!/usr/bin/env python3
"""Baut index.html aus products.json (neuestes Produkt oben).

    python build.py

Produkte mit einem Datum in der Zukunft werden erst ab diesem Tag angezeigt
(im Browser per JavaScript, ohne JavaScript erscheinen alle).
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TAG = "smartorhype-20"

products = json.load(open(os.path.join(HERE, "products.json"), encoding="utf-8"))
products.sort(key=lambda p: p["date"], reverse=True)


def card(p):
    e = {k: html.escape(str(v), quote=True) for k, v in p.items()}
    return f"""      <li class="card" data-date="{e['date']}">
        <div class="meta"><span class="brand">{e.get('brand', '')}</span><span class="price">{e.get('price', '')}</span></div>
        <h2>{e['name']}</h2>
        <p class="video">From the video: <em>{e.get('video', '')}</em></p>
        <a class="buy" href="{e['url']}" target="_blank" rel="sponsored nofollow noopener">View on Amazon <span aria-hidden="true">→</span></a>
      </li>"""


page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SMART or HYPE – Products from our videos</title>
<meta name="description" content="Every product from the SMART or HYPE tech shorts – with links to buy.">
<link rel="icon" href="logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;900&family=Playfair+Display:ital@1&display=swap" rel="stylesheet">
<style>
  :root {{ --bg:#141414; --card:#1f1f1f; --line:#2c2c2c; --ink:#f4efe4; --mute:#a29d93; --or:#fb7232; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink); font-family:Archivo, system-ui, sans-serif; }}
  main {{ max-width:560px; margin:0 auto; padding:40px 16px 56px; }}
  header {{ text-align:center; margin-bottom:28px; }}
  header img {{ width:88px; height:88px; border-radius:20px; display:block; margin:0 auto 18px; }}
  h1 {{ font-weight:900; font-size:34px; letter-spacing:-.5px; margin:0; }}
  h1 span {{ color:var(--or); }}
  .sub {{ font-family:"Playfair Display", Georgia, serif; font-style:italic; color:var(--mute); font-size:18px; margin:8px 0 0; }}
  .social {{ display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin:20px 0 0; padding:0; list-style:none; }}
  .social a {{ color:var(--ink); text-decoration:none; font-size:13px; font-weight:700; letter-spacing:.06em; text-transform:uppercase;
              border:1px solid var(--line); border-radius:999px; padding:8px 14px; display:inline-block; }}
  .social a:hover {{ border-color:var(--or); color:var(--or); }}
  ul.list {{ list-style:none; margin:0; padding:0; display:grid; gap:14px; }}
  .card {{ background:var(--card); border:1px solid var(--line); border-radius:18px; padding:18px 18px 16px; }}
  .meta {{ display:flex; justify-content:space-between; gap:12px; font-size:12px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:var(--mute); }}
  .price {{ color:var(--or); }}
  .card h2 {{ font-size:23px; font-weight:900; margin:8px 0 4px; letter-spacing:-.3px; }}
  .video {{ color:var(--mute); font-size:14px; margin:0 0 14px; line-height:1.4; }}
  .video em {{ font-family:"Playfair Display", Georgia, serif; color:var(--ink); }}
  .buy {{ display:block; text-align:center; background:var(--or); color:#141414; font-weight:900; font-size:16px; text-decoration:none;
          border-radius:12px; padding:13px 16px; }}
  .buy:hover {{ filter:brightness(1.08); }}
  footer {{ margin-top:30px; text-align:center; color:var(--mute); font-size:12px; line-height:1.6; }}
</style>
</head>
<body>
<main>
  <header>
    <h1>SMART <span>OR</span> HYPE</h1>
    <p class="sub">New tech, checked in 60 seconds. Every product from our videos.</p>
    <ul class="social">
      <li><a href="https://www.youtube.com/@smartorhype">YouTube</a></li>
      <li><a href="https://www.tiktok.com/@smartorhype">TikTok</a></li>
      <li><a href="https://www.instagram.com/smartorhype">Instagram</a></li>
      <li><a href="https://www.facebook.com/1433674179823756">Facebook</a></li>
    </ul>
  </header>
  <ul class="list">
{chr(10).join(card(p) for p in products)}
  </ul>
  <footer>
    As an Amazon Associate I earn from qualifying purchases.<br>
    Links marked “View on Amazon” are affiliate links. Prices as shown in the video; check Amazon for the current price.
  </footer>
</main>
<script>
  (function () {{
    var d = new Date(), today = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
    document.querySelectorAll(".card").forEach(function (c) {{ if (c.dataset.date > today) c.remove(); }});
  }})();
</script>
</body>
</html>
"""
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
print(f"index.html: {len(products)} Produkte")
