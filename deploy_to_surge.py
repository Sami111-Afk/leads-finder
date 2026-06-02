import subprocess
import sys
import os

def deploy(project_path, domain):
    print(f"\n[+] Inițiere deploy pentru: {project_path} -> https://{domain}")
    # Comanda surge
    cmd = ["npx", "surge", "--project", project_path, "--domain", domain]
    
    # Setăm variabilele de mediu pentru login non-interactiv
    env = os.environ.copy()
    env["SURGE_LOGIN"] = "savu.mihai.samuel.pfa@gmail.com"
    env["SURGE_TOKEN"] = "ca0f80c5e8e4053ee3437f3421ad6747"
    
    try:
        # Rulăm comanda sincron
        res = subprocess.run(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )
        print("[+] Rezultat Surge:")
        print(res.stdout)
        if res.stderr:
            print("[!] Erori/Avertismente:")
            print(res.stderr)
        return res.returncode == 0
    except subprocess.TimeoutExpired:
        print("[!] Timeout expirat la conectare/upload!")
        return False
    except Exception as e:
        print(f"[!] Eroare neașteptată: {str(e)}")
        return False

# Lista cu folderele de mockup și domeniile Surge dorite
deploys = [
    ("./teds_beauty_studio", "teds-beauty-mosilor.surge.sh"),
    ("./animal_plus", "animal-plus-mosilor.surge.sh"),
    ("./brilliant_roses", "brilliant-roses-mosilor.surge.sh"),
    ("./boston_shoes", "boston-shoes-carol.surge.sh"),
    ("./grande_pet_salon", "grande-pet-mosilor.surge.sh")
]

print("=== START DEPLOYMENT PE SURGE.SH ===")
successful_deploys = []

for folder, domain in deploys:
    success = deploy(folder, domain)
    if success:
        successful_deploys.append((folder, domain))
        print(f"[✓] Succes: https://{domain} este live!")
    else:
        print(f"[✗] Eșec la deploy-ul pentru {folder}")

print("\n=== REZUMAT DEPLOY ===")
for folder, domain in successful_deploys:
    print(f"- {folder} -> https://{domain}")
