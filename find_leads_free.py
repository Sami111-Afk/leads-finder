import urllib.parse
import csv
import time
import argparse
import requests
from bs4 import BeautifulSoup

def search_duckduckgo_free(query, max_results=30):
    """
    Caută pe DuckDuckGo HTML (fără API key) și returnează link-urile și descrierile.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    encoded_query = urllib.parse.quote(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
    
    print(f"\n[+] Se caută gratuit pe DuckDuckGo: '{query}'...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"[!] Eroare de conexiune la DuckDuckGo (Status {response.status_code})")
            return []
    except Exception as e:
        print(f"[!] Eroare la request: {str(e)}")
        return []
        
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("div", class_="result")
    
    leads = []
    for r in results:
        title_el = r.find("a", class_="result__snippet")
        title_title = r.find("a", class_="result__a")
        if not title_title:
            continue
            
        title = title_title.text.strip()
        link = title_title["href"]
        
        # Extrage link-ul real din redirect-ul DuckDuckGo dacă e cazul
        if "uddg=" in link:
            link = urllib.parse.unquote(link.split("uddg=")[1].split("&")[0])
            
        snippet = title_el.text.strip() if title_el else ""
        
        leads.append({
            "Titlu": title,
            "Link": link,
            "Descriere/Snippet": snippet
        })
        
        if len(leads) >= max_results:
            break
            
    return leads

def filter_facebook_leads(results):
    """
    Filtrează paginile de Facebook care ar putea fi afaceri locale fără site web.
    """
    filtered = []
    for res in results:
        link = res["Link"]
        # Filtrăm doar rezultatele care sunt pagini de Facebook (nu grupuri sau postări specifice)
        if "facebook.com" in link and not any(x in link for x in ["/groups/", "/posts/", "/photo", "/videos/"]):
            # Încercăm să curățăm URL-ul de Facebook
            clean_link = link.split("?")[0]
            filtered.append({
                "Nume Afacere": res["Titlu"].replace(" | Facebook", "").replace(" - Facebook", ""),
                "Pagina Facebook": clean_link,
                "Snippet": res["Descriere/Snippet"]
            })
    return filtered

def main():
    parser = argparse.ArgumentParser(description="Găsește pagini de Facebook ale afacerilor locale (Metoda gratuită)")
    parser.add_argument("--oras", required=True, help="Orașul în care cauți (ex: Brasov, Sibiu, Constanta)")
    parser.add_argument("--nisa", required=True, help="Nisa de afaceri (ex: 'salon', 'cabinet stomatologic', 'pensiune')")
    
    args = parser.parse_args()
    
    # Căutăm pagini de Facebook pentru afacerile care au doar social media
    query = f'site:facebook.com "{args.nisa}" "{args.oras}"'
    
    raw_results = search_duckduckgo_free(query, max_results=50)
    leads = filter_facebook_leads(raw_results)
    
    print(f"\n[+] Am găsit {len(leads)} potențiale afaceri locale cu pagini de Facebook:")
    for i, lead in enumerate(leads, 1):
        print(f"{i}. {lead['Nume Afacere']}")
        print(f"   Link: {lead['Pagina Facebook']}")
        print(f"   Info: {lead['Snippet']}\n")
        
    if leads:
        filename = f"leads_free_{args.nisa.replace(' ', '_')}_{args.oras.replace(' ', '_')}.csv"
        keys = leads[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(leads)
        print(f"[+] Am salvat rezultatele în: {filename}")
    else:
        print("[!] Nu am găsit pagini de Facebook relevante pentru această căutare.")

if __name__ == "__main__":
    main()
