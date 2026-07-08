#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pipeline_leads — cap-coadă: scrape → (om la mijloc) → generare v2 → git push + verificare live
→ intrare în SITEURI_DE_TESTAT.txt → (după testare) mutare în tested_leads.txt.

Comenzi:
  scrape   caută leads noi (deduplicate față de toate listele) și scrie pending_leads.json
           gata de generat (cu hours_s structurat + preset pe nișă).
             python3 pipeline_leads.py scrape --niches "vulcanizare Bucuresti" --max-per-niche 3
             python3 pipeline_leads.py scrape --niches-file niches.txt
           → REVIZUIEȘTE pending_leads.json (omul de la mijloc), apoi:

  publish  generează mockup-urile v2, face push, așteaptă HTTP 200 live și abia apoi
           scrie intrările (format standard, numerotare continuată) în SITEURI_DE_TESTAT.txt + push.
             python3 pipeline_leads.py publish                 # ia pending_leads.json
             python3 pipeline_leads.py publish alt_fisier.json
             python3 pipeline_leads.py publish --dry-run       # generează local, fără push/listă

  move     după ce ai sunat/testat un lead: mută intrarea din SITEURI_DE_TESTAT.txt
           în tested_leads.txt (cu status) și comite.
             python3 pipeline_leads.py move 23 --status "CONTACTAT — așteaptă răspuns"
             python3 pipeline_leads.py move 23 --status "CLIENT ✔" --no-push
"""
import argparse, json, os, re, subprocess, sys, time
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
LISTA = os.path.join(BASE, "SITEURI_DE_TESTAT.txt")
TESTED = os.path.join(BASE, "tested_leads.txt")
PENDING = os.path.join(BASE, "pending_leads.json")
LIVE_BASE = "https://sami111-afk.github.io/leads-finder/mockupuri"
VENV_PY = os.path.expanduser("~/.venvs/leads/bin/python")
if not os.path.exists(VENV_PY):
    VENV_PY = "/tmp/claude-1000/-home-sol/743c18f2-db96-4fa3-8f02-fbfae76e2626/scratchpad/venv/bin/python"

sys.path.insert(0, BASE)
import mockup_gen2 as g2

EMOJI = {"florarie":"💐","cizmarie":"👞","ceasornicarie":"⏱️","tapiterie":"🚗","mobila":"🪑",
         "parbrize":"🚙","vulcanizare":"🛞","electrica_auto":"⚡","detailing":"✨","vopsitorie":"🎨",
         "spalatorie":"💦","optica":"👓","kineto":"💆","reparatii_electro":"🧺","masini_spalat":"🧺",
         "frigidere":"🧺","gsm":"📱","service_auto":"🔧"}
CAT_SCURT = {"florarie":"Florărie","cizmarie":"Cizmărie","ceasornicarie":"Ceasornicărie",
             "tapiterie":"Tapițerie auto","mobila":"Mobilă la comandă","parbrize":"Parbrize auto",
             "vulcanizare":"Vulcanizare","electrica_auto":"Electrică auto","detailing":"Detailing auto",
             "vopsitorie":"Vopsitorie auto","spalatorie":"Spălătorie auto","optica":"Optică",
             "kineto":"Kinetoterapie","reparatii_electro":"Reparații electrocasnice","gsm":"Service GSM",
             "service_auto":"Service auto"}

def run(cmd, **kw):
    print("   $", " ".join(cmd))
    return subprocess.run(cmd, cwd=BASE, **kw)

def pretty_hours(hours_s, fallback="La programare"):
    if not hours_s: return fallback
    if hours_s == "nonstop": return "NON-STOP (24/7)"
    ZI = {"mon":"Luni","tue":"Marți","wed":"Miercuri","thu":"Joi","fri":"Vineri","sat":"Sâmbătă","sun":"Duminică"}
    ORD = ["mon","tue","wed","thu","fri","sat","sun"]
    def hhmm(x):
        h = int(x); return "%02d:%s" % (h, "30" if (x - h) >= 0.5 else "00")
    def cell(v):
        if v is None: return "Închis"
        if v == [0, 24]: return "Non-Stop"
        return "%s - %s" % (hhmm(v[0]), hhmm(v[1]))
    segs, i = [], 0
    while i < 7:
        j = i
        while j + 1 < 7 and hours_s.get(ORD[j+1]) == hours_s.get(ORD[i]): j += 1
        lbl = ZI[ORD[i]] if i == j else ZI[ORD[i]] + " - " + ZI[ORD[j]]
        segs.append("%s: %s" % (lbl, cell(hours_s.get(ORD[i])))); i = j + 1
    return " | ".join(segs)

def next_number():
    txt = open(LISTA, encoding="utf-8").read()
    nums = [int(m) for m in re.findall(r"^\S+\s+(\d+)\.\s", txt, re.M)]
    return (max(nums) + 1) if nums else 1

def entry_block(nr, lead):
    nk = lead.get("niche_key", "")
    emoji = EMOJI.get(nk, "📍")
    cat = CAT_SCURT.get(nk, nk)
    zona = (re.search(r"Sector\s*\d", lead.get("address", "")) or [None])
    zona = zona.group(0) if hasattr(zona, "group") else "București"
    link = "%s/%s.html" % (LIVE_BASE, lead["slug"])
    rating = str(lead.get("rating", "")).replace(".", ",")
    fb = " (are DOAR pagină de Facebook)" if lead.get("fb_only") else ""
    program = pretty_hours(lead.get("hours_s"), lead.get("program_text") or "La programare")
    azi = date.today().strftime("%Y-%m-%d")
    pitch = ("Bună ziua! Numele meu este Savu Mihai Samuel, sunt programator local în București. "
             "Am găsit %s%s, dar am observat că nu aveți un site web propriu. Am creat un prototip de site mobil premium, "
             "unde clienții vă găsesc rapid serviciile și programul și vă pot scrie direct pe WhatsApp. Îl puteți testa live aici:\n%s\n\n"
             "Dacă vă place și doriți să îl adaptăm cu detaliile exacte și să îl lansăm ca site oficial, vă ajut cu mare drag. O zi excelentă!"
             % (lead["name"], (" și recenziile foarte bune (%s★, %s recenzii)" % (rating, lead.get("reviews_count")))
                if str(lead.get("rating","")) not in ("", "—", "None") else "", link))
    return """
--------------------------------------------------------------------------------
%s %d. %s (%s / %s)
--------------------------------------------------------------------------------
*   Locație: %s
*   Telefon: %s
*   Program de Lucru: %s
*   Link Prototip Live: %s
*   Stare: Activ, NU deține site web propriu%s. Reputație %s★ (%s recenzii Google). Verificat Google Maps %s. Mockup v2 (%s).
*   Pitch (Mesaj WhatsApp de trimis):
%s
""" % (emoji, nr, lead["name"], cat, zona, lead.get("address",""), lead["phone_display"],
       program, link, fb, rating, lead.get("reviews_count",""), azi,
       lead.get("archetype") or g2.NICHE_PRESETS.get(nk,{}).get("archetype","v2"), pitch)

# ─────────────────────────────────────────────── scrape
def cmd_scrape(args):
    out_raw = os.path.join(BASE, "leads_found.json")
    cmd = [VENV_PY, os.path.join(BASE, "scrape_maps_leads.py"),
           "--min-rating", str(args.min_rating), "--min-reviews", str(args.min_reviews),
           "--max-per-niche", str(args.max_per_niche), "--scroll", str(args.scroll),
           "--out", "leads_found.json"]
    if args.niches: cmd += ["--niches", args.niches]
    elif args.niches_file: cmd += ["--niches-file", args.niches_file]
    else: sys.exit("dă --niches sau --niches-file")
    r = run(cmd)
    if r.returncode != 0: sys.exit("scraper a eșuat")
    leads = g2.from_scraped(out_raw)
    # completează fb_only din raw
    raw = {g2.norm_phone(x["phone"]): x for x in json.load(open(out_raw, encoding="utf-8"))}
    for l in leads:
        src = raw.get(l["phone_wa"][2:])
        if src: l["fb_only"] = src.get("fb_only", False)
    json.dump(leads, open(PENDING, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n[✓] %d leaduri pregătite → %s" % (len(leads), PENDING))
    print("    Revizuiește copy-ul (omul de la mijloc), apoi: python3 pipeline_leads.py publish")

# ─────────────────────────────────────────────── publish
def wait_live(slugs, tries=30, sleep_s=10):
    import urllib.request
    left = set(slugs)
    for i in range(tries):
        for slug in list(left):
            url = "%s/%s.html" % (LIVE_BASE, slug)
            try:
                with urllib.request.urlopen(url, timeout=10) as resp:
                    if resp.status == 200: left.discard(slug)
            except Exception: pass
        if not left:
            print("   [✓] toate live (~%ds)" % ((i+1)*sleep_s)); return True
        time.sleep(sleep_s)
    print("   [!] încă ne-live:", ", ".join(left)); return False

def cmd_publish(args):
    src = args.json_in or PENDING
    leads = json.load(open(src, encoding="utf-8"))
    if not leads: sys.exit("niciun lead în " + src)
    print("═══ generez %d mockup-uri v2 ═══" % len(leads))
    files = []
    for lead in leads:
        html = g2.build2(lead)
        p = os.path.join(g2.OUT_DIR, lead["slug"] + ".html")
        open(p, "w", encoding="utf-8").write(html)
        files.append("mockupuri/%s.html" % lead["slug"])
        print("✓ %-46s %6d octeți" % (lead["slug"], len(html.encode("utf-8"))))
    if args.dry_run:
        print("\n[dry-run] fără push/listă. Preview intrare pentru primul lead:")
        print(entry_block(next_number(), leads[0]))
        return
    # 1) push mockupuri
    print("═══ push mockupuri ═══")
    run(["git", "add"] + files)
    run(["git", "commit", "-q", "-m", "Pipeline: %d mockupuri v2 noi" % len(leads)])
    run(["git", "push", "origin", "master"])
    # 2) verific live
    print("═══ verific live ═══")
    ok = wait_live([l["slug"] for l in leads])
    if not ok and not args.force:
        sys.exit("[!] opresc înainte de listă — rulează din nou publish după ce Pages e ok (sau --force)")
    # 3) abia acum scriu în listă + push
    print("═══ scriu intrările în SITEURI_DE_TESTAT.txt ═══")
    nr = next_number()
    with open(LISTA, "a", encoding="utf-8") as f:
        f.write("\n================================================================================\n")
        f.write("PIPELINE %s\n" % date.today().strftime("%d-%m-%Y"))
        f.write("================================================================================\n")
        for i, lead in enumerate(leads):
            f.write(entry_block(nr + i, lead))
            print("   + %d. %s" % (nr + i, lead["name"]))
    run(["git", "add", "SITEURI_DE_TESTAT.txt"])
    run(["git", "commit", "-q", "-m", "Pipeline: intrari %d-%d in lista" % (nr, nr + len(leads) - 1)])
    run(["git", "push", "origin", "master"])
    os.rename(src, src + ".published") if os.path.exists(src) else None
    print("\n═══ GATA: %d leaduri live + în listă (nr. %d-%d) ═══" % (len(leads), nr, nr + len(leads) - 1))

# ─────────────────────────────────────────────── move
def cmd_move(args):
    txt = open(LISTA, encoding="utf-8").read()
    # blocul = separatorul dinainte de header-ul cu numărul + tot până la următorul separator/heading
    pat = re.compile(
        r"\n?-{20,}\n\S+\s+%d\.\s[^\n]*\n-{20,}\n.*?(?=\n-{20,}\n\S+\s+\d+\.|\n=+\n|\Z)" % args.numar,
        re.S)
    m = pat.search(txt)
    if not m: sys.exit("nu găsesc intrarea nr. %d în listă" % args.numar)
    block = m.group(0)
    name_m = re.search(r"\d+\.\s+(.+?)(?:\s*\(|\n)", block)
    tel_m = re.search(r"Telefon:\s*([\d\s/]+)", block)
    name = name_m.group(1).strip() if name_m else "?"
    tel = tel_m.group(1).strip() if tel_m else "?"
    txt = txt.replace(block, "")
    open(LISTA, "w", encoding="utf-8").write(txt)
    line = "%03d. %-60s |  Tel: %-22s | Status: %s\n" % (args.numar, name[:60], tel, args.status)
    with open(TESTED, "a", encoding="utf-8") as f:
        f.write(line)
    print("[✓] mutat #%d %s → tested_leads.txt (%s)" % (args.numar, name, args.status))
    if not args.no_push:
        run(["git", "add", "SITEURI_DE_TESTAT.txt", "tested_leads.txt"])
        run(["git", "commit", "-q", "-m", "Pipeline move: #%d %s -> tested (%s)" % (args.numar, name, args.status)])
        run(["git", "push", "origin", "master"])

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scrape")
    s.add_argument("--niches"); s.add_argument("--niches-file")
    s.add_argument("--min-rating", type=float, default=4.0)
    s.add_argument("--min-reviews", type=int, default=10)
    s.add_argument("--max-per-niche", type=int, default=5)
    s.add_argument("--scroll", type=int, default=7)
    s.set_defaults(fn=cmd_scrape)
    p = sub.add_parser("publish")
    p.add_argument("json_in", nargs="?")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_publish)
    m = sub.add_parser("move")
    m.add_argument("numar", type=int)
    m.add_argument("--status", default="TESTAT")
    m.add_argument("--no-push", action="store_true")
    m.set_defaults(fn=cmd_move)
    args = ap.parse_args()
    args.fn(args)

if __name__ == "__main__":
    main()
