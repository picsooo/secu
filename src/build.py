#!/usr/bin/env python3
"""Génère les maquettes Secura : un dossier par société, 3 pages chacune."""
import json, os, html, shutil, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "public")
E = html.escape

ICONS = [
    '<path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5z"/><path d="m9 12 2 2 4-4"/>',
    '<rect x="3" y="7" width="18" height="12" rx="2"/><path d="M7 7V5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v2"/><circle cx="12" cy="13" r="2"/>',
    '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    '<path d="M3 21h18"/><path d="M5 21V8l7-5 7 5v13"/><path d="M9 21v-6h6v6"/>',
    '<circle cx="11" cy="11" r="7"/><path d="m21 21-5-5"/>',
]


def icon(i):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round">' + ICONS[i % len(ICONS)] + '</svg>')


def imgs(slug):
    d = os.path.join(SRC, "img", slug)
    if not os.path.isdir(d):
        return []
    return sorted(f for f in os.listdir(d) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))


def visual(c, pics, i, cls):
    if pics:
        p = pics[i % len(pics)]
        return f'<div class="{cls} ph"><img src="img/{p}" alt="" draggable="false" loading="lazy"></div>'
    return f'<div class="{cls} ph ph-abs"><span>{E(c["name"])}</span></div>'


def monogram(name):
    words = [w for w in re.split(r"[\s'’-]+", name) if w and w[0].isalpha() and w.lower() not in ("et", "de", "la", "le", "des", "du", "l")]
    return "".join(w[0] for w in words[:2]).upper() or name[:2].upper()


def head(c, page):
    nav = [("index.html", "Accueil"), ("services.html", "Services"), ("contact.html", "Contact")]
    links = "".join(f'<a href="{h}"{" class=on" if h == page else ""}>{t}</a>' for h, t in nav)
    return f"""<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>{E(c['name'])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@500;600;700&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/site.css">
<style>:root{{--ac:{c['accent']};--dk:{c['dark']}}}</style></head>
<body><div class="wm" aria-hidden="true"></div>
<header class="top"><div class="wrap bar">
<a class="brand" href="index.html"><b>{E(monogram(c['name']))}</b><span>{E(c['name'])}</span></a>
<nav>{links}</nav><a class="btn sm" href="contact.html">Demander un devis</a>
<button class="burger" aria-label="Menu" onclick="document.body.classList.toggle('nav-open')"><i></i><i></i></button>
</div></header>"""


def foot(c):
    return f"""<footer class="foot"><div class="wrap fgrid">
<div><a class="brand light" href="index.html"><b>{E(monogram(c['name']))}</b><span>{E(c['name'])}</span></a>
<p>{E(c['full'])}<br>{E(c['group'])} · {E(c['city'])}</p></div>
<div><h4>Navigation</h4><a href="index.html">Accueil</a><a href="services.html">Services</a><a href="contact.html">Contact</a></div>
<div><h4>Contact</h4><p>{E(c['city'])}, Algérie<br>{E(c['phone'] or 'Téléphone à compléter')}</p></div>
</div><div class="wrap legal">© 2026 {E(c['name'])} · Maquette réalisée par Webminds Digital Solutions</div></footer>
<script src="../assets/p.js"></script></body></html>"""


def page_index(c, pics):
    stats = "".join(f'<div><strong>{E(a)}</strong><span>{E(b)}</span></div>' for a, b in c["stats"])
    svc = "".join(f'<a class="card" href="services.html"><span class="ic">{icon(i)}</span><h3>{E(t)}</h3><p>{E(d)}</p><em>En savoir plus →</em></a>'
                  for i, (t, d) in enumerate(c["services"][:3]))
    return head(c, "index.html") + f"""
<main>
<section class="hero"><div class="wrap hgrid">
<div class="htxt reveal"><p class="kicker">{E(c['group'])} · {E(c['city'])}</p>
<h1>{E(c['tagline'])}</h1><p class="lead">{E(c['intro'])}</p>
<div class="ctas"><a class="btn" href="contact.html">Demander un devis</a><a class="btn ghost" href="services.html">Nos services</a></div></div>
{visual(c, pics, 0, 'hvis reveal')}
</div></section>
<section class="stats"><div class="wrap sgrid">{stats}</div></section>
<section class="sec"><div class="wrap">
<div class="shead reveal"><p class="kicker">Ce que nous faisons</p><h2>{E(c.get('svc_title','Des solutions de sécurité adaptées à chaque site'))}</h2></div>
<div class="cards reveal">{svc}</div></div></section>
<section class="sec alt"><div class="wrap split">
{visual(c, pics, 1, 'svis reveal')}
<div class="reveal"><p class="kicker">Qui sommes-nous</p><h2>{E(c['full'])}</h2><p>{E(c['about'])}</p>
<a class="link" href="contact.html">Nous rencontrer →</a></div></div></section>
<section class="band"><div class="wrap bandin reveal"><h2>{E(c.get('band','Un site à protéger ? Parlons-en.'))}</h2>
<a class="btn light" href="contact.html">Contactez-nous</a></div></section>
</main>""" + foot(c)


def page_services(c, pics):
    cards = "".join(f'<div class="card"><span class="ic">{icon(i)}</span><h3>{E(t)}</h3><p>{E(d)}</p></div>'
                    for i, (t, d) in enumerate(c["services"]))
    steps = [("Écoute", "Nous visitons votre site et identifions vos besoins."),
             ("Analyse", "Nous évaluons les risques et les points sensibles."),
             ("Dispositif", "Nous proposons un dispositif chiffré et adapté."),
             ("Suivi", "Nous assurons le contrôle qualité et le reporting.")]
    st = "".join(f'<li><b>0{i+1}</b><h4>{a}</h4><p>{b}</p></li>' for i, (a, b) in enumerate(steps))
    return head(c, "services.html") + f"""
<main>
<section class="phead"><div class="wrap"><p class="kicker">Services</p><h1>Nos prestations</h1>
<p class="lead">{E(c['intro'])}</p></div></section>
<section class="sec"><div class="wrap"><div class="cards six reveal">{cards}</div></div></section>
<section class="sec alt"><div class="wrap">
<div class="shead reveal"><p class="kicker">Notre méthode</p><h2>De l'audit au suivi, une démarche claire</h2></div>
<ol class="steps reveal">{st}</ol></div></section>
<section class="sec"><div class="wrap split">
<div class="reveal"><p class="kicker">Sur le terrain</p><h2>{E(c.get('field_title','Des équipes formées et encadrées'))}</h2>
<p>{E(c.get('field','Chaque agent est recruté, formé et suivi selon des procédures strictes. Nos responsables de site assurent un contrôle régulier et un compte rendu à nos clients.'))}</p>
<a class="btn" href="contact.html">Demander un devis</a></div>
{visual(c, pics, 2, 'svis reveal')}</div></section>
</main>""" + foot(c)


def page_contact(c, pics):
    opts = "".join(f"<option>{E(t)}</option>" for t, _ in c["services"])
    return head(c, "contact.html") + f"""
<main>
<section class="phead"><div class="wrap"><p class="kicker">Contact</p><h1>Parlons de votre projet</h1>
<p class="lead">Décrivez votre site et vos besoins : un responsable vous recontacte rapidement.</p></div></section>
<section class="sec"><div class="wrap cgrid">
<form class="form reveal" onsubmit="event.preventDefault();this.classList.add('sent')">
<div class="row"><label>Nom<input required></label><label>Société<input></label></div>
<div class="row"><label>Téléphone<input required></label><label>E-mail<input type="email"></label></div>
<label>Prestation<select>{opts}</select></label>
<label>Message<textarea rows="5"></textarea></label>
<button class="btn" type="submit">Envoyer la demande</button>
<p class="ok">Merci, votre demande a bien été envoyée.</p></form>
<aside class="info reveal"><h3>{E(c['full'])}</h3><p>{E(c['group'])}</p>
<ul><li><span>Adresse</span>{E(c['city'])}, Algérie</li><li><span>Téléphone</span>{E(c['phone'] or 'À compléter')}</li>
<li><span>E-mail</span>À compléter</li><li><span>Horaires</span>Dimanche – jeudi, 8 h – 17 h<br>Permanence 24/7</li></ul>
{visual(c, pics, 3, 'mini')}</aside></div></section>
</main>""" + foot(c)


def hub(cs):
    items = "".join(f'<a href="{c["slug"]}/index.html" style="--ac:{c["accent"]};--dk:{c["dark"]}"><b>{E(monogram(c["name"]))}</b>'
                    f'<span>{E(c["name"])}</span><em>Stand {E(c["stand"])} · {E(c["city"])}</em></a>' for c in cs)
    return f"""<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Secura</title>
<link href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@600;700&family=Instrument+Sans:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css"></head><body class="hubp"><div class="wm"></div>
<main class="wrap hub"><h1>Secura Algeria 2026</h1><p class="lead">Maquettes préparées par Webminds pour les exposants.</p>
<div class="hubgrid">{items}</div></main><script src="assets/p.js"></script></body></html>"""


def main():
    cs = json.load(open(os.path.join(SRC, "companies.json"), encoding="utf-8"))
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    shutil.copy(os.path.join(SRC, "site.css"), os.path.join(OUT, "assets", "site.css"))
    for c in cs:
        d = os.path.join(OUT, c["slug"])
        os.makedirs(d)
        pics = imgs(c["slug"])
        if pics:
            shutil.copytree(os.path.join(SRC, "img", c["slug"]), os.path.join(d, "img"))
        for name, fn in (("index.html", page_index), ("services.html", page_services), ("contact.html", page_contact)):
            open(os.path.join(d, name), "w", encoding="utf-8").write(fn(c, pics))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(hub(cs))
    print(len(cs), "sociétés générées")


if __name__ == "__main__":
    main()
