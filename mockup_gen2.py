#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mockup_gen2 — generator de mockup-uri nivel „showcase" (v2).
Un motor + 4 ARHETIPURI de layout, fiecare cu identitate proprie:

  atelier — meșteșug editorial (hârtie + cerneală + serif wonk)   ex: florărie, cizmărie, ceasornicărie, tapițerie, croitorie, mobilă
  urgent  — intervenție rapidă (asfalt întunecat, telefon uriaș)   ex: parbrize, tractări, deblocări, electrică auto la domiciliu
  studio  — vizual premium (galerie, imagini mari, minimal)        ex: detailing, vopsitorie, optică
  cabinet — programare calmă (încredere, program în față)          ex: kineto, reparații electrocasnice, GSM

Elemente-semnătură incluse în toate:
  • compozitor WhatsApp: pași configurabili per nișă → mesaj precompletat live
  • stare „Deschis/Închis acum" pe fusul București din program STRUCTURAT + ziua de azi evidențiată
  • ticker tematic per nișă, recenzii oneste (rating real), reveal cu failsafe, reduced-motion, JSON-LD

Usage:
  python3 mockup_gen2.py leads_v2.json                # generează în mockupuri/
  python3 mockup_gen2.py --from-scraped leads_found.json --out-json round_v2.json
                                                      # convertește output-ul scraperului în leaduri v2 (presets pe nișă)

Schema lead v2 (câmpuri principale; ce lipsește se completează din NICHE_PRESETS + ARCHETYPES):
  slug, archetype, niche_key, accent?, name, brand_a, brand_b?, brand_sub,
  phone_wa, phone_display, address, addr_line1, addr_city,
  rating, reviews_count, hours_s ({"mon":[8,20],...,"sun":null} sau "nonstop"),
  eyebrow, h1_a, h1_wonk, h1_b, lead,
  ticker_label, ticker[], composer{intro_title,intro_wonk,intro_sub,steps[{key,label,hint,options[{label,value}]}],base},
  services[{title,desc,tag,img}], story{eyebrow,h2_a,h2_wonk,body,facts[]},
  reviews[3], visit_kicker, visit_sub, images{hero,story}, seo_title, seo_desc
"""
import argparse, json, os, re, sys
from string import Template
from urllib.parse import quote

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE, "mockupuri")

U = "https://images.unsplash.com/photo-%s?auto=format&fit=crop&w=%d&q=%d"
def img(pid, w=900, q=80):
    if str(pid).startswith("http"): return pid
    return U % (pid, w, q)

# ─────────────────────────────────────────────────────── imagini verificate (200 + vizual)
IMG = {
  # florărie (verificate vizual în showcase)
  "flori_hero":"1487530811176-3780de880c2d","flori_dark":"1457089328109-e5d9bd499191",
  "flori_nunta":"1563241527-3004b7be0ffd","flori_vaza":"1591886960571-74d43a9d4166","flori_lalele":"1561181286-d3fee7d55364",
  # auto interior / tapițerie
  "tap_hero":"1503376780353-7e6692767b70","tap_scaun":"1547038577-da80abbc4f19","tap_volan":"1552519507-da3b142c6e3d",
  "tap_cusatura":"1489824904134-891ab64532f1","tap_clasic":"1449965408869-eaa3f722e40d",
  # detailing / spălătorie / studio auto
  "det_hero":"1520340356584-f9917d1eea6f","det_spuma":"1605559424843-9e4c228bf1c2","det_interior":"1503736334956-4c8f8e92946d",
  "det_lac":"1558618666-fcd25c85cd64","auto_road":"1492144534655-ae79c964c9d7","auto_dark":"1493238792000-8113da705763",
  "auto_far":"1486262715619-67b85e0b08d3",
  # vopsitorie / service
  "vops_1":"1625047509168-a7026f36de04","vops_2":"1487754180451-c456f719a1fc",
  # reparații / casă / cabinet
  "rep_1":"1581092160562-40aa08e78837","rep_2":"1607472586893-edb57bdc0e39","rep_3":"1620714223084-8fcacc6dfd8d",
  "casa_1":"1581578731548-c64695cc6952","casa_2":"1556909212-d5b604d0c90d",
  # generic curat
  "gen_1":"1497366216548-37526070297c","gen_2":"1521737604893-d14cc237f11d",
}

# ─────────────────────────────────────────────────────── arhetipuri
ARCHETYPES = {
 "atelier": dict(
   body_class="arch-atelier",
   fonts='<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..700,0..100,0..1;1,9..144,300..700,0..100,0..1&family=Instrument+Sans:ital,wght@0,400..700;1,400..700&display=swap" rel="stylesheet">',
   font_d="'Fraunces','Georgia',serif", font_s="'Instrument Sans',system-ui,sans-serif",
   tokens=dict(bg="#F6F2E7", bg2="#EFE9D8", card="#FFFDF6", ink="#1D2B22", ink2="#28382D", ink3="#41523F",
               line="#D8D0BC", lineink="#3B4B3E", mut="#5C6355", mutink="#A9B5A4",
               accent="#B42B62", accent_deep="#8E1F4C", soft="#F3E4E0", pollen="#E0A81C", stem="#64805F"),
   hero="split_arch", dark_story=True, radius="14px", chip_bg="#FFFDF6",
 ),
 "urgent": dict(
   body_class="arch-urgent",
   fonts='<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,72..125,400..900;1,72..125,400..900&family=Inter:wght@400..700&display=swap" rel="stylesheet">',
   font_d="'Archivo',system-ui,sans-serif", font_s="'Inter',system-ui,sans-serif",
   tokens=dict(bg="#101214", bg2="#16191C", card="#1C2024", ink="#F2F4F5", ink2="#E4E8EA", ink3="#C7CDD1",
               line="#2A3036", lineink="#2A3036", mut="#9AA3AA", mutink="#9AA3AA",
               accent="#FFC couldbe", accent_deep="#D99C00", soft="#22262B", pollen="#FFBE0B", stem="#5A6570"),
   hero="phone_first", dark_story=False, radius="10px", chip_bg="#1C2024",
 ),
 "studio": dict(
   body_class="arch-studio",
   fonts='<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400..700&family=Manrope:wght@400..800&display=swap" rel="stylesheet">',
   font_d="'Space Grotesk',system-ui,sans-serif", font_s="'Manrope',system-ui,sans-serif",
   tokens=dict(bg="#F4F4F2", bg2="#EBEBE8", card="#FFFFFF", ink="#151517", ink2="#232326", ink3="#3E3E44",
               line="#DDDDD8", lineink="#33333A", mut="#6B6B72", mutink="#A8A8B0",
               accent="#2762F3", accent_deep="#1D4CC4", soft="#E7EDFB", pollen="#E0A81C", stem="#7C7C85"),
   hero="fullbleed", dark_story=True, radius="16px", chip_bg="#FFFFFF",
 ),
 "cabinet": dict(
   body_class="arch-cabinet",
   fonts='<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300..800&family=Instrument+Sans:ital,wght@0,400..700;1,400..700&display=swap" rel="stylesheet">',
   font_d="'Bricolage Grotesque',system-ui,sans-serif", font_s="'Instrument Sans',system-ui,sans-serif",
   tokens=dict(bg="#F2F5F1", bg2="#E9EEE8", card="#FFFFFF", ink="#1E3230", ink2="#2A403D", ink3="#4057543",
               line="#D5DED4", lineink="#3A4F4C", mut="#5D6E6B", mutink="#A7B8B4",
               accent="#0E7C6B", accent_deep="#0A5F52", soft="#E2EFEB", pollen="#E0A81C", stem="#6E8A7F"),
   hero="calm_card", dark_story=True, radius="18px", chip_bg="#FFFFFF",
 ),
}
# corecții token-uri greșite mai sus (accent urgent, ink3 cabinet)
ARCHETYPES["urgent"]["tokens"]["accent"] = "#FFBE0B"
ARCHETYPES["cabinet"]["tokens"]["ink3"] = "#405754"

def norm_phone(s):
    d = re.sub(r"\D", "", s or "")
    return d[-9:] if len(d) >= 9 else d

def wa(tel, msg): return "https://wa.me/%s?text=%s" % (tel, quote(msg))

STAR = '<svg viewBox="0 0 24 24"><path d="M12 2l3 6.5 7 .8-5.2 4.7L18.5 22 12 18.3 5.5 22l1.7-8L2 9.3l7-.8z"/></svg>'
STARS5 = '<span class="stars" aria-hidden="true">' + STAR*5 + '</span>'
WA_SVG = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3a13 13 0 0 0-11 19.6L3 29l6.6-2a13 13 0 1 0 6.4-24zm0 23.6a10.6 10.6 0 0 1-5.4-1.5l-.4-.2-4 1 1-3.9-.3-.4A10.6 10.6 0 1 1 16 26.6zm6-7.9c-.3-.2-2-1-2.3-1.1-.3-.1-.5-.2-.8.2s-.9 1.1-1.1 1.3-.4.2-.8 0a8.6 8.6 0 0 1-4.3-3.7c-.3-.6.3-.5.9-1.8.1-.2 0-.4 0-.6s-.8-1.9-1-2.6c-.3-.7-.6-.6-.8-.6h-.7a1.3 1.3 0 0 0-1 .4 4 4 0 0 0-1.2 2.9 6.9 6.9 0 0 0 1.4 3.6 15.7 15.7 0 0 0 6 5.3c2.2 1 3 1 4.1.9a3.5 3.5 0 0 0 2.3-1.6 2.9 2.9 0 0 0 .2-1.6c0-.2-.3-.3-.6-.5z"/></svg>'
TEL_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 2.8c.5-.1 1 .1 1.3.5l1.9 2.6c.3.5.3 1.1-.1 1.5L8.6 8.8a12.6 12.6 0 0 0 6.6 6.6l1.4-1.1c.4-.4 1-.4 1.5-.1l2.6 1.9c.4.3.6.8.5 1.3l-.4 2c-.1.6-.6 1-1.2 1A17.4 17.4 0 0 1 3.6 4.4c0-.6.4-1.1 1-1.2z"/></svg>'
PIN_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7.4 7.4 0 0 0-7.4 7.4C4.6 15 12 22 12 22s7.4-7 7.4-12.6A7.4 7.4 0 0 0 12 2zm0 10a2.6 2.6 0 1 1 0-5.2 2.6 2.6 0 0 1 0 5.2z"/></svg>'
ARROW_SVG = '<svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
MARK_SVG = '<svg viewBox="0 0 48 48" class="fl" aria-hidden="true"><circle cx="24" cy="24" r="4.5"/><path d="M24 19.5c0-6-4-9.5-4-9.5s7.5-1 8.5 5.5c.6 3.9-4.5 4-4.5 4z"/><path d="M28.5 24c6 0 9.5-4 9.5-4s1 7.5-5.5 8.5c-3.9.6-4-4.5-4-4.5z"/><path d="M24 28.5c0 6 4 9.5 4 9.5s-7.5 1-8.5-5.5c-.6-3.9 4.5-4 4.5-4z"/><path d="M19.5 24c-6 0-9.5 4-9.5 4s-1-7.5 5.5-8.5c3.9-.6 4 4.5 4 4.5z"/></svg>'
BOLT_SVG = '<svg viewBox="0 0 48 48" class="fl" aria-hidden="true"><path d="M26 4 10 28h10l-2 16 18-26H26z"/></svg>'

ZI_RO = {"mon":"Luni","tue":"Marți","wed":"Miercuri","thu":"Joi","fri":"Vineri","sat":"Sâmbătă","sun":"Duminică"}
ZI_ORD = ["mon","tue","wed","thu","fri","sat","sun"]
ZI_JS  = {"mon":1,"tue":2,"wed":3,"thu":4,"fri":5,"sat":6,"sun":0}

def hours_rows_html(hours_s):
    """Rânduri tabel program din structura de ore, cu grupare pe zile consecutive identice."""
    if hours_s == "nonstop":
        return '<tr data-d="-1"><td>Luni – Duminică</td><td>NON-STOP</td></tr>', "toate"
    def cell(v): return "Închis" if v is None else "%02d:00 – %02d:00" % (v[0], v[1])
    rows, i = [], 0
    while i < 7:
        j = i
        while j+1 < 7 and hours_s.get(ZI_ORD[j+1]) == hours_s.get(ZI_ORD[i]): j += 1
        zile = ZI_RO[ZI_ORD[i]] if i == j else ZI_RO[ZI_ORD[i]] + " – " + ZI_RO[ZI_ORD[j]]
        dlist = ",".join(str(ZI_JS[ZI_ORD[k]]) for k in range(i, j+1))
        rows.append('<tr data-d="%s"><td>%s</td><td>%s</td></tr>' % (dlist, zile, cell(hours_s.get(ZI_ORD[i]))))
        i = j+1
    return "\n".join(rows), "grupat"

def hours_js_obj(hours_s):
    """Obiect JS {0:[8,17],...} pt starea live; null = închis; 'NS' = nonstop."""
    if hours_s == "nonstop": return '"NS"'
    parts = []
    for k in ZI_ORD:
        v = hours_s.get(k)
        parts.append('%d:%s' % (ZI_JS[k], "null" if v is None else "[%d,%d]" % (v[0], v[1])))
    return "{" + ",".join(parts) + "}"

# ─────────────────────────────────────────────────────── presets per nișă
# Fiecare preset e un mockup aproape complet: copy, compozitor, servicii, ticker.
# Placeholder-ele {name}, {zona} se completează din datele leadului.
NICHE_PRESETS = {

 "florarie": dict(
   archetype="atelier", accent="#B42B62",
   eyebrow="Florărie de familie · {zona}", h1_a="Flori proaspete,", h1_wonk="legate cu mâna,", h1_b="pentru orice ocazie.",
   lead="Spune-ne ocazia și bugetul pe WhatsApp — buchetul te așteaptă împachetat în hârtie, cu bilet scris de mână.",
   ticker_label="În sezon acum", ticker=["hortensii","floarea-soarelui","lisianthus","trandafiri de grădină","dalii","garofițe","eucalipt proaspăt"],
   composer=dict(intro_title="Compune buchetul,", intro_wonk="noi îl legăm.",
     intro_sub="Alege mai jos — biletul se scrie singur și ajunge la noi pe WhatsApp.",
     base="Bună ziua! Aș dori un buchet", unit="buchetul",
     steps=[
       dict(key="ocazie", label="Care e ocazia?", options=[("Aniversare","pentru o aniversare"),("Pentru cineva drag","pentru o surpriză"),("Mulțumesc","ca mulțumire"),("Nuntă / botez","pentru o nuntă/botez"),("Condoleanțe","pentru condoleanțe"),("Doar așa","doar așa, fără ocazie")]),
       dict(key="buget", label="Buget orientativ", hint="(rămâne între noi)", options=[("până în 150 lei","buget până în 150 lei"),("150–250 lei","buget 150–250 lei"),("250–400 lei","buget 250–400 lei"),("peste 400 lei","buget peste 400 lei")]),
       dict(key="preluare", label="Cum îl primești?", options=[("Îl ridic eu","îl ridic eu de la voi"),("Livrare (dau adresa pe chat)","aș dori livrare — trimit adresa pe chat")]),
     ]),
   services=[
     dict(title="Buchete legate manual", desc="Flori de sezon, legate la comandă. Hârtie de împachetat, sfoară, bilet scris de mână.", tag="azi, din piață", img=IMG["flori_vaza"]),
     dict(title="Aranjamente florale", desc="Compoziții în vas sau cutie, pentru acasă, birou sau cadou.", tag="în vas sau cutie", img=IMG["flori_dark"]),
     dict(title="Nunți & botezuri", desc="Buchet de mireasă, lumânări, aranjamente de masă — stabilim totul împreună.", tag="cu programare", img=IMG["flori_nunta"]),
     dict(title="Livrare în București", desc="Noi legăm buchetul, tu ne dai adresa și mesajul pentru bilet.", tag="prin curier", img=IMG["flori_lalele"]),
   ],
   story=dict(eyebrow="Atelierul nostru", h2_a="Flori alese bucată cu bucată,", h2_wonk="aduse în zori.",
     body="Nu ținem flori „de ieri”: marfa sosește dimineața. Legăm fiecare buchet la comandă — iar dacă nu știi ce să alegi, spune-ne doar pentru cine e.",
     facts=["Marfă proaspătă în fiecare dimineață","Fiecare buchet e legat la comandă","Bilet scris de mână, gratuit"]),
   reviews=["„Am cerut «ceva frumos, fără să știu ce» — au ieșit cele mai frumoase flori pe care le-am dăruit.",
            "„Scris pe WhatsApp dimineața, la prânz buchetul era la ușă. Biletul de mână a impresionat-o cel mai tare.",
            "„Flori proaspete de fiecare dată — trec săptămânal și mereu găsesc altceva frumos."],
   images=dict(hero=IMG["flori_hero"], story=IMG["flori_dark"]),
   visit_kicker="Vino să miroși florile",
 ),

 "cizmarie": dict(
   archetype="atelier", accent="#9A5B2D",
   eyebrow="Atelier de cizmărie · {zona}", h1_a="Pantofii buni", h1_wonk="nu se aruncă —", h1_b="se repară.",
   lead="Talpă, tocuri, cusături, vopsit — adu-i la atelier sau trimite-ne o poză pe WhatsApp și îți spunem pe loc ce se poate face.",
   ticker_label="Reparăm zilnic", ticker=["talpă & pingele","tocuri și flecuri","cusături manuale","fermoare","vopsit & recondiționat","întins pantofi","genți & curele"],
   composer=dict(intro_title="Spune-ne ce reparăm,", intro_wonk="pe scurt.",
     intro_sub="Alege mai jos și trimite — cel mai simplu e cu o poză pe chat, răspundem cu prețul pe loc.",
     base="Bună ziua! Am nevoie de o reparație", unit="reparația",
     steps=[
       dict(key="obiect", label="Ce aduci la atelier?", options=[("Pantofi","la o pereche de pantofi"),("Cizme / ghete","la cizme sau ghete"),("Geantă","la o geantă"),("Curea","la o curea"),("Altceva din piele","la un obiect din piele")]),
       dict(key="problema", label="Care e problema?", options=[("Talpă / pingele","talpă sau pingele"),("Toc / flec","toc sau flec"),("Cusătură desfăcută","o cusătură desfăcută"),("Fermoar","fermoarul"),("Vopsit / recondiționat","vopsire / recondiționare"),("Nu știu — trimit poză","nu știu exact — trimit o poză pe chat")]),
       dict(key="urgenta", label="Cât de repede?", options=[("Nu mă grăbesc","fără grabă"),("Săptămâna asta","în cursul săptămânii"),("Urgent","cât mai urgent")]),
     ]),
   services=[
     dict(title="Talpă, pingele & flecuri", desc="Înlocuim ce s-a tocit cu materiale rezistente — pantofii țin ani de zile după.", tag="cel mai cerut", img=IMG["tap_cusatura"]),
     dict(title="Cusături & fermoare", desc="Cusături manuale refăcute, fermoare schimbate la ghete, genți și geci.", tag="reparații fine", img=IMG["tap_scaun"]),
     dict(title="Vopsit & recondiționat", desc="Redăm culoarea și viața pielii — pantofi, genți, curele.", tag="piele naturală", img=IMG["tap_hero"]),
     dict(title="Întins & ajustat", desc="Lărgim pantofii care strâng și ajustăm ce nu se așază bine.", tag="pe calapod", img=IMG["tap_clasic"]),
   ],
   story=dict(eyebrow="Meserie veche, făcută bine", h2_a="Un meșter, un calapod,", h2_wonk="lucru făcut ca lumea.",
     body="Reparăm încălțăminte de zeci de ani. Îți spunem sincer când merită reparat și când nu — și ce reparăm, ține.",
     facts=["Preț spus înainte, pe loc","Materiale rezistente, nu de fațadă","Sincer: îți spunem și când NU merită"]),
   reviews=["„Mi-au salvat pantofii preferați — arată mai bine ca noi.",
            "„Am trimis poză pe WhatsApp, mi-au zis prețul pe loc. A doua zi erau gata.",
            "„Lucru de meșter adevărat, se vede la cusătură."],
   images=dict(hero=IMG["tap_cusatura"], story=IMG["tap_hero"]),
   visit_kicker="Adu-i la atelier",
 ),

 "ceasornicarie": dict(
   archetype="atelier", accent="#A8781C",
   eyebrow="Ceasornicărie · {zona}", h1_a="Timpul se repară", h1_wonk="cu răbdare,", h1_b="nu cu grabă.",
   lead="Ceasuri mecanice, automatice sau quartz — diagnostic pe loc, preț spus înainte. Scrie-ne pe WhatsApp sau treci pe la atelier.",
   ticker_label="Lucrăm pe", ticker=["ceasuri mecanice","automatice","quartz","ceasuri de perete","pendule","baterii & garnituri","curele & brățări"],
   composer=dict(intro_title="Spune-ne ce ceas ai,", intro_wonk="noi îl trezim.",
     intro_sub="Alege mai jos — sau trimite direct o poză cu ceasul pe chat.",
     base="Bună ziua! Am un ceas care are nevoie de atenție", unit="ceasul",
     steps=[
       dict(key="tip", label="Ce fel de ceas?", options=[("Mecanic","un ceas mecanic"),("Automatic","un ceas automatic"),("Quartz (baterie)","un ceas quartz"),("De perete / pendulă","un ceas de perete")]),
       dict(key="problema", label="Ce face (sau nu face)?", options=[("S-a oprit","s-a oprit de tot"),("Rămâne în urmă","rămâne în urmă / o ia înainte"),("Baterie / garnituri","are nevoie de baterie"),("Curea / brățară","are nevoie de curea nouă"),("Revizie generală","are nevoie de revizie")]),
     ]),
   services=[
     dict(title="Reparații mecanisme", desc="Demontăm, curățăm, ungem și reglăm — mecanice, automatice, quartz.", tag="diagnostic pe loc", img=IMG["gen_2"]),
     dict(title="Baterii & etanșare", desc="Baterie schimbată corect, cu garnituri verificate.", tag="5 minute", img=IMG["gen_1"]),
     dict(title="Curele & brățări", desc="Curele de piele, metal sau silicon, ajustate pe încheietura ta.", tag="pe măsură", img=IMG["tap_volan"]),
     dict(title="Ceasuri de familie", desc="Pendule și ceasuri vechi readuse la viață, cu piese potrivite.", tag="cu suflet", img=IMG["tap_clasic"]),
   ],
   story=dict(eyebrow="Atelierul", h2_a="Meserie de precizie,", h2_wonk="făcută la lupă.",
     body="Un ceas bun merită reparat, nu înlocuit. Îl deschidem, îți arătăm ce are și îți spunem prețul înainte să atingem ceva.",
     facts=["Diagnostic gratuit, pe loc","Preț spus înainte de orice lucrare","Piese potrivite, nu improvizate"]),
   reviews=["„Ceasul bunicului meu ticăie din nou. Nu credeam că se mai poate.",
            "„Mi-au arătat exact ce avea și cât costă, înainte să înceapă.",
            "„Baterie + garnituri în 10 minute, cu verificare de etanșare."],
   images=dict(hero=IMG["gen_2"], story=IMG["gen_1"]),
   visit_kicker="Treci pe la atelier",
 ),

 "tapiterie": dict(
   archetype="atelier", accent="#B4632B",
   eyebrow="Tapițerie auto · {zona}", h1_a="Interiorul mașinii,", h1_wonk="refăcut de mână,", h1_b="ca din fabrică.",
   lead="Scaune, plafon, volan — piele sau textil, cusătură de meșter. Trimite o poză pe WhatsApp și primești o evaluare pe loc.",
   ticker_label="Lucrăm pe", ticker=["scaune piele & textil","plafoane","volane îmbrăcate","vopsire piele","reparații arsuri","interioare clasice"],
   composer=dict(intro_title="Spune-ne ce refacem,", intro_wonk="în 3 atingeri.",
     intro_sub="Alege mai jos — cu o poză pe chat, evaluarea vine pe loc.",
     base="Bună ziua! Aș dori o lucrare de tapițerie", unit="lucrarea",
     steps=[
       dict(key="element", label="Ce refacem?", options=[("Scaune","la scaune"),("Plafon","la plafon"),("Volan","la volan"),("Panouri uși","la panourile de uși"),("Tot interiorul","la tot interiorul")]),
       dict(key="material", label="Ce material?", options=[("Piele naturală","cu piele naturală"),("Ecopiele","cu ecopiele"),("Alcantara","cu alcantara"),("Textil","cu textil"),("Nu știu — mă sfătuiți voi","nu știu — aștept recomandarea voastră")]),
       dict(key="cand", label="Când?", options=[("Săptămâna asta","săptămâna aceasta"),("Nu mă grăbesc","fără grabă"),("Vreau întâi un preț","momentan doar pentru preț")]),
     ]),
   services=[
     dict(title="Scaune piele & textil", desc="Refacem scaunele de la zero — ca originalul sau într-un design nou.", tag="cel mai cerut", img=IMG["tap_scaun"]),
     dict(title="Plafoane", desc="Plafon căzut sau pătat? Îl întindem pe material nou, fixat definitiv.", tag="rezolvare definitivă", img=IMG["tap_hero"]),
     dict(title="Volane îmbrăcate", desc="Piele nouă cusută manual, grip mai bun, aspect premium.", tag="cusut manual", img=IMG["tap_volan"]),
     dict(title="Reparații & vopsire piele", desc="Arsuri, tăieturi, uzură — petice invizibile și recolorare.", tag="fără schimbat tot", img=IMG["tap_cusatura"]),
   ],
   story=dict(eyebrow="Atelierul", h2_a="Cusătura spune", h2_wonk="tot adevărul.",
     body="Lucrăm manual, cu materiale alese pe proiect. Vino să vezi mostre de piele și cusături înainte să te decizi.",
     facts=["Mostre reale de piele și ață, la atelier","Preț ferm după evaluare, nu surprize","Lucrăm și interioare clasice / de colecție"]),
   reviews=["„Scaunele arată ca la mașină nouă. Cusătura e artă curată.",
            "„Plafonul căzut de ani de zile — rezolvat într-o zi.",
            "„Poză trimisă seara, preț primit în 10 minute, programare a doua zi."],
   images=dict(hero=IMG["tap_hero"], story=IMG["tap_cusatura"]),
   visit_kicker="Vino cu mașina la atelier",
 ),

 "mobila": dict(
   archetype="atelier", accent="#8C5A2E",
   eyebrow="Mobilă la comandă · {zona}", h1_a="Mobilă pe milimetru,", h1_wonk="gândită de tine,", h1_b="făcută de noi.",
   lead="Bucătării, dressinguri, mobilier pe spațiul tău exact. Trimite dimensiunile sau o schiță pe WhatsApp și primești o estimare.",
   ticker_label="Proiectăm & montăm", ticker=["bucătării","dressinguri","dulapuri în nișă","mobilier living","birouri","măsurători la domiciliu"],
   composer=dict(intro_title="Pornește proiectul,", intro_wonk="în 3 alegeri.",
     intro_sub="Alege mai jos — apoi discutăm pe chat schița și dimensiunile.",
     base="Bună ziua! Aș dori mobilă la comandă", unit="proiectul",
     steps=[
       dict(key="piesa", label="Ce construim?", options=[("Bucătărie","o bucătărie"),("Dressing","un dressing"),("Dulap în nișă","un dulap în nișă"),("Mobilier living","mobilier de living"),("Altceva","altceva — detaliez pe chat")]),
       dict(key="stadiu", label="În ce stadiu ești?", options=[("Am dimensiunile","am dimensiunile măsurate"),("Am doar ideea","am doar ideea — vreau măsurători"),("Am schiță/proiect","am o schiță sau un proiect")]),
       dict(key="cand", label="Când ai vrea montajul?", options=[("Luna asta","luna aceasta"),("În 2–3 luni","în 2–3 luni"),("Doar mă interesez","momentan doar mă interesez de preț")]),
     ]),
   services=[
     dict(title="Bucătării la comandă", desc="Proiectate pe spațiul tău, cu feronerie bună și finisaje la alegere.", tag="proiect 3D", img=IMG["casa_2"]),
     dict(title="Dressinguri & dulapuri", desc="Fiecare centimetru folosit — uși culisante sau clasice.", tag="pe nișă", img=IMG["casa_1"]),
     dict(title="Mobilier living & birou", desc="Biblioteci, comode, birouri — asortate cu restul casei.", tag="unitar", img=IMG["gen_1"]),
     dict(title="Măsurători & montaj", desc="Venim, măsurăm, montăm curat — cu garanție pe lucrare.", tag="totul inclus", img=IMG["rep_3"]),
   ],
   story=dict(eyebrow="Atelierul", h2_a="Milimetrul face", h2_wonk="diferența.",
     body="Mobila bună începe cu măsurătoarea corectă. Venim la tine, desenăm proiectul și îl execuți exact cum l-ai aprobat.",
     facts=["Măsurători la domiciliu","Proiect aprobat înainte de execuție","Montaj curat, cu garanție"]),
   reviews=["„Bucătăria arată exact ca în proiect. Fiecare sertar se închide perfect.",
            "„Au folosit o nișă imposibilă — acum e cel mai util dulap din casă.",
            "„Comunicare pe WhatsApp la fiecare pas, montaj fără praf și fără stres."],
   images=dict(hero=IMG["casa_2"], story=IMG["casa_1"]),
   visit_kicker="Hai să măsurăm",
 ),

 "parbrize": dict(
   archetype="urgent",
   eyebrow="Parbrize & geamuri auto · {zona}", h1_a="Parbriz spart?", h1_wonk="Montăm azi.", h1_b="",
   lead="Parbrize, lunete și geamuri laterale pentru orice mașină. Sună sau trimite locația pe WhatsApp — venim sau te programăm imediat.",
   ticker_label="Intervenim pentru", ticker=["parbrize","lunete","geamuri laterale","chip-uri & fisuri","senzori & cameră recalibrate","orice marcă"],
   composer=dict(intro_title="Spune-ne ce s-a spart —", intro_wonk="rezolvăm azi.",
     intro_sub="3 atingeri și mesajul pleacă. Răspundem imediat în program.",
     base="Bună ziua! Am o urgență cu geamurile mașinii", unit="intervenția",
     steps=[
       dict(key="element", label="Ce s-a spart?", options=[("Parbriz","parbrizul"),("Lunetă","luneta"),("Geam lateral","un geam lateral"),("Doar o fisură/chip","doar o fisură sau un chip")]),
       dict(key="masina", label="Ce mașină?", options=[("Autoturism","la un autoturism"),("SUV / 4x4","la un SUV"),("Utilitară / dubă","la o utilitară"),("Camion","la un camion")]),
       dict(key="unde", label="Unde ești?", options=[("Vin eu la voi","pot veni eu la atelier"),("Trimit locația pe chat","trimit locația pe chat — mașina nu se poate deplasa")]),
     ]),
   services=[
     dict(title="Parbrize montate pe loc", desc="Stoc pentru majoritatea modelelor — montaj cu adeziv profesional, gata în aceeași zi.", tag="azi", img=IMG["auto_far"]),
     dict(title="Lunete & geamuri laterale", desc="Înlocuire rapidă, cu curățarea completă a cioburilor.", tag="rapid", img=IMG["auto_dark"]),
     dict(title="Reparații chip & fisuri", desc="Fisurile mici se repară fără schimbarea parbrizului — dacă vii la timp.", tag="economisești", img=IMG["auto_road"]),
     dict(title="Recalibrare senzori", desc="Cameră și senzori de ploaie recalibrate după montaj.", tag="ADAS", img=IMG["det_lac"]),
   ],
   story=dict(eyebrow="De ce noi", h2_a="Când e spart,", h2_wonk="contează ora.",
     body="De-aia răspundem repede, avem stoc și lucrăm curat. Spune-ne modelul și anul — îți confirmăm pe loc dacă avem geamul.",
     facts=["Răspundem imediat în program","Stoc pentru modelele uzuale","Montaj cu materiale profesionale"]),
   reviews=["„Parbriz spart dimineața, la prânz eram pe drum cu unul nou.",
            "„Au venit unde eram — n-am mișcat mașina deloc.",
            "„Preț corect, exact cât au zis pe WhatsApp."],
   images=dict(hero=IMG["auto_far"], story=IMG["auto_dark"]),
   visit_kicker="Sau vino direct la noi",
 ),

 "electrica_auto": dict(
   archetype="urgent",
   eyebrow="Electrică auto & diagnoză · {zona}", h1_a="Nu pornește?", h1_wonk="Găsim de ce.", h1_b="",
   lead="Diagnoză computerizată, instalații electrice, alternatoare, electromotoare. Spune-ne simptomul pe WhatsApp — venim sau te programăm.",
   ticker_label="Rezolvăm", ticker=["diagnoză tester","nu pornește","baterie & alternator","electromotor","instalație electrică","senzori & becuri martor"],
   composer=dict(intro_title="Descrie simptomul —", intro_wonk="noi punem diagnosticul.",
     intro_sub="Alege mai jos și trimite. Cu anul și modelul mașinii în chat, mergem și mai repede.",
     base="Bună ziua! Am o problemă electrică la mașină", unit="intervenția",
     steps=[
       dict(key="simptom", label="Ce face mașina?", options=[("Nu pornește deloc","nu pornește deloc"),("Porneste greu","pornește greu"),("Bec martor aprins","are un bec martor aprins"),("Se descarcă bateria","i se descarcă bateria"),("Altceva","altceva — detaliez pe chat")]),
       dict(key="unde", label="Unde e mașina?", options=[("Pot veni la voi","pot veni la atelier"),("E blocată — veniți voi","e blocată — trimit locația pe chat")]),
       dict(key="cand", label="Cât de urgent?", options=[("Chiar acum","chiar acum"),("Azi","astăzi"),("Zilele astea","în zilele următoare")]),
     ]),
   services=[
     dict(title="Diagnoză computerizată", desc="Citim erorile cu tester profesional și îți explicăm pe românește ce au găsit.", tag="rapid", img=IMG["rep_1"]),
     dict(title="Alternatoare & electromotoare", desc="Reparate sau înlocuite — cu piesa potrivită, nu improvizată.", tag="cauza, nu efectul", img=IMG["rep_2"]),
     dict(title="Instalații electrice", desc="Scurtcircuite, trasee arse, consum anormal — găsim firul cu probleme.", tag="migală", img=IMG["rep_3"]),
     dict(title="Intervenție la domiciliu", desc="Când mașina nu se mișcă, venim noi cu testerul la ea.", tag="mobil", img=IMG["auto_road"]),
   ],
   story=dict(eyebrow="De ce noi", h2_a="Electrică fără ghicit:", h2_wonk="măsurăm, nu schimbăm la nimereală.",
     body="Nu înlocuim piese la întâmplare. Măsurăm, găsim cauza și abia apoi reparăm — de-aia problema nu se întoarce.",
     facts=["Tester profesional, nu cititor de erori de buzunar","Explicăm pe românește ce are mașina","Piese schimbate doar când e nevoie"]),
   reviews=["„Trei service-uri au schimbat piese degeaba. Ei au găsit firul ars în 40 de minute.",
            "„Au venit la mine în parcare, mașina pornea în ora aia.",
            "„Mi-au arătat pe tester exact ce era — fără povești."],
   images=dict(hero=IMG["rep_1"], story=IMG["rep_2"]),
   visit_kicker="Sau adu mașina la noi",
 ),

 "detailing": dict(
   archetype="studio",
   eyebrow="Studio detailing · {zona}", h1_a="Mașina ta,", h1_wonk="în cea mai bună zi a ei.", h1_b="",
   lead="Polish, protecție ceramică, interioare refăcute în detaliu. Programează pe WhatsApp — locurile se ocupă repede.",
   ticker_label="În studio", ticker=["polish & corecție lac","protecție ceramică","detailing interior","tapițerie curățată","faruri polishate","folie PPF"],
   composer=dict(intro_title="Alege tratamentul —", intro_wonk="noi pregătim studioul.",
     intro_sub="3 atingeri și cererea de programare pleacă pe WhatsApp.",
     base="Bună ziua! Aș dori o programare la detailing", unit="programarea",
     steps=[
       dict(key="tratament", label="Ce își dorește mașina?", options=[("Polish & corecție","polish și corecție de lac"),("Protecție ceramică","protecție ceramică"),("Detailing interior","detailing interior complet"),("Pachet complet","pachetul complet in & out")]),
       dict(key="masina", label="Ce mașină e?", options=[("Hatchback / sedan","pentru un sedan"),("SUV","pentru un SUV"),("Sport / premium","pentru o mașină premium")]),
       dict(key="cand", label="Când ți-ar conveni?", options=[("Săptămâna asta","săptămâna aceasta"),("Weekend","în weekend"),("Când e primul loc liber","când aveți primul loc liber")]),
     ]),
   services=[
     dict(title="Polish & corecție lac", desc="Scoatem zgârieturile fine și redăm adâncimea culorii, în trepte controlate.", tag="transformare", img=IMG["det_lac"]),
     dict(title="Protecție ceramică", desc="Strat ceramic aplicat în condiții de studio — luciu și protecție ani, nu luni.", tag="premium", img=IMG["det_hero"]),
     dict(title="Detailing interior", desc="Tapițerie, plastice, piele — curățate și hrănite până la ultimul detaliu.", tag="ca nouă", img=IMG["det_interior"]),
     dict(title="Spălare de studio", desc="Spălare atentă, în doi pași, cu uscare fără urme.", tag="întreținere", img=IMG["det_spuma"]),
   ],
   story=dict(eyebrow="Studioul", h2_a="Detaliul e", h2_wonk="tot spectacolul.",
     body="Lucrăm la lumină controlată, cu produse profesionale și timp suficient pentru fiecare mașină. Nu numărăm mașinile pe zi — numărăm rezultatele.",
     facts=["Lumină de inspecție în studio","Produse pro, aplicate cu răbdare","Poze înainte / după la fiecare lucrare"]),
   reviews=["„Am primit poze pe parcurs — transformarea e reală, nu marketing.",
            "„Ceramica aplicată acum un an arată tot impecabil.",
            "„Interiorul arăta obosit. Acum miroase și arată ca din showroom."],
   images=dict(hero=IMG["det_hero"], story=IMG["det_lac"]),
   visit_kicker="Programează o vizită",
 ),

 "vopsitorie": dict(
   archetype="studio", accent="#D64545",
   eyebrow="Vopsitorie & tinichigerie · {zona}", h1_a="După accident,", h1_wonk="ca înainte de el.", h1_b="",
   lead="Vopsitorie în cabină, tinichigerie și dosare de daună fără bătăi de cap. Trimite pozele mașinii pe WhatsApp pentru un deviz rapid.",
   ticker_label="Reparăm", ticker=["vopsitorie în cabină","tinichigerie","daune RCA & CASCO","polish final","înlocuiri elemente","deviz din poze"],
   composer=dict(intro_title="Trimite dauna —", intro_wonk="primești devizul.",
     intro_sub="Alege situația ta, apoi trimite pozele pe chat. Devizul vine rapid.",
     base="Bună ziua! Am nevoie de vopsitorie/tinichigerie", unit="devizul",
     steps=[
       dict(key="situatie", label="Ce s-a întâmplat?", options=[("Daună RCA (vinovat terț)","daună RCA — dosarul e pe asigurarea vinovatului"),("CASCO","daună CASCO"),("Plătesc eu","reparație plătită direct"),("Doar estimare","momentan vreau doar o estimare")]),
       dict(key="zona", label="Ce zonă a mașinii?", options=[("Bară / aripă","bară sau aripă"),("Ușă / prag","ușă sau prag"),("Capotă / plafon","capotă sau plafon"),("Mai multe elemente","mai multe elemente")]),
     ]),
   services=[
     dict(title="Daune RCA & CASCO", desc="Ne ocupăm noi de dosar și de discuția cu asiguratorul — tu aduci doar mașina.", tag="fără drumuri", img=IMG["vops_2"]),
     dict(title="Vopsitorie în cabină", desc="Culoare potrivită computerizat, uscare corectă, luciu uniform.", tag="nuanța exactă", img=IMG["vops_1"]),
     dict(title="Tinichigerie", desc="Îndreptăm și înlocuim elemente cu geometria respectată.", tag="pe schemă", img=IMG["auto_dark"]),
     dict(title="Finisaj & polish", desc="Predăm mașina polishată, cu tranziții invizibile.", tag="predare curată", img=IMG["det_lac"]),
   ],
   story=dict(eyebrow="De ce noi", h2_a="Reparăm mașina", h2_wonk="și actele.",
     body="Partea grea la o daună nu e vopsitul — e birocrația. O preluăm noi: dosar, poze, constatare, iar tu primești mașina gata.",
     facts=["Dosar de daună gestionat integral","Deviz din poze, pe WhatsApp","Nuanță potrivită computerizat"]),
   reviews=["„Dosar RCA rezolvat de ei cap-coadă — eu doar am adus mașina.",
            "„Nuanța e perfectă, nu se vede nicio tranziție.",
            "„Deviz corect din poze, fără surprize la final."],
   images=dict(hero=IMG["vops_1"], story=IMG["vops_2"]),
   visit_kicker="Adu mașina la evaluare",
 ),

 "spalatorie": dict(
   archetype="studio", accent="#1F8FE0",
   eyebrow="Spălătorie auto · {zona}", h1_a="Curat", h1_wonk="ca scos din folie,", h1_b="de fiecare dată.",
   lead="Spălare atentă interior & exterior, cu program lung și prețuri corecte. Întreabă pe WhatsApp cât durează chiar acum.",
   ticker_label="Facem zilnic", ticker=["spălare exterior","interior complet","ceruire","curățare tapițerie","jante & anvelope","motor"],
   composer=dict(intro_title="Alege pachetul —", intro_wonk="mașina intră la rând.",
     intro_sub="Trimite și îți răspundem cu cât e de așteptat chiar acum.",
     base="Bună ziua! Aș dori o spălare", unit="programarea",
     steps=[
       dict(key="pachet", label="Ce pachet vrei?", options=[("Exterior","exterior"),("Interior + exterior","interior + exterior"),("Complet cu ceruire","completă, cu ceruire"),("Curățare tapițerie","cu curățare de tapițerie")]),
       dict(key="masina", label="Ce mașină?", options=[("Mică / compactă","pentru o mașină compactă"),("Sedan / break","pentru un sedan"),("SUV / dubă","pentru un SUV sau o dubă")]),
     ]),
   services=[
     dict(title="Exterior cu atenție", desc="Prespălare, spumă activă, uscare manuală — fără zgârieturi de perie.", tag="manual", img=IMG["det_spuma"]),
     dict(title="Interior complet", desc="Aspirare, plastice, geamuri, praguri — mașina miroase a curat.", tag="detaliu", img=IMG["det_interior"]),
     dict(title="Ceruire & protecție", desc="Ceară aplicată corect — apa fuge, praful nu se lipește.", tag="luciu", img=IMG["det_lac"]),
     dict(title="Tapițerie & pete", desc="Injecție-extracție pentru scaune și mochete cu pete vechi.", tag="profund", img=IMG["det_hero"]),
   ],
   story=dict(eyebrow="De ce la noi", h2_a="Aceeași grijă,", h2_wonk="la fiecare mașină.",
     body="Program lung, echipă stabilă și materiale bune. Mașina ta nu e „încă una la rând” — e cartea noastră de vizită.",
     facts=["Program lung, 7 zile din 7","Echipă stabilă, nu sezonieri","Materiale profesionale, nu diluate"]),
   reviews=["„Cea mai atentă spălătorie din zonă — se vede la detalii.",
            "„Mi-au scos pete din tapițerie pe care le credeam permanente.",
            "„Întreb pe WhatsApp cât e de așteptat și vin fix la timp."],
   images=dict(hero=IMG["det_spuma"], story=IMG["det_interior"]),
   visit_kicker="Treci pe la noi",
 ),

 "optica": dict(
   archetype="studio", accent="#7A4BD6",
   eyebrow="Optică medicală · {zona}", h1_a="Vezi bine,", h1_wonk="arăți și mai bine.", h1_b="",
   lead="Consultații optometrice, lentile potrivite corect și rame alese pe fizionomia ta. Programează-te pe WhatsApp.",
   ticker_label="În magazin", ticker=["consult optometric","lentile la comandă","rame de vedere","ochelari de soare","ajustări & reparații","lentile de contact"],
   composer=dict(intro_title="Programează-te —", intro_wonk="vederea nu așteaptă.",
     intro_sub="Alege mai jos și trimite. Confirmăm ora pe chat.",
     base="Bună ziua! Aș dori o programare la optică", unit="programarea",
     steps=[
       dict(key="serviciu", label="Pentru ce vii?", options=[("Consult + ochelari noi","consult și ochelari noi"),("Doar consult","doar consultul optometric"),("Schimb lentilele","schimbarea lentilelor la rama mea"),("Reparație / ajustare","o reparație sau ajustare")]),
       dict(key="cand", label="Când îți convine?", options=[("Dimineața","dimineața"),("După-amiaza","după-amiaza"),("Sâmbătă","sâmbăta")]),
     ]),
   services=[
     dict(title="Consult optometric", desc="Verificarea completă a vederii, cu aparatură modernă și răbdare.", tag="programare", img=IMG["gen_1"]),
     dict(title="Lentile la comandă", desc="Monofocale, progresive, subțiate — montate corect pe centrii optici.", tag="precizie", img=IMG["gen_2"]),
     dict(title="Rame pe fizionomie", desc="Te ajutăm să alegi rama care ți se potrivește — nu doar care e la modă.", tag="stil", img=IMG["casa_1"]),
     dict(title="Ajustări & reparații", desc="Strângem, îndreptăm, schimbăm plăcuțe — de multe ori pe loc.", tag="pe loc", img=IMG["rep_3"]),
   ],
   story=dict(eyebrow="Magazinul", h2_a="Ochelarii corecți", h2_wonk="îți schimbă ziua.",
     body="O dioptrie corect măsurată și lentile centrate cum trebuie fac diferența dintre „ochelari” și „ochelarii tăi”.",
     facts=["Măsurători atente, fără grabă","Montaj corect pe centrii optici","Ajustări gratuite după cumpărare"]),
   reviews=["„Primul consult în care mi s-a explicat tot, pas cu pas.",
            "„Progresivele făcute aici sunt primele pe care le port cu plăcere.",
            "„Mi-au reparat pe loc ochelarii călcați — gratuit."],
   images=dict(hero=IMG["gen_1"], story=IMG["gen_2"]),
   visit_kicker="Programează un consult",
 ),

 "kineto": dict(
   archetype="cabinet",
   eyebrow="Kinetoterapie & recuperare · {zona}", h1_a="Corpul tău știe drumul.", h1_wonk="Noi îl ghidăm.", h1_b="",
   lead="Recuperare după accidentări sau operații, dureri de spate, postură. Ședințe 1-la-1, cu plan personalizat.",
   ticker_label="Lucrăm cu", ticker=["dureri de spate","recuperare post-operatorie","umăr & genunchi","postură","masaj terapeutic","mobilitate"],
   composer=dict(intro_title="Spune-ne unde doare —", intro_wonk="facem un plan.",
     intro_sub="Alege mai jos. Prima discuție e de evaluare — vedem împreună de unde pornim.",
     base="Bună ziua! Aș dori o programare la kinetoterapie", unit="programarea",
     steps=[
       dict(key="problema", label="Cu ce te putem ajuta?", options=[("Dureri de spate","pentru dureri de spate"),("Recuperare post-operație","pentru recuperare post-operatorie"),("Umăr / genunchi","pentru o problemă la umăr sau genunchi"),("Postură","pentru corectarea posturii"),("Masaj terapeutic","pentru masaj terapeutic")]),
       dict(key="vechime", label="De când te supără?", options=[("Recent (zile)","de câteva zile"),("Câteva săptămâni","de câteva săptămâni"),("Cronic (luni/ani)","de luni sau ani")]),
       dict(key="cand", label="Când poți ajunge?", options=[("Dimineața","dimineața"),("La prânz","în jurul prânzului"),("După program (17+)","după ora 17")]),
     ]),
   services=[
     dict(title="Evaluare & plan personal", desc="Prima ședință: testăm, măsurăm și stabilim obiective realiste.", tag="prima ședință", img=IMG["rep_1"]),
     dict(title="Kinetoterapie 1-la-1", desc="Exerciții ghidate, corectate în timp real — nu fișe generice.", tag="individual", img=IMG["casa_2"]),
     dict(title="Masaj terapeutic", desc="Lucrăm țintit pe zonele tensionate, în sprijinul recuperării.", tag="țintit", img=IMG["casa_1"]),
     dict(title="Recuperare post-operatorie", desc="Protocoale adaptate indicațiilor medicului tău chirurg.", tag="în siguranță", img=IMG["gen_1"]),
   ],
   story=dict(eyebrow="Cabinetul", h2_a="Recuperarea e un drum —", h2_wonk="nu o minune.",
     body="Progresul vine din constanță și exerciții corecte. Îți construim planul, îl ajustăm pe parcurs și te învățăm să continui acasă.",
     facts=["Ședințe individuale, nu pe bandă","Plan scris, cu obiective măsurabile","Exerciții pentru acasă incluse"]),
   reviews=["„După operația la genunchi, am revenit la alergat în 4 luni. Plan clar, progres constant.",
            "„Durerea de spate cu care trăiam de ani — controlată în 8 ședințe.",
            "„Îți explică fiecare exercițiu: ce lucrează și de ce contează."],
   images=dict(hero=IMG["casa_2"], story=IMG["rep_1"]),
   visit_kicker="Programează evaluarea",
 ),

 "reparatii_electro": dict(
   archetype="cabinet", accent="#2E7DD1",
   eyebrow="Reparații electrocasnice · {zona}", h1_a="S-a stricat?", h1_wonk="Reparăm la tine acasă.", h1_b="",
   lead="Mașini de spălat, frigidere, uscătoare — diagnostic la domiciliu și reparație pe loc, cu piese aduse la a doua vizită dacă e nevoie.",
   ticker_label="Reparăm", ticker=["mașini de spălat","frigidere & combine","uscătoare","mașini de vase","plite & cuptoare","la domiciliu"],
   composer=dict(intro_title="Descrie defectul —", intro_wonk="venim cu scula potrivită.",
     intro_sub="Alege mai jos. Cu marca și modelul în chat, venim pregătiți cu piese.",
     base="Bună ziua! Am un electrocasnic defect", unit="intervenția",
     steps=[
       dict(key="aparat", label="Ce aparat e?", options=[("Mașină de spălat","mașina de spălat"),("Frigider / combină","frigiderul"),("Uscător","uscătorul"),("Mașină de vase","mașina de vase"),("Plită / cuptor","plita sau cuptorul")]),
       dict(key="simptom", label="Ce face?", options=[("Nu pornește","nu pornește deloc"),("Face zgomot","face zgomot anormal"),("Curge apă","curge apă"),("Nu răcește / nu încălzește","nu răcește sau nu încălzește"),("Altceva","altceva — detaliez pe chat")]),
       dict(key="cand", label="Când să venim?", options=[("Azi dacă se poate","azi, dacă se poate"),("Mâine","mâine"),("În weekend","în weekend")]),
     ]),
   services=[
     dict(title="Diagnostic la domiciliu", desc="Venim, testăm și îți spunem pe loc ce are și cât costă.", tag="preț pe loc", img=IMG["rep_2"]),
     dict(title="Reparație pe loc", desc="Majoritatea defectelor se rezolvă din prima vizită.", tag="o vizită", img=IMG["rep_1"]),
     dict(title="Piese potrivite", desc="Folosim piese compatibile de calitate — cu garanție la lucrare.", tag="garanție", img=IMG["rep_3"]),
     dict(title="Sfat sincer", desc="Dacă reparația nu merită, îți spunem direct — nu reparăm de dragul facturii.", tag="onest", img=IMG["casa_2"]),
   ],
   story=dict(eyebrow="Cum lucrăm", h2_a="Reparat azi", h2_wonk="e mai ieftin ca înlocuit mâine.",
     body="Un rulment schimbat la timp salvează o mașină de spălat întreagă. Vino spre noi cu simptomul — te ajutăm rapid și corect.",
     facts=["Deplasare rapidă în tot orașul","Preț anunțat înainte de reparație","Garanție pe lucrare și piese"]),
   reviews=["„Mașina de spălat repornită în aceeași zi — rulment schimbat pe loc.",
            "„Mi-au zis sincer că nu merită reparat frigiderul vechi și ce să aleg în loc.",
            "„Au venit cu piesa potrivită din prima, știau modelul."],
   images=dict(hero=IMG["rep_2"], story=IMG["rep_1"]),
   visit_kicker="Cheamă tehnicianul",
 ),

 "gsm": dict(
   archetype="cabinet", accent="#4B64D8",
   eyebrow="Service GSM · {zona}", h1_a="Telefonul tău,", h1_wonk="reparat cât aștepți.", h1_b="",
   lead="Display-uri, baterii, mufe de încărcare — multe reparații se fac pe loc. Întreabă prețul pe WhatsApp înainte să vii.",
   ticker_label="Reparăm zilnic", ticker=["display-uri","baterii","mufe de încărcare","camere","carcase & sticle spate","deblocări"],
   composer=dict(intro_title="Spune-ne modelul —", intro_wonk="îți zicem prețul.",
     intro_sub="Alege mai jos, iar în chat scrie modelul exact. Răspundem cu preț și durată.",
     base="Bună ziua! Am un telefon de reparat", unit="reparația",
     steps=[
       dict(key="problema", label="Ce are telefonul?", options=[("Display spart","display-ul spart"),("Baterie slabă","bateria — se descarcă repede"),("Nu se încarcă","mufa — nu se mai încarcă"),("Camera","camera"),("Altceva","altceva — detaliez pe chat")]),
       dict(key="marca", label="Ce marcă?", options=[("iPhone","un iPhone"),("Samsung","un Samsung"),("Xiaomi / alt Android","un Android")]),
     ]),
   services=[
     dict(title="Display-uri", desc="Înlocuire cu ecrane de calitate, verificate — telefonul rămâne etanș.", tag="pe loc", img=IMG["gen_2"]),
     dict(title="Baterii", desc="Baterie nouă montată corect, cu verificarea consumului.", tag="30 min", img=IMG["rep_3"]),
     dict(title="Mufe & încărcare", desc="Curățare sau înlocuire mufă — de multe ori mai simplu decât pare.", tag="des întâlnit", img=IMG["rep_2"]),
     dict(title="Diagnoza gratuită", desc="Îți spunem ce are și cât costă înainte de orice intervenție.", tag="gratuit", img=IMG["gen_1"]),
   ],
   story=dict(eyebrow="Service-ul", h2_a="Fără telefonul tău", h2_wonk="nici noi nu plecăm acasă.",
     body="Știm cât de legat ești de el. De-aia reparăm rapid, cu piese verificate, și îți spunem mereu prețul înainte.",
     facts=["Diagnoză gratuită, preț înainte","Multe reparații gata pe loc","Garanție la piesele montate"]),
   reviews=["„Display schimbat în 40 de minute, cât am băut o cafea alături.",
            "„Preț spus pe WhatsApp, același preț la plată.",
            "„Mi-au recuperat telefonul pe care alt service l-a declarat mort."],
   images=dict(hero=IMG["gen_2"], story=IMG["rep_3"]),
   visit_kicker="Treci pe la service",
 ),

 "service_auto": dict(
   archetype="cabinet", accent="#C4622D",
   eyebrow="Service auto · {zona}", h1_a="Mecanici care explică,", h1_wonk="nu doar factură.", h1_b="",
   lead="Revizii, reparații și diagnoză cu preț anunțat înainte. Programează-te pe WhatsApp — știi mereu ce se lucrează la mașina ta.",
   ticker_label="În service", ticker=["revizii complete","frâne","distribuție","suspensie","diagnoză","pregătire ITP"],
   composer=dict(intro_title="Programează mașina —", intro_wonk="fără telefoane pierdute.",
     intro_sub="Alege mai jos. Modelul și anul, scrise în chat, ne ajută să pregătim piesele.",
     base="Bună ziua! Aș dori o programare la service", unit="programarea",
     steps=[
       dict(key="lucrare", label="Ce lucrare?", options=[("Revizie","o revizie completă"),("Frâne","la frâne"),("Distribuție","la distribuție"),("Diagnoză / verificare","o diagnoză"),("Pregătire ITP","pregătire pentru ITP")]),
       dict(key="cand", label="Când?", options=[("Cât mai repede","cât mai repede"),("Săptămâna asta","săptămâna aceasta"),("Îmi spuneți voi","când aveți primul loc")]),
     ]),
   services=[
     dict(title="Revizii cu fișă", desc="Primești lista exactă: ce s-a schimbat, ce urmează și când.", tag="transparent", img=IMG["rep_1"]),
     dict(title="Frâne & siguranță", desc="Plăcuțe, discuri, lichid — verificate și schimbate la timp.", tag="prioritate", img=IMG["auto_road"]),
     dict(title="Distribuție", desc="Kit complet, montat pe repere — cu poze la predare.", tag="cu dovezi", img=IMG["rep_2"]),
     dict(title="Diagnoză & ITP", desc="Verificăm mașina cum trebuie, nu doar să treacă.", tag="corect", img=IMG["rep_3"]),
   ],
   story=dict(eyebrow="Cum lucrăm", h2_a="Piesele vechi", h2_wonk="ți le dăm înapoi.",
     body="Transparența nu e un slogan: primești pozele lucrării, piesele schimbate și explicația pe românește. Așa se construiește încrederea.",
     facts=["Preț anunțat înainte de lucrare","Piesele vechi returnate la predare","Fișă de service după fiecare vizită"]),
   reviews=["„Primul service care mi-a arătat pozele lucrării fără să cer.",
            "„Deviz respectat la leu. Revin cu încredere.",
            "„Mi-au explicat ce NU trebuie schimbat încă — rar lucru."],
   images=dict(hero=IMG["rep_1"], story=IMG["rep_2"]),
   visit_kicker="Programează mașina",
 ),
}
# alias-uri utile
NICHE_PRESETS["masini_spalat"] = NICHE_PRESETS["reparatii_electro"]
NICHE_PRESETS["frigidere"] = NICHE_PRESETS["reparatii_electro"]
NICHE_PRESETS["vulcanizare"] = NICHE_PRESETS["parbrize"]

# ─────────────────────────────────────────────────────── CSS master (skin prin tokens + clase arhetip)
CSS = Template(r"""
:root{
  --bg:$bg; --bg2:$bg2; --card:$card; --ink:$ink; --ink2:$ink2; --ink3:$ink3;
  --line:$line; --lineink:$lineink; --mut:$mut; --mutink:$mutink;
  --accent:$accent; --accent-deep:$accent_deep; --soft:$soft; --pollen:$pollen; --stem:$stem;
  --wa:#1FA855; --d:$font_d; --s:$font_s; --r:$radius;
  --maxw:1180px; --pad:clamp(20px,4.5vw,48px); --ease:cubic-bezier(.22,.75,.25,1);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{font-family:var(--s);background:var(--bg);color:var(--ink);line-height:1.6;
  font-size:clamp(1rem,.96rem + .2vw,1.0625rem);-webkit-font-smoothing:antialiased;overflow-x:hidden}
img,svg{display:block;max-width:100%} img{height:auto}
a{color:inherit;text-decoration:none} ul,ol{list-style:none}
button{font:inherit;cursor:pointer;border:0;background:none;color:inherit}
:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:3px}
::selection{background:var(--accent);color:#fff}
.wrap{width:100%;max-width:var(--maxw);margin-inline:auto;padding-inline:var(--pad)}
.skip{position:fixed;left:14px;top:-60px;z-index:300;background:var(--ink);color:var(--bg);padding:10px 16px;border-radius:6px;font-weight:600;transition:top .2s}
.skip:focus{top:14px}
.eyebrow{font-size:.72rem;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:var(--accent)}
h1,h2,h3{font-family:var(--d);line-height:1.06;letter-spacing:-.015em;font-weight:460}
h2{font-size:clamp(1.9rem,1.25rem + 3vw,3.05rem)}
.sub{color:var(--mut);max-width:54ch}
.wonk{font-style:italic;color:var(--accent)}
.arch-atelier .wonk{font-variation-settings:"SOFT" 60,"WONK" 1}
.arch-urgent h1,.arch-urgent h2{font-weight:860;letter-spacing:-.01em;text-transform:uppercase;font-stretch:112%}
.arch-urgent .wonk{font-style:normal;color:var(--accent)}
.arch-studio h1,.arch-studio h2{font-weight:600;letter-spacing:-.03em}
.arch-studio .wonk{font-style:normal;color:var(--accent)}
.arch-cabinet .wonk{font-style:italic;color:var(--accent)}

/* butoane */
.btn{display:inline-flex;align-items:center;gap:.55rem;font-weight:650;font-size:1rem;padding:.9em 1.45em;
  border-radius:999px;border:1.5px solid transparent;white-space:nowrap;
  transition:transform .22s var(--ease),box-shadow .22s,background .22s,border-color .22s,color .22s}
.btn svg{width:1.15em;height:1.15em;flex:none}
.btn:active{transform:translateY(1px) scale(.99)}
.btn-wa{background:var(--wa);color:#fff;box-shadow:0 14px 30px -14px rgba(31,168,85,.55)}
.btn-wa svg{fill:currentColor}
.btn-wa:hover{transform:translateY(-2px);box-shadow:0 20px 36px -14px rgba(31,168,85,.6)}
.btn-ink{background:var(--ink);color:var(--bg)} .btn-ink svg{fill:currentColor}
.btn-ink:hover{transform:translateY(-2px)}
.arch-urgent .btn-ink{background:var(--accent);color:#141414}
.btn-ghost{border-color:var(--ink);color:var(--ink);background:transparent} .btn-ghost svg{fill:currentColor}
.btn-ghost:hover{background:var(--ink);color:var(--bg)}
.arch-urgent .btn-ghost{border-color:var(--ink3);color:var(--ink)}
.arch-urgent .btn-ghost:hover{background:var(--ink);color:#141414}

/* topline live */
.topline{background:var(--ink);color:var(--mutink);font-size:.8rem}
.arch-urgent .topline{background:var(--accent);color:#141414}
.arch-urgent .topline a,.arch-urgent .topline .status{color:#141414;font-weight:700}
.topline .wrap{display:flex;align-items:center;justify-content:space-between;gap:14px;min-height:36px;padding-block:5px}
.status{display:inline-flex;align-items:center;gap:.5rem;color:var(--bg2);font-weight:500}
.arch-urgent .status{color:#141414}
.status .dot{width:8px;height:8px;border-radius:50%;background:var(--pollen);flex:none}
.status.open .dot{background:#37C871;animation:puls 2.4s infinite}
.arch-urgent .status .dot{background:#141414}
@keyframes puls{0%{box-shadow:0 0 0 0 rgba(55,200,113,.45)}70%{box-shadow:0 0 0 8px rgba(55,200,113,0)}100%{box-shadow:0 0 0 0 rgba(55,200,113,0)}}
.topline a{color:var(--bg2);font-weight:500;white-space:nowrap}

/* masthead */
.mast{position:sticky;top:0;z-index:120;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.mast .wrap{display:flex;align-items:center;justify-content:space-between;gap:18px;height:72px}
.markx{display:flex;align-items:baseline;flex-wrap:wrap;font-family:var(--d);font-size:clamp(1.02rem,.82rem + .55vw,1.42rem);line-height:1.05;max-width:340px}
.arch-urgent .markx{font-weight:860;text-transform:uppercase;font-stretch:112%}
.markx .amp{font-style:italic;color:var(--accent);font-size:1.2em;margin-inline:.1em}
.arch-atelier .markx .amp{font-variation-settings:"SOFT" 60,"WONK" 1}
.markx small{font-family:var(--s);font-size:.6rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--mut);margin-left:.7rem;transform:translateY(-2px)}
.nav{display:flex;gap:1.6rem}
.nav a{font-weight:500;font-size:.94rem;color:var(--ink3);position:relative;padding:4px 0}
.nav a::after{content:"";position:absolute;left:0;right:100%;bottom:0;height:1.5px;background:var(--accent);transition:right .25s var(--ease)}
.nav a:hover{color:var(--ink)} .nav a:hover::after{right:0}
.mast-cta{display:flex;align-items:center;gap:10px}
.mast-cta .btn{padding:.62em 1.1em;font-size:.92rem}
.burger{display:none;width:44px;height:44px;border:1px solid var(--line);border-radius:10px;flex-direction:column;gap:5px;align-items:center;justify-content:center}
.burger span{width:18px;height:1.6px;background:var(--ink)}

/* proof + stele */
.proof{display:flex;align-items:center;gap:.6rem;color:var(--ink3);font-size:.95rem;font-weight:500}
.stars{display:inline-flex;gap:2px} .stars svg{width:17px;height:17px;fill:var(--pollen)}
.proof b{font-family:var(--d);font-size:1.15rem}

/* ——— HERO: split_arch (atelier) ——— */
.hero-a{padding:clamp(44px,7vw,90px) 0 clamp(40px,6vw,72px);overflow:hidden}
.hero-a .wrap{display:grid;grid-template-columns:1.05fr .95fr;gap:clamp(28px,5vw,72px);align-items:center}
.hero-a h1{font-size:clamp(2.6rem,1.4rem + 5.4vw,5.1rem);margin:1.1rem 0 1.3rem}
.arch-atelier .hero-a h1{font-variation-settings:"opsz" 144}
.hero-a h1 .ln{display:block;overflow:hidden}
.hero-a h1 .ln>span{display:inline-block;transform:translateY(112%);animation:rise .9s var(--ease) forwards}
.hero-a h1 .ln:nth-child(2)>span{animation-delay:.1s}
.hero-a h1 .ln:nth-child(3)>span{animation-delay:.2s}
@keyframes rise{to{transform:none}}
.hero-a .lead{font-size:1.08rem;color:var(--mut);max-width:46ch;margin-bottom:1.8rem}
.hero-cta{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:1.5rem}
.hfig{position:relative}
.hfig .main{border-radius:999px 999px 22px 22px;overflow:hidden;box-shadow:0 34px 70px -30px rgba(0,0,0,.45);animation:bloom 1.1s var(--ease) both .15s}
@keyframes bloom{from{clip-path:inset(6% round 999px 999px 22px 22px);opacity:.4}to{clip-path:inset(0 round 999px 999px 22px 22px);opacity:1}}
.hfig .main img{width:100%;aspect-ratio:4/5.1;object-fit:cover}
.hfig .notecard{position:absolute;left:-14px;bottom:26px;background:var(--card);border:1px solid var(--line);border-radius:10px;
  padding:12px 16px 12px 14px;max-width:230px;transform:rotate(-2.4deg);box-shadow:0 18px 34px -18px rgba(0,0,0,.35);display:flex;gap:10px;align-items:center}
.hfig .notecard svg{width:30px;height:30px;flex:none}
.hfig .notecard p{font-family:var(--d);font-style:italic;font-size:.92rem;line-height:1.35;color:var(--ink2)}
.hfig .badge{position:absolute;right:6px;top:10px;background:var(--bg);border:1px solid var(--line);border-radius:999px;
  font-size:.7rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;padding:.55em 1em;color:var(--ink3);transform:rotate(3deg)}
.fl{fill:none;stroke:var(--accent);stroke-width:1.6;stroke-linecap:round}

/* ——— HERO: phone_first (urgent) ——— */
.hero-u{padding:clamp(40px,6vw,76px) 0 clamp(36px,5vw,60px);position:relative;overflow:hidden}
.hero-u .wrap{display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(28px,5vw,64px);align-items:center}
.hero-u h1{font-size:clamp(2.5rem,1.3rem + 5.6vw,4.9rem);margin:1rem 0 1.1rem}
.hero-u .lead{color:var(--mut);max-width:48ch;margin-bottom:1.5rem}
.bigtel{display:inline-flex;align-items:center;gap:.5em;font-family:var(--d);font-weight:860;font-stretch:112%;
  font-size:clamp(1.9rem,1rem + 4vw,3.4rem);letter-spacing:.01em;color:var(--accent);margin-bottom:1.2rem}
.bigtel svg{width:.9em;height:.9em;fill:var(--accent)}
.bigtel:hover{color:var(--ink)} .bigtel:hover svg{fill:var(--ink)}
.hero-u .hfig2{position:relative}
.hero-u .hfig2 .main{clip-path:polygon(8% 0,100% 0,100% 100%,0 100%);border-radius:var(--r);overflow:hidden}
.hero-u .hfig2 img{width:100%;aspect-ratio:4/4.6;object-fit:cover;filter:saturate(.9) contrast(1.05)}
.hero-u .flag{position:absolute;right:14px;left:auto;top:14px;background:var(--accent);color:#141414;font-weight:800;
  letter-spacing:.14em;text-transform:uppercase;font-size:.72rem;padding:.6em 1.1em;border-radius:6px;transform:rotate(-3deg);
  box-shadow:0 14px 30px rgba(0,0,0,.4)}

/* ——— HERO: fullbleed (studio) ——— */
.hero-s{position:relative}
.hero-s .media{height:clamp(420px,62vh,640px);overflow:hidden;position:relative}
.hero-s .media img{width:100%;height:100%;object-fit:cover}
.hero-s .media::after{content:"";position:absolute;inset:0;background:linear-gradient(185deg,rgba(10,10,12,.05) 40%,rgba(10,10,12,.55))}
.hero-s .panel{position:relative;margin-top:clamp(-120px,-14vw,-70px);z-index:5}
.hero-s .panel-in{background:var(--card);border:1px solid var(--line);border-radius:calc(var(--r) + 4px);
  box-shadow:0 40px 80px -40px rgba(0,0,0,.35);padding:clamp(26px,4vw,46px);max-width:820px}
.hero-s h1{font-size:clamp(2.3rem,1.2rem + 4.6vw,4.2rem);margin:.9rem 0 1rem}
.hero-s .lead{color:var(--mut);max-width:56ch;margin-bottom:1.5rem}

/* ——— HERO: calm_card (cabinet) ——— */
.hero-c{padding:clamp(44px,6.5vw,84px) 0 0;text-align:center}
.hero-c .inner{max-width:760px;margin-inline:auto}
.hero-c h1{font-size:clamp(2.4rem,1.3rem + 4.8vw,4.3rem);margin:1rem 0 1.1rem}
.hero-c .lead{color:var(--mut);margin:0 auto 1.6rem;max-width:52ch}
.hero-c .hero-cta{justify-content:center}
.hero-c .proof{justify-content:center}
.hero-c .banner{margin-top:clamp(30px,4.5vw,52px);border-radius:calc(var(--r) + 8px) calc(var(--r) + 8px) 0 0;overflow:hidden}
.hero-c .banner img{width:100%;aspect-ratio:16/6.4;object-fit:cover}
.trustrow{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:1.4rem}
.trust{display:inline-flex;align-items:center;gap:.5rem;background:var(--card);border:1px solid var(--line);
  border-radius:999px;padding:.55em 1.1em;font-size:.88rem;font-weight:600;color:var(--ink3)}
.trust svg{width:16px;height:16px;fill:none;stroke:var(--accent);stroke-width:2.4;stroke-linecap:round}

/* ticker */
.season{background:var(--ink);color:var(--bg);overflow:hidden;border-block:1px solid var(--lineink)}
.arch-urgent .season{background:var(--bg2);color:var(--ink);border-color:var(--line)}
.season-in{position:relative;display:flex;align-items:center;min-height:52px}
.season .lbl{position:absolute;z-index:2;left:0;top:0;bottom:0;display:flex;align-items:center;gap:.5rem;background:inherit;
  background:var(--ink);padding:0 18px 0 var(--pad);font-size:.7rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--pollen);box-shadow:24px 0 24px -12px var(--ink)}
.arch-urgent .season .lbl{background:var(--bg2);color:var(--accent);box-shadow:24px 0 24px -12px var(--bg2)}
.tk{display:flex;width:max-content;animation:tk 34s linear infinite;padding-left:250px}
.season:hover .tk{animation-play-state:paused}
.tk span{display:inline-flex;align-items:center;font-family:var(--d);font-size:1.02rem;white-space:nowrap;color:var(--bg2)}
.arch-atelier .tk span{font-style:italic}
.arch-urgent .tk span{color:var(--ink3);font-weight:700;text-transform:uppercase;font-size:.9rem;letter-spacing:.06em}
.tk span::after{content:"•";color:var(--stem);margin:0 1.25em}
.arch-atelier .tk span::after{content:"✿"}
@keyframes tk{to{transform:translateX(-50%)}}

/* compozitor */
.comp{padding:clamp(60px,8vw,104px) 0;background:linear-gradient(var(--bg),var(--bg2) 140%)}
.comp-head{max-width:58ch;margin-bottom:clamp(28px,4vw,44px)}
.comp-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(26px,4vw,54px);align-items:start}
.step{border-top:1px solid var(--line);padding:20px 0 24px}
.step:last-of-type{border-bottom:1px solid var(--line)}
.step-lb{display:flex;align-items:baseline;gap:.8rem;margin-bottom:13px}
.step-lb .no{font-family:var(--d);font-style:italic;color:var(--accent);font-size:1.4rem;min-width:1.3em}
.arch-atelier .step-lb .no{font-variation-settings:"SOFT" 60,"WONK" 1}
.arch-urgent .step-lb .no{font-style:normal;font-weight:860}
.step-lb h3{font-size:1.2rem;font-weight:560}
.step-lb span{font-size:.85rem;color:var(--mut)}
.chips{display:flex;flex-wrap:wrap;gap:9px}
.chip{border:1.5px solid var(--line);border-radius:999px;padding:.55em 1.12em;font-size:.94rem;font-weight:550;color:var(--ink3);
  background:$chip_bg;transition:all .2s var(--ease)}
.chip:hover{border-color:var(--stem);color:var(--ink);transform:translateY(-1px)}
.chip[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:var(--bg)}
.arch-urgent .chip[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#141414}
.chip[aria-pressed="true"]::before{content:"✓ ";color:var(--pollen)}
.arch-urgent .chip[aria-pressed="true"]::before{color:#141414}
.ticket{position:sticky;top:96px;background:var(--card);border:1px solid var(--line);border-radius:var(--r);
  box-shadow:0 30px 60px -34px rgba(0,0,0,.4);overflow:hidden;transform:rotate(.6deg)}
.arch-studio .ticket,.arch-cabinet .ticket{transform:none}
.ticket-top{display:flex;align-items:center;gap:.6rem;background:var(--soft);padding:13px 18px;border-bottom:1px dashed var(--line)}
.ticket-top svg{width:22px;height:22px}
.ticket-top b{font-size:.8rem;letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:var(--accent-deep)}
.arch-urgent .ticket-top b{color:var(--accent)}
.ticket-body{padding:20px 22px 6px;font-family:var(--d);font-size:1.04rem;line-height:1.75;color:var(--ink2);min-height:150px}
.arch-atelier .ticket-body{font-style:italic}
.ticket-body .muted{color:var(--mut)}
.ticket-foot{padding:16px 22px 22px}
.ticket-foot .btn{width:100%;justify-content:center;font-size:1.04rem}
.ticket-hint{margin-top:10px;font-size:.8rem;color:var(--mut);text-align:center}

/* servicii: rows (atelier/urgent) */
.idx{padding:clamp(56px,8vw,100px) 0}
.idx-head{margin-bottom:clamp(22px,3.5vw,38px)}
.rows{border-top:1px solid var(--line)}
.row{display:grid;grid-template-columns:88px 1fr auto auto;align-items:center;gap:clamp(16px,3vw,34px);
  padding:20px 10px;border-bottom:1px solid var(--line);transition:background .25s var(--ease);position:relative}
.row:hover{background:var(--soft)}
.row .th{width:88px;height:88px;border-radius:50% 50% 50% 8px;overflow:hidden;flex:none;border:1px solid var(--line)}
.arch-urgent .row .th{border-radius:var(--r)}
.row .th img{width:100%;height:100%;object-fit:cover;transition:transform .5s var(--ease)}
.row:hover .th img{transform:scale(1.08)}
.row h3{font-size:clamp(1.25rem,1rem + 1.3vw,1.8rem);font-weight:520;margin-bottom:.2rem}
.arch-urgent .row h3{font-weight:800;text-transform:none;font-size:clamp(1.15rem,1rem + 1vw,1.5rem)}
.row p{color:var(--mut);font-size:.95rem;max-width:52ch}
.row .tag{font-size:.66rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--stem);
  border:1px solid var(--line);border-radius:999px;padding:.5em 1em;white-space:nowrap}
.arch-urgent .row .tag{color:var(--accent);border-color:var(--lineink)}
.row .go{display:grid;place-items:center;width:46px;height:46px;border-radius:50%;border:1.5px solid var(--ink);transition:all .25s var(--ease)}
.row .go svg{width:19px;height:19px;fill:none;stroke:currentColor;stroke-width:2;transition:transform .25s var(--ease)}
.row:hover .go{background:var(--ink);color:var(--bg)}
.arch-urgent .row:hover .go{background:var(--accent);border-color:var(--accent);color:#141414}
.row:hover .go svg{transform:translateX(2px)}
.row>a.cover{position:absolute;inset:0}

/* servicii: media (studio) */
.media-rows{display:grid;gap:clamp(30px,4.5vw,54px)}
.mrow{display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(20px,3.5vw,48px);align-items:center;position:relative}
.mrow:nth-child(even) .mimg{order:2}
.mrow .mimg{border-radius:var(--r);overflow:hidden;box-shadow:0 26px 60px -34px rgba(0,0,0,.35)}
.mrow .mimg img{width:100%;aspect-ratio:3/2;object-fit:cover;transition:transform .6s var(--ease)}
.mrow:hover .mimg img{transform:scale(1.03)}
.mrow .idxno{font-family:var(--d);font-weight:600;color:var(--accent);font-size:.95rem;letter-spacing:.1em;margin-bottom:.5rem;display:block}
.mrow h3{font-size:clamp(1.5rem,1.1rem + 1.8vw,2.2rem);margin-bottom:.5rem}
.mrow p{color:var(--mut);max-width:46ch;margin-bottom:1rem}
.mrow .tag{display:inline-block;font-size:.66rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--stem);
  border:1px solid var(--line);border-radius:999px;padding:.5em 1em;margin-bottom:1rem}
.mlink{display:inline-flex;align-items:center;gap:.5rem;font-weight:700;color:var(--ink)}
.mlink svg{width:18px;height:18px;fill:none;stroke:var(--accent);stroke-width:2.4;transition:transform .25s var(--ease)}
.mlink:hover svg{transform:translateX(4px)}

/* servicii: cards (cabinet) */
.cardgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:clamp(16px,2.5vw,26px)}
.scard{background:var(--card);border:1px solid var(--line);border-radius:calc(var(--r) + 4px);padding:24px;position:relative;
  display:flex;gap:18px;align-items:flex-start;transition:transform .25s var(--ease),box-shadow .25s}
.scard:hover{transform:translateY(-4px);box-shadow:0 26px 50px -30px rgba(0,0,0,.3)}
.scard .th{width:74px;height:74px;border-radius:50%;overflow:hidden;flex:none;border:1px solid var(--line)}
.scard .th img{width:100%;height:100%;object-fit:cover}
.scard h3{font-size:1.25rem;font-weight:600;margin-bottom:.25rem}
.scard p{color:var(--mut);font-size:.94rem;margin-bottom:.6rem}
.scard .tag{font-size:.64rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:var(--accent)}
.scard>a.cover{position:absolute;inset:0}

/* story */
.story{background:var(--ink);color:var(--bg);padding:clamp(64px,9vw,112px) 0}
.arch-urgent .story{background:var(--bg2);color:var(--ink);border-block:1px solid var(--line)}
.story .wrap{display:grid;grid-template-columns:.92fr 1.08fr;gap:clamp(30px,5vw,80px);align-items:center}
.story .eyebrow{color:var(--pollen)}
.arch-urgent .story .eyebrow{color:var(--accent)}
.story h2 .wonk{color:var(--pollen)}
.arch-urgent .story h2 .wonk{color:var(--accent)}
.story .fig{border-radius:22px 22px 999px 999px;overflow:hidden;box-shadow:0 40px 80px -40px rgba(0,0,0,.6)}
.arch-studio .story .fig,.arch-urgent .story .fig{border-radius:var(--r)}
.story .fig img{width:100%;aspect-ratio:4/4.9;object-fit:cover}
.arch-studio .story .fig img,.arch-urgent .story .fig img{aspect-ratio:4/4.2}
.story p.body{color:var(--mutink);margin:1.2rem 0 1.7rem;max-width:50ch}
.arch-urgent .story p.body{color:var(--mut)}
.facts{border-top:1px solid var(--lineink)}
.facts li{display:flex;gap:1rem;align-items:baseline;padding:13px 2px;border-bottom:1px solid var(--lineink);color:var(--bg2);font-size:.97rem}
.arch-urgent .facts li{color:var(--ink3)}
.facts li .fmark{color:var(--pollen);font-family:var(--d);font-style:italic;flex:none}
.arch-urgent .facts li .fmark{color:var(--accent);font-style:normal;font-weight:800}
.story .proof{color:var(--bg2);margin-top:1.5rem}
.arch-urgent .story .proof{color:var(--ink3)}
.story .proof b{color:#fff}
.arch-urgent .story .proof b{color:var(--ink)}

/* recenzii */
.rev{padding:clamp(60px,8vw,104px) 0;background:var(--bg2)}
.rev-head{text-align:center;max-width:56ch;margin:0 auto clamp(28px,4vw,46px)}
.notes{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(16px,2.5vw,26px)}
.note-c{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:26px 24px 20px;position:relative;
  box-shadow:0 24px 44px -30px rgba(0,0,0,.3)}
.arch-atelier .note-c:nth-child(1){transform:rotate(-1.1deg)}
.arch-atelier .note-c:nth-child(2){transform:rotate(.7deg) translateY(8px)}
.arch-atelier .note-c:nth-child(3){transform:rotate(-.5deg)}
.note-c .pin{position:absolute;top:-11px;left:50%;transform:translateX(-50%);width:22px;height:22px;background:var(--bg2)}
.note-c blockquote{font-family:var(--d);font-size:1.05rem;line-height:1.6;color:var(--ink2);margin-bottom:1rem}
.arch-atelier .note-c blockquote{font-style:italic}
.note-c figcaption{display:flex;align-items:center;justify-content:space-between;gap:10px;font-size:.85rem;color:var(--mut)}
.note-c .stars svg{width:13px;height:13px}
.rev-note{margin-top:clamp(24px,3vw,36px);text-align:center;font-size:.84rem;color:var(--mut)}

/* vizită */
.visit{padding:clamp(60px,8vw,104px) 0}
.visit .wrap{display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(30px,5vw,70px);align-items:start}
.visit h2{margin:.9rem 0 1rem}
.visit .addr{font-family:var(--d);font-size:1.3rem;font-weight:520;margin-bottom:.35rem}
.visit .sub{margin-bottom:1.6rem}
.visit-cta{display:flex;flex-wrap:wrap;gap:12px}
.hoursbox{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:clamp(22px,3vw,32px)}
.hoursbox h3{font-size:1.28rem;font-weight:600;margin-bottom:.9rem;display:flex;justify-content:space-between;align-items:baseline;gap:10px}
.hoursbox h3 .st{font-family:var(--s);font-size:.76rem;font-weight:700;letter-spacing:.08em;color:var(--stem)}
.hoursbox table{width:100%;border-collapse:collapse}
.hoursbox td{padding:.72rem 2px;border-bottom:1px solid var(--line);font-size:.96rem}
.hoursbox tr:last-child td{border-bottom:0}
.hoursbox td:last-child{text-align:right;font-weight:550;color:var(--ink3);white-space:nowrap}
.hoursbox tr.today td{color:var(--accent-deep);font-weight:700}
.arch-urgent .hoursbox tr.today td{color:var(--accent)}
.hoursbox tr.today td:first-child::after{content:" · azi";font-family:var(--d);font-style:italic;font-weight:400}

/* footer + dock */
.foot{background:var(--ink);color:var(--mutink);padding:clamp(40px,6vw,60px) 0 110px}
.arch-urgent .foot{background:#0B0C0E;color:var(--mut)}
.foot .wrap{display:grid;gap:24px}
.foot .markx{color:var(--bg)} .arch-urgent .foot .markx{color:var(--ink)}
.foot-nav{display:flex;gap:1.5rem;flex-wrap:wrap}
.foot-nav a{color:var(--bg2);font-weight:500;font-size:.94rem;opacity:.85}
.arch-urgent .foot-nav a{color:var(--ink3)}
.foot-legal{font-size:.82rem;line-height:1.7;border-top:1px solid var(--lineink);padding-top:20px}
.dock{position:fixed;right:16px;bottom:16px;z-index:150;display:flex;flex-direction:column;gap:10px}
.dock a{display:grid;place-items:center;width:56px;height:56px;border-radius:50%;box-shadow:0 14px 32px rgba(0,0,0,.4);transition:transform .2s var(--ease)}
.dock a:hover{transform:scale(1.07)}
.dock .d-call{background:var(--bg);color:var(--ink);border:1px solid var(--line)}
.dock .d-wa{background:var(--wa);color:#fff;position:relative}
.dock .d-wa::after{content:"";position:absolute;inset:0;border-radius:50%;animation:ping3 2.6s infinite}
@keyframes ping3{0%{box-shadow:0 0 0 0 rgba(31,168,85,.45)}70%{box-shadow:0 0 0 14px rgba(31,168,85,0)}100%{box-shadow:0 0 0 0 rgba(31,168,85,0)}}
.dock svg{width:26px;height:26px;fill:currentColor}

/* reveal + reduced motion */
.rv{opacity:0;transform:translateY(18px);transition:opacity .7s var(--ease),transform .7s var(--ease)}
.rv.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{animation:none!important;transition:none!important}
  .rv{opacity:1;transform:none}
  .hero-a h1 .ln>span{transform:none}
}

/* responsive */
@media (max-width:960px){
  .hero-a .wrap,.hero-u .wrap{grid-template-columns:1fr}
  .hfig,.hero-u .hfig2{max-width:520px}
  .comp-grid{grid-template-columns:1fr}
  .ticket{position:static;transform:none}
  .story .wrap{grid-template-columns:1fr}
  .story .fig{max-width:520px;order:-1}
  .notes{grid-template-columns:1fr;max-width:560px;margin-inline:auto}
  .arch-atelier .note-c:nth-child(2){transform:rotate(.7deg)}
  .visit .wrap{grid-template-columns:1fr}
  .mrow{grid-template-columns:1fr}
  .mrow:nth-child(even) .mimg{order:0}
  .cardgrid{grid-template-columns:1fr}
}
@media (max-width:820px){
  .nav{position:fixed;inset:72px 0 auto 0;z-index:110;flex-direction:column;gap:0;background:var(--bg);
    border-bottom:1px solid var(--line);padding:6px var(--pad) 16px;transform:translateY(-130%);
    transition:transform .3s var(--ease);box-shadow:0 30px 50px -30px rgba(0,0,0,.4)}
  .nav.open{transform:none}
  .nav a{padding:13px 0;border-bottom:1px solid var(--line);font-size:1.02rem}
  .burger{display:flex}
  .mast-cta .btn span{display:none}
  .mast-cta .btn{padding:.62em}
  .topline .hide-s{display:none}
  .row{grid-template-columns:64px 1fr auto}
  .row .th{width:64px;height:64px}
  .row .tag{display:none}
  .season .lbl{position:static;box-shadow:none;padding:10px var(--pad) 0}
  .season-in{flex-direction:column;align-items:stretch;padding-bottom:8px}
  .tk{padding-left:var(--pad)}
}
@media (max-width:480px){
  .hero-cta .btn,.visit-cta .btn{width:100%;justify-content:center}
  .hfig .notecard{left:8px;bottom:12px;max-width:200px}
}
""")

# ─────────────────────────────────────────────────────── constructori HTML
def btns_html(d, center=False):
    return ('<div class="hero-cta">'
      '<a class="btn btn-wa" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a>'
      '<a class="btn btn-ghost" href="tel:+%s">%s<span>Sună acum</span></a></div>'
      % (wa(d["phone_wa"], d["composer"]["base"] + "."), WA_SVG, d.get("cta_wa","Scrie pe WhatsApp"), d["phone_wa"], TEL_SVG))

def proof_html(d):
    return ('<p class="proof">%s <b>%s</b> · %s recenzii pe Google</p>'
            % (STARS5, str(d["rating"]).replace(".", ","), d["reviews_count"]))

def hero_split_arch(d):
    h1 = ('<span class="ln"><span>%s</span></span><span class="ln"><span class="wonk">%s</span></span>' % (d["h1_a"], d["h1_wonk"]))
    if d.get("h1_b"): h1 += '<span class="ln"><span>%s</span></span>' % d["h1_b"]
    note = d.get("note_text", "Răspundem pe WhatsApp de obicei pe loc, în timpul programului.")
    return Template('''<section class="hero-a" id="top"><div class="wrap">
  <div><p class="eyebrow">$eyebrow</p><h1>$h1</h1><p class="lead">$lead</p>$btns$proof</div>
  <figure class="hfig"><span class="badge">$badge</span>
    <div class="main"><img src="$hero_img" alt="$name" width="1100" height="1400" fetchpriority="high"></div>
    <div class="notecard" aria-hidden="true">$mark<p>$note</p></div>
  </figure></div></section>''').substitute(
    eyebrow=d["eyebrow"], h1=h1, lead=d["lead"], btns=btns_html(d), proof=proof_html(d),
    badge=d["addr_line1"], hero_img=img(d["images"]["hero"], 1100, 82), name=d["name"], mark=MARK_SVG, note=note)

def hero_phone_first(d):
    h1 = '%s <span class="wonk">%s</span>' % (d["h1_a"], d["h1_wonk"])
    return Template('''<section class="hero-u" id="top"><div class="wrap">
  <div><p class="eyebrow">$eyebrow</p><h1>$h1</h1><p class="lead">$lead</p>
    <a class="bigtel" href="tel:+$tel">$telsvg $tel_disp</a>
    $btns$proof</div>
  <figure class="hfig2"><span class="flag">$flag</span>
    <div class="main"><img src="$hero_img" alt="$name" width="1000" height="1150" fetchpriority="high"></div>
  </figure></div></section>''').substitute(
    eyebrow=d["eyebrow"], h1=h1, lead=d["lead"], tel=d["phone_wa"], telsvg=TEL_SVG.replace('aria-hidden="true"','aria-hidden="true" style="fill:currentColor"'),
    tel_disp=d["phone_display"], btns=btns_html(d), proof=proof_html(d),
    flag=d.get("flag","Intervenție rapidă"), hero_img=img(d["images"]["hero"], 1000, 80), name=d["name"])

def hero_fullbleed(d):
    h1 = '%s <span class="wonk">%s</span>%s' % (d["h1_a"], d["h1_wonk"], (" " + d["h1_b"]) if d.get("h1_b") else "")
    return Template('''<section class="hero-s" id="top">
  <div class="media"><img src="$hero_img" alt="$name" fetchpriority="high"></div>
  <div class="panel"><div class="wrap"><div class="panel-in">
    <p class="eyebrow">$eyebrow</p><h1>$h1</h1><p class="lead">$lead</p>$btns$proof
  </div></div></div></section>''').substitute(
    eyebrow=d["eyebrow"], h1=h1, lead=d["lead"], btns=btns_html(d), proof=proof_html(d),
    hero_img=img(d["images"]["hero"], 1800, 82), name=d["name"])

def hero_calm_card(d):
    h1 = '%s <span class="wonk">%s</span>%s' % (d["h1_a"], d["h1_wonk"], (" " + d["h1_b"]) if d.get("h1_b") else "")
    trust = "".join('<span class="trust"><svg viewBox="0 0 24 24"><path d="M5 13l4 4 10-12"/></svg>%s</span>' % t
                    for t in d["story"]["facts"][:3])
    return Template('''<section class="hero-c" id="top"><div class="wrap"><div class="inner">
  <p class="eyebrow">$eyebrow</p><h1>$h1</h1><p class="lead">$lead</p>$btns$proof
  <div class="trustrow">$trust</div></div>
  <div class="banner"><img src="$hero_img" alt="$name" fetchpriority="high"></div>
</div></section>''').substitute(
    eyebrow=d["eyebrow"], h1=h1, lead=d["lead"], btns=btns_html(d), proof=proof_html(d),
    trust=trust, hero_img=img(d["images"]["hero"], 1800, 80), name=d["name"])

HEROES = {"split_arch": hero_split_arch, "phone_first": hero_phone_first,
          "fullbleed": hero_fullbleed, "calm_card": hero_calm_card}

def services_rows(d):
    out = []
    for s in d["services"]:
        msg = "Bună ziua! Aș dori detalii despre: %s." % s["title"]
        out.append(Template('''<article class="row rv">
  <div class="th"><img src="$im" alt="$t — $name" width="300" height="300"></div>
  <div><h3>$t</h3><p>$dsc</p></div>
  <span class="tag">$tag</span>
  <span class="go" aria-hidden="true">$arrow</span>
  <a class="cover" href="$href" target="_blank" rel="noopener" aria-label="Întreabă despre $t pe WhatsApp"></a>
</article>''').substitute(im=img(s["img"], 300, 75), t=s["title"], dsc=s["desc"], tag=s.get("tag",""),
                          name=d["name"], arrow=ARROW_SVG, href=wa(d["phone_wa"], msg)))
    return '<div class="rows">%s</div>' % "".join(out)

def services_media(d):
    out = []
    for i, s in enumerate(d["services"], 1):
        msg = "Bună ziua! Aș dori detalii despre: %s." % s["title"]
        out.append(Template('''<article class="mrow rv">
  <div class="mimg"><img src="$im" alt="$t — $name" width="900" height="600"></div>
  <div><span class="idxno">$no</span><h3>$t</h3><span class="tag">$tag</span><p>$dsc</p>
    <a class="mlink" href="$href" target="_blank" rel="noopener">Întreabă pe WhatsApp $arrow</a></div>
</article>''').substitute(im=img(s["img"], 900, 80), t=s["title"], dsc=s["desc"], tag=s.get("tag",""),
                          no="%02d" % i, name=d["name"], arrow=ARROW_SVG, href=wa(d["phone_wa"], msg)))
    return '<div class="media-rows">%s</div>' % "".join(out)

def services_cards(d):
    out = []
    for s in d["services"]:
        msg = "Bună ziua! Aș dori detalii despre: %s." % s["title"]
        out.append(Template('''<article class="scard rv">
  <div class="th"><img src="$im" alt="$t — $name" width="300" height="300"></div>
  <div><h3>$t</h3><p>$dsc</p><span class="tag">$tag</span></div>
  <a class="cover" href="$href" target="_blank" rel="noopener" aria-label="Întreabă despre $t pe WhatsApp"></a>
</article>''').substitute(im=img(s["img"], 300, 75), t=s["title"], dsc=s["desc"], tag=s.get("tag",""),
                          name=d["name"], href=wa(d["phone_wa"], msg)))
    return '<div class="cardgrid">%s</div>' % "".join(out)

SERVICES_LAYOUT = {"atelier": services_rows, "urgent": services_rows,
                   "studio": services_media, "cabinet": services_cards}

def composer_html(d):
    c = d["composer"]
    steps_html, keys = [], []
    letters = "abcdefgh"
    for i, st in enumerate(c["steps"]):
        keys.append(st["key"])
        chips = "".join('<button class="chip" aria-pressed="false" data-v="%s">%s</button>'
                        % (v.replace('"','&quot;'), l) for (l, v) in st["options"])
        hint = ('<span>%s</span>' % st["hint"]) if st.get("hint") else ""
        steps_html.append('''<div class="step rv"><div class="step-lb"><span class="no" aria-hidden="true">%s.</span><h3>%s</h3>%s</div>
<div class="chips" data-grp="%s" role="group" aria-label="%s">%s</div></div>''' % (letters[i], st["label"], hint, st["key"], st["label"], chips))
    return Template('''<section class="comp" id="comanda"><div class="wrap">
  <header class="comp-head rv"><p class="eyebrow">$kick</p>
    <h2>$t1 <span class="wonk">$t2</span></h2>
    <p class="sub" style="margin-top:.8rem">$sub</p></header>
  <div class="comp-grid"><div>$steps</div>
  <aside class="ticket rv" aria-live="polite">
    <div class="ticket-top">$mark<b>Mesajul tău</b></div>
    <div class="ticket-body" id="bilet"></div>
    <div class="ticket-foot">
      <a class="btn btn-wa" id="waBtn" href="#" target="_blank" rel="noopener">$wasvg<span>Trimite pe WhatsApp</span></a>
      <p class="ticket-hint">Se deschide WhatsApp cu mesajul gata scris — îl poți edita înainte de trimitere.</p>
    </div></aside></div></div></section>''').substitute(
    kick=d.get("comp_kicker","Durează 30 de secunde"), t1=c["intro_title"], t2=c["intro_wonk"],
    sub=c["intro_sub"], steps="".join(steps_html), mark=MARK_SVG, wasvg=WA_SVG), keys

def story_html(d):
    s = d["story"]
    facts = "".join('<li class="rv"><span class="fmark">%s</span>%s</li>'
                    % ("✿" if d["archetype"]=="atelier" else "→", f) for f in s["facts"])
    return Template('''<section class="story" id="atelier"><div class="wrap">
  <figure class="fig rv"><img src="$im" alt="$name" width="1000" height="1250"></figure>
  <div><p class="eyebrow rv">$kick</p>
    <h2 class="rv">$a <span class="wonk">$b</span></h2>
    <p class="body rv">$body</p>
    <ul class="facts">$facts</ul>
    <p class="proof rv">$stars <b>$rating</b> din $rc recenzii pe Google</p>
  </div></div></section>''').substitute(
    im=img(d["images"]["story"], 1000, 82), name=d["name"], kick=s["eyebrow"], a=s["h2_a"], b=s["h2_wonk"],
    body=s["body"], facts=facts, stars=STARS5, rating=str(d["rating"]).replace(".", ","), rc=d["reviews_count"])

def reviews_html(d):
    out = []
    for q in d["reviews"][:3]:
        out.append('''<figure class="note-c rv">%s<blockquote>%s"</blockquote>
<figcaption><span>Client Google</span>%s</figcaption></figure>''' % (
            MARK_SVG.replace('class="fl"','class="pin fl"'), q, STARS5.replace('width:17px','width:13px')))
    return Template('''<section class="rev" id="recenzii"><div class="wrap">
  <header class="rev-head rv"><p class="eyebrow">Ce spun clienții</p>
    <h2>$t1 <span class="wonk">$t2</span></h2></header>
  <div class="notes">$notes</div>
  <p class="rev-note rv">Rating real: $rating★ din $rc recenzii pe Google. Citatele de mai sus sunt ilustrative.</p>
</div></section>''').substitute(notes="".join(out), rating=str(d["rating"]).replace(".", ","),
    rc=d["reviews_count"], t1=d.get("rev_t1","Oamenii se întorc"), t2=d.get("rev_t2","cu drag."))

# ─────────────────────────────────────────────────────── template HTML master
PAGE = Template('''<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$seo_title</title>
<meta name="description" content="$seo_desc">
<meta name="theme-color" content="$theme">
<meta property="og:title" content="$og_title">
<meta property="og:description" content="$seo_desc">
<meta property="og:type" content="website">
<meta property="og:image" content="$og_image">
<link rel="icon" href="$favicon">
<link rel="preload" as="image" href="$hero_pre" fetchpriority="high">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
$fonts
<script type="application/ld+json">$schema</script>
<style>$css</style>
</head>
<body class="$body_class">
<a class="skip" href="#continut">Sari la conținut</a>
<div class="topline"><div class="wrap">
  <span class="status" id="stare"><span class="dot"></span><span id="stareTxt">$addr_short</span></span>
  <span class="hide-s" style="font-family:var(--d);font-style:italic">$topline_moto</span>
  <a href="tel:+$tel">$tel_disp</a>
</div></div>
<header class="mast"><div class="wrap">
  <a class="markx" href="#top" aria-label="$name — acasă">$brand<small>$brand_sub</small></a>
  <nav class="nav" id="nav" aria-label="Principal">
    <a href="#comanda">$nav_comanda</a><a href="#servicii">Ce facem</a><a href="#atelier">$nav_story</a><a href="#recenzii">Recenzii</a><a href="#vizita">Vizită</a>
  </nav>
  <div class="mast-cta">
    <a class="btn btn-ghost" href="tel:+$tel" aria-label="Sună la $tel_disp">$telsvg<span>$tel_disp</span></a>
    <button class="burger" id="burger" aria-label="Meniu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</div></header>
<main id="continut">
$hero
<div class="season" aria-label="$ticker_label"><div class="season-in">
  <span class="lbl">$ticker_label</span>
  <div class="tk" id="ticker">$ticker_items</div>
</div></div>
$composer
<section class="idx" id="servicii"><div class="wrap">
  <div class="idx-head rv"><p class="eyebrow">$serv_kicker</p><h2>$serv_t1 <span class="wonk">$serv_t2</span></h2></div>
  $services
</div></section>
$story
$reviews
<section class="visit" id="vizita"><div class="wrap">
  <div><p class="eyebrow rv">$visit_kicker</p>
    <h2 class="rv">$visit_t1 <span class="wonk">$visit_t2</span></h2>
    <p class="addr rv">$address</p>
    <p class="sub rv">$visit_sub</p>
    <div class="visit-cta rv">
      <a class="btn btn-ink" href="$maps" target="_blank" rel="noopener">$pinsvg<span>Deschide în Google Maps</span></a>
      <a class="btn btn-ghost" href="tel:+$tel">$telsvg<span>$tel_disp</span></a>
    </div></div>
  <aside class="hoursbox rv"><h3>Program <span class="st" id="stareProgram"></span></h3>
    <table id="tabelProgram">$hours_rows</table>
  </aside>
</div></section>
</main>
<footer class="foot"><div class="wrap">
  <a class="markx" href="#top">$brand<small>$brand_sub</small></a>
  <nav class="foot-nav" aria-label="Subsol"><a href="#comanda">$nav_comanda</a><a href="#servicii">Ce facem</a><a href="#recenzii">Recenzii</a><a href="#vizita">Vizită</a></nav>
  <p class="foot-legal">© <span id="an"></span> $name · $address · $tel_disp<br>$foot_line Rating $rating★ din $rc recenzii Google.</p>
</div></footer>
<div class="dock">
  <a class="d-call" href="tel:+$tel" aria-label="Sună acum">$telsvg</a>
  <a class="d-wa" href="$wa_main" target="_blank" rel="noopener" aria-label="Scrie pe WhatsApp">$wasvg</a>
</div>
<script>
(function(){
  "use strict";
  var TEL="$tel", BASE="$js_base", STEPS=$js_steps, ORE=$js_ore;
  var an=document.getElementById('an'); if(an) an.textContent=new Date().getFullYear();
  var burger=document.getElementById('burger'), nav=document.getElementById('nav');
  if(burger&&nav){
    burger.addEventListener('click',function(){var o=nav.classList.toggle('open');burger.setAttribute('aria-expanded',o?'true':'false');});
    nav.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('open');burger.setAttribute('aria-expanded','false');});});
  }
  var tk=document.getElementById('ticker'); if(tk) tk.innerHTML+=tk.innerHTML;
  /* stare live */
  function acumBuc(){
    try{
      var s=new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Bucharest',weekday:'short',hour:'numeric',minute:'numeric',hour12:false}).formatToParts(new Date());
      var o={}; s.forEach(function(p){o[p.type]=p.value});
      var zi={Sun:0,Mon:1,Tue:2,Wed:3,Thu:4,Fri:5,Sat:6}[o.weekday];
      return {zi:zi, ora:parseInt(o.hour,10)+parseInt(o.minute,10)/60};
    }catch(e){ var d=new Date(); return {zi:d.getDay(), ora:d.getHours()+d.getMinutes()/60}; }
  }
  function pad2(n){return (n<10?'0':'')+n;}
  var stare=document.getElementById('stare'), stareTxt=document.getElementById('stareTxt'), sp=document.getElementById('stareProgram');
  var now=acumBuc(), deschis=false, txt="";
  if(ORE==="NS"){ deschis=true; txt="Deschis NON-STOP · $addr_short"; }
  else if(ORE){
    var iv=ORE[now.zi];
    deschis=!!iv && now.ora>=iv[0] && now.ora<iv[1];
    if(deschis){ txt="Deschis acum · până la "+iv[1]+":00 · $addr_short"; }
    else{
      var urm=null;
      if(iv && now.ora<iv[0]) urm=iv[0];
      else{ for(var k=1;k<=7;k++){ var nx=ORE[(now.zi+k)%7]; if(nx){urm=nx[0];break;} } }
      txt="Închis acum"+(urm!==null?" · deschidem la "+pad2(urm)+":00":"")+" · $addr_short";
    }
  }
  if(stare&&stareTxt&&ORE){ if(deschis) stare.classList.add('open'); stareTxt.textContent=txt; }
  if(sp&&ORE){ sp.textContent=deschis?"● deschis acum":"● închis acum"; if(!deschis) sp.style.color="var(--mut)"; }
  document.querySelectorAll('#tabelProgram tr').forEach(function(r){
    var ds=(r.getAttribute('data-d')||"").split(',');
    if(ds.indexOf(String(now.zi))>-1 || ds[0]==="-1") r.classList.add('today');
  });
  /* compozitor */
  var sel={}, bilet=document.getElementById('bilet'), waBtn=document.getElementById('waBtn');
  function cap(s){return s.charAt(0).toUpperCase()+s.slice(1);}
  function scrie(){
    var lin=[], first=sel[STEPS[0]];
    lin.push(BASE+(first?" "+first:"")+".");
    for(var i=1;i<STEPS.length;i++){ var v=sel[STEPS[i]]; if(v) lin.push(cap(v)+"."); }
    lin.push("Mulțumesc!");
    var vre=false; STEPS.forEach(function(k){ if(sel[k]) vre=true; });
    if(bilet){
      if(!vre){ bilet.innerHTML='<span class="muted">'+BASE+'…</span><br><br><span class="muted" style="font-size:.9rem">— alege mai sus, iar mesajul se compune aici —</span>'; }
      else{ bilet.innerHTML=lin.map(function(l){return l.replace(/&/g,'&amp;').replace(/</g,'&lt;')}).join('<br>'); }
    }
    if(waBtn) waBtn.href='https://wa.me/'+TEL+'?text='+encodeURIComponent(lin.join('\\n'));
  }
  document.querySelectorAll('.chips').forEach(function(grp){
    var key=grp.getAttribute('data-grp');
    grp.querySelectorAll('.chip').forEach(function(ch){
      ch.addEventListener('click',function(){
        var era=ch.getAttribute('aria-pressed')==='true';
        grp.querySelectorAll('.chip').forEach(function(c){c.setAttribute('aria-pressed','false')});
        if(!era){ ch.setAttribute('aria-pressed','true'); sel[key]=ch.getAttribute('data-v'); } else sel[key]=null;
        scrie();
      });
    });
  });
  scrie();
  /* reveal cu failsafe */
  var els=document.querySelectorAll('.rv');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12,rootMargin:'0px 0px -6% 0px'});
    els.forEach(function(el){io.observe(el)});
    setTimeout(function(){ els.forEach(function(el){el.classList.add('in')}); io.disconnect(); },1200);
  } else els.forEach(function(el){el.classList.add('in')});
})();
</script>
</body>
</html>''')

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Crect width='48' height='48' rx='10' fill='INKC'/%3E"
 "%3Cg fill='none' stroke='ACCC' stroke-width='2.4' stroke-linecap='round'%3E%3Ccircle cx='24' cy='24' r='4.5'/%3E"
 "%3Cpath d='M24 19.5c0-6-4-9.5-4-9.5s7.5-1 8.5 5.5c.6 3.9-4.5 4-4.5 4z'/%3E%3Cpath d='M28.5 24c6 0 9.5-4 9.5-4s1 7.5-5.5 8.5c-3.9.6-4-4.5-4-4.5z'/%3E"
 "%3Cpath d='M24 28.5c0 6 4 9.5 4 9.5s-7.5 1-8.5-5.5c-.6-3.9 4.5-4 4.5-4z'/%3E%3Cpath d='M19.5 24c-6 0-9.5 4-9.5 4s-1-7.5 5.5-8.5c3.9-.6 4 4.5 4 4.5z'/%3E%3C/g%3E%3C/svg%3E")

def brand_html(d):
    n = d["name"]
    for sep in (" & ", " și ", " si "):
        if sep in n:
            a, b = n.split(sep, 1)
            return '%s<span class="amp">&amp;</span>%s' % (a.strip(), b.strip())
    return n

def build2(lead):
    nk = lead.get("niche_key", "")
    preset = dict(NICHE_PRESETS.get(nk, {}))
    d = {}
    d.update(preset); d.update({k: v for k, v in lead.items() if v is not None})
    # completări derivate
    arch_key = d.get("archetype", "cabinet")
    arch = ARCHETYPES[arch_key]; d["archetype"] = arch_key
    tokens = dict(arch["tokens"])
    if d.get("accent"): tokens["accent"] = d["accent"]
    if d.get("accent_deep"): tokens["accent_deep"] = d["accent_deep"]
    zona = d.get("zona") or (re.search(r"Sector\s*\d", d.get("address","")) or [None])
    zona = zona.group(0) if hasattr(zona, "group") else (d.get("addr_city") or "București")
    for f in ("eyebrow",):
        d[f] = d.get(f, "").replace("{zona}", zona).replace("{name}", d["name"])
    hours_s = d.get("hours_s")
    if hours_s:
        rows, _ = hours_rows_html(hours_s); ore_js = hours_js_obj(hours_s)
    else:
        rows = '<tr data-d="-2"><td>Program</td><td>%s</td></tr>' % d.get("program_text", "La programare")
        ore_js = "null"
    comp_html, step_keys = composer_html(d)
    css = CSS.substitute(font_d=arch["font_d"], font_s=arch["font_s"], radius=arch["radius"],
                         chip_bg=arch["chip_bg"], **tokens)
    schema = json.dumps({"@context":"https://schema.org","@type":d.get("schema_type","LocalBusiness"),
      "name":d["name"],"image":img(d["images"]["hero"],1200),"telephone":"+"+d["phone_wa"],
      "address":{"@type":"PostalAddress","streetAddress":d.get("addr_line1",""),"addressLocality":d.get("addr_city","București"),"addressCountry":"RO"},
      "aggregateRating":{"@type":"AggregateRating","ratingValue":str(d["rating"]),"reviewCount":str(d["reviews_count"])}}, ensure_ascii=False)
    ticker_items = "".join("<span>%s</span>" % t for t in d["ticker"])
    html = PAGE.substitute(
        seo_title=d.get("seo_title", "%s — %s" % (d["name"], d.get("addr_city","București"))),
        seo_desc=d.get("seo_desc", "%s · %s. Rating %s din %s recenzii Google. Telefon: %s." % (d["name"], d.get("address",""), d["rating"], d["reviews_count"], d["phone_display"])),
        og_title=d.get("seo_title", d["name"]), og_image=img(d["images"]["hero"], 1200),
        theme=tokens["ink"] if arch_key != "urgent" else tokens["bg"],
        favicon=FAVICON.replace("INKC", "%23" + tokens["ink"].lstrip("#")).replace("ACCC", "%23" + tokens["accent"].lstrip("#")),
        hero_pre=img(d["images"]["hero"], 1100, 82), fonts=arch["fonts"], schema=schema, css=css,
        body_class=arch["body_class"], addr_short=d.get("addr_line1", d.get("address","")),
        topline_moto=d.get("topline_moto", d.get("eyebrow","")),
        tel=d["phone_wa"], tel_disp=d["phone_display"], telsvg=TEL_SVG, wasvg=WA_SVG, pinsvg=PIN_SVG,
        name=d["name"], brand=brand_html(d), brand_sub=d.get("brand_sub", zona),
        nav_comanda=d.get("nav_comanda","Cere ofertă"), nav_story=d.get("nav_story","Despre noi"),
        hero=HEROES[arch["hero"]](d),
        ticker_label=d.get("ticker_label","Ce facem"), ticker_items=ticker_items,
        composer=comp_html,
        serv_kicker=d.get("serv_kicker","Ce facem"), serv_t1=d.get("serv_t1","Serviciile noastre,"),
        serv_t2=d.get("serv_t2","pe scurt."),
        services=SERVICES_LAYOUT[arch_key](d),
        story=story_html(d), reviews=reviews_html(d),
        visit_kicker=d.get("visit_kicker","Unde ne găsești"),
        visit_t1=d.get("visit_t1","Ne găsești"), visit_t2=d.get("visit_t2","ușor."),
        address=d.get("address",""), maps="https://www.google.com/maps/search/?api=1&query=" + quote("%s %s" % (d["name"], d.get("address",""))),
        visit_sub=d.get("visit_sub","Scrie-ne pe WhatsApp înainte să pornești — îți confirmăm că suntem pe loc."),
        hours_rows=rows, foot_line=d.get("foot_line",""),
        rating=str(d["rating"]).replace(".", ","), rc=d["reviews_count"],
        js_base=d["composer"]["base"].replace('"','\\"'), js_steps=json.dumps(step_keys, ensure_ascii=False), js_ore=ore_js,
        wa_main=wa(d["phone_wa"], d["composer"]["base"] + "."),
    )
    return html

def guess_niche_key(q):
    q = (q or "").lower()
    table = [
        (r"tapiter", "tapiterie"), (r"florar|flori", "florarie"), (r"cizm|incaltamint", "cizmarie"),
        (r"ceasornic|ceasuri", "ceasornicarie"), (r"mobil[ăa]|bucatarii|dressing", "mobila"),
        (r"parbriz|geamuri auto|lunet", "parbrize"), (r"vulcaniz|anvelop", "vulcanizare"),
        (r"electric[ăa] auto|diagnoz|electrician auto", "electrica_auto"),
        (r"detailing|polish", "detailing"), (r"vopsitor|tinichig|daune", "vopsitorie"),
        (r"spalatorie|car wash|spălătorie", "spalatorie"), (r"optic", "optica"),
        (r"kineto|masaj|recuperare|fizio", "kineto"),
        (r"masin[ăa] de spalat|frigider|electrocasnic|uscator", "reparatii_electro"),
        (r"gsm|telefo", "gsm"), (r"service auto|mecanic", "service_auto"),
    ]
    for rx, key in table:
        if re.search(rx, q): return key
    return None

def from_scraped(path):
    """leads_found.json (scraper) → listă leaduri v2 pe presets."""
    raw = json.load(open(path, encoding="utf-8"))
    out = []
    for r in raw:
        nk = guess_niche_key(r.get("niche") or r.get("category") or r.get("name"))
        if not nk:
            print("[skip] nișă necunoscută:", r.get("name")); continue
        ph = norm_phone(r["phone"])
        slug = re.sub(r"[^a-z0-9]+", "_", ("%s_%s" % (nk, r["name"])).lower()).strip("_")[:60]
        addr = r.get("address") or "București"
        lead = dict(slug=slug, niche_key=nk, name=r["name"].strip(),
                    phone_wa="40"+ph, phone_display=r["phone"].strip(),
                    address=addr, addr_line1=addr.split(",")[0], addr_city="București",
                    rating=r.get("rating") or "—", reviews_count=r.get("reviews") or 0,
                    program_text=r.get("program"))
        out.append(lead)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_in", nargs="?", help="fișier JSON cu leaduri v2")
    ap.add_argument("--from-scraped", help="convertește leads_found.json (scraper) în leaduri v2")
    ap.add_argument("--out-json", help="unde scriu leadurile convertite (cu --from-scraped)")
    ap.add_argument("--no-build", action="store_true", help="doar conversia, fără generare HTML")
    args = ap.parse_args()
    leads = []
    if args.from_scraped:
        leads = from_scraped(args.from_scraped)
        if args.out_json:
            json.dump(leads, open(args.out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            print("[✓] %d leaduri v2 → %s" % (len(leads), args.out_json))
        if args.no_build: return
    elif args.json_in:
        leads = json.load(open(args.json_in, encoding="utf-8"))
    else:
        ap.error("dă un JSON v2 sau --from-scraped")
    os.makedirs(OUT_DIR, exist_ok=True)
    for lead in leads:
        html = build2(lead)
        p = os.path.join(OUT_DIR, lead["slug"] + ".html")
        open(p, "w", encoding="utf-8").write(html)
        print("✓ %-46s %6d octeți  [%s]" % (lead["slug"], len(html.encode("utf-8")),
              lead.get("archetype") or NICHE_PRESETS.get(lead.get("niche_key",""),{}).get("archetype","?")))


# ─────────────────────────────────────────────────────── imagini corecte (recoltate din rundele 4-7, verificate vizual de agenți)
IMG.update({
 "ciz_cobbler":"1477517787936-70ba786643fd","ciz_boots":"1449505278894-297fdb3edbc1","ciz_shoes":"1614252235316-8c857d38b5f4",
 "ciz_tie":"1520639888713-7851133b1ed0","ciz_suede":"1598532163257-ae3c6b2524b6","ciz_bag":"1590874103328-eac38a683ce7",
 "ciz_f_sew":"https://live.staticflickr.com/65535/49482714491_ac8daa910c_b.jpg",
 "ciz_f_last":"https://live.staticflickr.com/65535/49482919832_7fa7f801a3_b.jpg",
 "ciz_f_glue":"https://live.staticflickr.com/65535/49482716781_f4e0ba9873_b.jpg",
 "ciz_f_cut":"https://live.staticflickr.com/65535/49482926232_95f25f839c_b.jpg",
 "watch_1":"1524805444758-089113d48a6d","watch_2":"1547996160-81dfa63595aa","watch_3":"1533139502658-0198f920d8e8",
 "watch_4":"1585123334904-845d60e97b29","watch_5":"1622434641406-a158123450f9","watch_6":"1495856458515-0637185db551",
 "watch_7":"1523170335258-f5ed11844a49","watch_8":"1509048191080-d2984bad6ae5",
 "kin_masaj":"1544161515-4ab6ce6db874","kin_fizio":"1600334129128-685c5582fd35","kin_terapeut":"1594824476967-48c8b964273f",
 "kin_stretch":"1518611012118-696072aa579a","kin_stones":"1519824145371-296894a0daa9",
 "gsm_board":"1550041473-d296a3a8a18a","gsm_iphone":"1617299516258-eb06985065ff","gsm_macro":"1518770660439-4636190af475",
 "gsm_phones":"1616410011236-7a42121dd981",
 "opt_1":"1574258495973-f010dfbb5371","opt_2":"1508296695146-257a814070b4","opt_3":"1577803645773-f96470509666","opt_4":"1591076482161-42ce6da69f67",
 "det_int2":"1600661653561-629509216228","det_wheel":"1605164599901-db7f68c1b2fd","det_wax":"1607860108855-64acf2078ed9","det_foam2":"1621252179027-94459d278660",
 "wash_1":"1721274501976-144f45bfb1af","wash_2":"1746017240064-83e015ac117d","wash_3":"1752805869096-9b149e6effa1","wash_4":"1761079976271-3a78f547ca67",
 "vop_booth":"1601362840469-51e4d8d58785","vop_spray":"1580414057403-c5f451f30e1c","vop_car":"1619642751034-765dfdf7c58e","vop_tape":"1615826167603-c9b5f4f9c1b5",
 "far_led":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/2014_Toyota_Corolla_LED_Headlight.jpg/1920px-2014_Toyota_Corolla_LED_Headlight.jpg",
 "far_led9":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/2014_Toyota_Corolla_LED_Headlight.jpg/960px-2014_Toyota_Corolla_LED_Headlight.jpg",
 "far_yellow":"https://upload.wikimedia.org/wikipedia/commons/b/b3/Yellowed_headlight_of_a_Toyota_car.jpg",
 "volan_mb":"https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/2014_Mercedes-Benz_steering_wheel_%288403244933%29.jpg/960px-2014_Mercedes-Benz_steering_wheel_%288403244933%29.jpg",
 "volan_amg":"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/AMG_%28Mercedes-Benz%29_interior%2C_AMG_BiTurbo%2C_red_leather.jpg/960px-AMG_%28Mercedes-Benz%29_interior%2C_AMG_BiTurbo%2C_red_leather.jpg",
 "vulc_f1":"https://live.staticflickr.com/65535/49973032726_d153221cb6_b.jpg",
 "vulc_f2":"https://live.staticflickr.com/65535/49988558466_cbb2514fa9_b.jpg",
 "vulc_f3":"https://live.staticflickr.com/3833/10960581703_955da7848b_b.jpg",
 "vulc_f4":"https://live.staticflickr.com/7126/27209360756_d3e224a38e_b.jpg",
})

def _re_img(nk, hero, story, per_service):
    P = NICHE_PRESETS[nk]
    P["images"] = dict(hero=IMG[hero], story=IMG[story])
    for s_, key in zip(P["services"], per_service):
        s_["img"] = IMG[key]

_re_img("cizmarie",     "ciz_cobbler", "ciz_f_sew",  ["ciz_f_last","ciz_f_glue","ciz_suede","ciz_tie"])
_re_img("ceasornicarie","watch_1",     "watch_6",    ["watch_2","watch_3","watch_4","watch_5"])
_re_img("kineto",       "kin_masaj",   "kin_terapeut",["kin_stretch","kin_fizio","kin_masaj","kin_stones"])
_re_img("gsm",          "gsm_board",   "gsm_iphone", ["gsm_iphone","gsm_macro","gsm_board","gsm_phones"])
_re_img("optica",       "opt_1",       "opt_2",      ["opt_3","opt_4","opt_2","opt_1"])
_re_img("detailing",    "det_hero",    "det_wax",    ["auto_dark","det_wax","det_int2","det_hero"])
_re_img("spalatorie",   "det_foam2",   "det_int2",   ["det_hero","det_int2","det_wax","det_wheel"])
_re_img("vopsitorie",   "vop_booth",   "vop_spray",  ["vop_car","vop_booth","vop_tape","det_wax"])
_re_img("reparatii_electro","wash_1",  "wash_2",     ["wash_3","wash_1","wash_4","wash_2"])
_re_img("parbrize",     "far_led",     "auto_dark",  ["auto_road","auto_dark","far_yellow","far_led9"])
_re_img("electrica_auto","auto_far",   "gsm_macro",  ["rep_1","auto_far","gsm_macro","auto_road"])

# volan în serviciul de tapițerie → poza reală de volan
NICHE_PRESETS["tapiterie"]["services"][2]["img"] = IMG["volan_mb"]

# titluri de secțiune per nișă (în loc de genericul „Serviciile noastre, pe scurt.")
for nk, (a, b) in {
  "cizmarie":("Ce reparăm,","cel mai des."), "parbrize":("Intervenții,","pe scurt."),
  "detailing":("Tratamentele,","în detaliu."), "kineto":("Cum te ajutăm,","pas cu pas."),
  "florarie":("Patru feluri de","bucurie."), "ceasornicarie":("Ce trece prin","mâinile noastre."),
  "gsm":("Reparații,","cât aștepți."), "vopsitorie":("De la daună,","la predare."),
  "spalatorie":("Pachetele,","pe scurt."), "optica":("Pentru ochii tăi,","pe rând."),
  "reparatii_electro":("Ce reparăm,","acasă la tine."), "tapiterie":("Ce refacem,","bucată cu bucată."),
  "mobila":("Ce construim,","pe măsură."), "electrica_auto":("Ce rezolvăm,","cu testerul."),
  "service_auto":("Lucrările,","pe față."),
}.items():
    NICHE_PRESETS[nk]["serv_t1"] = a; NICHE_PRESETS[nk]["serv_t2"] = b

# vulcanizare: preset propriu (urgent), cu pozele Flickr reale de atelier roți
import copy as _copy
_v = _copy.deepcopy(NICHE_PRESETS["parbrize"])
_v.update(
  eyebrow="Vulcanizare & anvelope · {zona}", h1_a="Pană?", h1_wonk="Intri și ieși.", h1_b="",
  lead="Anvelope montate, echilibrate și reparate rapid — vino direct sau întreabă pe WhatsApp cât e de așteptat acum.",
  ticker_label="Facem zilnic", ticker=["schimb anvelope","reparații pană","echilibrare","schimb sezonier","hotel anvelope","jante"],
  composer=dict(intro_title="Spune-ne ce are roata —", intro_wonk="te băgăm la rând.",
    intro_sub="Trimite și îți răspundem cu timpul de așteptare de acum.",
    base="Bună ziua! Am nevoie la roți", unit="intervenția",
    steps=[
      dict(key="ce", label="Ce s-a întâmplat?", options=[("Pană","o pană"),("Schimb sezonier","schimbul sezonier"),("Echilibrare","echilibrare"),("Anvelope noi","anvelope noi"),("Hotel anvelope","depozitare anvelope")]),
      dict(key="masina", label="Ce mașină?", options=[("Autoturism","la un autoturism"),("SUV / 4x4","la un SUV"),("Utilitară","la o utilitară")]),
      dict(key="cand", label="Când ajungi?", options=[("Acum, sunt pe drum","acum — sunt pe drum"),("Azi","azi"),("Zilele astea","în zilele următoare")]),
    ]),
  services=[
    dict(title="Schimb & montaj anvelope", desc="Montaj atent, cu cuplu corect la strângere — nu cu pistolul la maxim.", tag="rapid", img=IMG["vulc_f1"]),
    dict(title="Reparații pană", desc="Reparăm profesional, nu doar cu fitil — ca să țină.", tag="ține", img=IMG["vulc_f3"]),
    dict(title="Echilibrare", desc="Scapi de vibrațiile din volan la viteză.", tag="confort", img=IMG["vulc_f2"]),
    dict(title="Hotel anvelope", desc="Îți ținem noi setul de sezon, etichetat și depozitat corect.", tag="depozitare", img=IMG["vulc_f4"]),
  ],
  story=dict(eyebrow="De ce la noi", h2_a="Roțile țin mașina pe drum —", h2_wonk="le tratăm serios.",
    body="Montaj cu grijă la jantă, presiuni corecte, cuplu la cheie dinamometrică. Lucru rapid nu înseamnă lucru neglijent.",
    facts=["Cuplu corect la strângere, nu „la pistol”","Presiuni verificate la predare","Program lung, weekend inclus"]),
  images=dict(hero=IMG["vulc_f1"], story=IMG["vulc_f2"]),
  serv_t1="La roți,", serv_t2="pe scurt.",
)
NICHE_PRESETS["vulcanizare"] = _v


if __name__ == "__main__":
    main()
