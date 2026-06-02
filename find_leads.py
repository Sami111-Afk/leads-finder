import os
import csv
import json
import argparse
import requests

def search_leads(api_key, query, max_results=20):
    """
    Căută afaceri folosind Google Places API (New) și filtrează
    doar pe cele care nu au site sau au doar pagină de Social Media.
    """
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.nationalPhoneNumber,places.websiteUri,places.rating,places.userRatingCount"
    }
    
    payload = {
        "textQuery": query,
        "pageSize": min(max_results, 20)  # Limita API-ului per request este de 20
    }
    
    print(f"\n[+] Se caută afaceri pentru: '{query}'...")
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"[!] Eroare API ({response.status_code}): {response.text}")
            return []
    except Exception as e:
        print(f"[!] Eroare de conexiune: {str(e)}")
        return []
        
    data = response.json()
    places = data.get("places", [])
    
    leads = []
    for place in places:
        name = place.get("displayName", {}).get("text", "Nume Necunoscut")
        address = place.get("formattedAddress", "Fără adresă")
        phone = place.get("nationalPhoneNumber", "Fără telefon")
        website = place.get("websiteUri", "")
        rating = place.get("rating", "N/A")
        reviews = place.get("userRatingCount", 0)
        
        # Filtrare: Căutăm afaceri FĂRĂ site sau cu site doar pe Facebook/Instagram
        is_lead = False
        status = ""
        
        if not website:
            is_lead = True
            status = "Fără site web"
        elif any(domain in website.lower() for domain in ["facebook.com", "instagram.com", "fb.me", "t.me"]):
            is_lead = True
            status = f"Doar Social Media ({website})"
            
        if is_lead:
            leads.append({
                "Nume": name,
                "Telefon": phone,
                "Adresă": address,
                "Rating": rating,
                "Recenzii": reviews,
                "Website Actual": website if website else "Niciunul",
                "Status": status
            })
            
    return leads

def save_to_csv(leads, filename):
    if not leads:
        print("[!] Nu există lead-uri de salvat.")
        return
        
    keys = leads[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f: # utf-8-sig pentru suport Excel în limba română
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(leads)
    print(f"[+] Succes! Am salvat {len(leads)} lead-uri în fișierul: {filename}")

def main():
    parser = argparse.ArgumentParser(description="Detector de clienți fără site web (Google Places API)")
    parser.add_argument("--key", help="Cheia Google Places API (opțional, poate fi setată și ca variabilă de mediu PLACES_API_KEY)")
    parser.add_argument("--oras", required=True, help="Orașul în care cauți (ex: Brasov, Sibiu, Cluj)")
    parser.add_argument("--nisa", required=True, help="Nisa de afaceri (ex: 'cabinet stomatologic', 'salon infrumusetare', 'service auto')")
    parser.add_argument("--limita", type=int, default=20, help="Numărul maxim de rezultate primite de la API (max 20 per request)")
    
    args = parser.parse_args()
    
    # Preluare cheie API din argumente sau din variabila de mediu
    api_key = args.key or os.environ.get("PLACES_API_KEY")
    
    if not api_key:
        print("\n[!] Atenție: Nu ai furnizat o cheie Google API.")
        print("Obține o cheie gratuită din Google Cloud Console (cu Places API activat).")
        api_key = input("Introduceți cheia API acum: ").strip()
        if not api_key:
            print("[!] Fără cheie API, scriptul nu poate rula. Ieșire.")
            return

    query = f"{args.nisa} {args.oras}"
    leads = search_leads(api_key, query, args.limita)
    
    print(f"\n[+] Am găsit {len(leads)} afaceri potrivite (fără site sau doar cu social media):")
    for i, lead in enumerate(leads, 1):
        print(f"{i}. {lead['Nume']} | Tel: {lead['Telefon']} | Status: {lead['Status']}")
        
    if leads:
        output_file = f"leads_{args.nisa.replace(' ', '_')}_{args.oras.replace(' ', '_')}.csv"
        save_to_csv(leads, output_file)

if __name__ == "__main__":
    main()
