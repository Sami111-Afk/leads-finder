# -*- coding: utf-8 -*-
import os
import re
import json

def normalize_phone(phone):
    if not phone:
        return ""
    digits = re.sub(r'\D', '', phone)
    if digits.startswith("40"):
        digits = digits[2:]
    elif digits.startswith("0"):
        digits = digits[1:]
    return digits

def normalize_name(name):
    if not name:
        return ""
    # Remove emoji, bracket notes like (Barber Shop Premium), and normalize text
    name = re.sub(r'[\u2600-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDF00-\uDFFF]|\uD83D[\uDFFF-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF]', '', name)
    name = re.sub(r'\(.*?\)', '', name)
    name = name.lower()
    name = re.sub(r'[^a-z0-9]', '', name)
    return name

def get_existing_leads():
    existing_phones = set()
    existing_names = set()
    
    # 1. Parse tested_leads.txt
    tested_path = "tested_leads.txt"
    if os.path.exists(tested_path):
        with open(tested_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # Format: XXX. Name | Tel: Phone | Status: Status
                if '|' in line:
                    parts = line.split('|')
                    name_part = parts[0].strip()
                    # Remove number prefix, e.g. "001. "
                    name_part = re.sub(r'^\d+\.\s*', '', name_part)
                    name_norm = normalize_name(name_part)
                    if name_norm:
                        existing_names.add(name_norm)
                    
                    if len(parts) > 1 and 'Tel:' in parts[1]:
                        phone_val = parts[1].replace('Tel:', '').strip()
                        phone_norm = normalize_phone(phone_val)
                        if phone_norm:
                            existing_phones.add(phone_norm)

    # 2. Parse siteuri_clienti.txt
    siteuri_path = "siteuri_clienti.txt"
    if os.path.exists(siteuri_path):
        with open(siteuri_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Find all entries
            # Titles like: --- \n emoji XXX. Name \n ---
            # Phone like: *   Telefon: Phone
            entries = content.split('--------------------------------------------------------------------------------')
            for entry in entries:
                lines = [l.strip() for l in entry.strip().split('\n') if l.strip()]
                if not lines:
                    continue
                # The first line might contain the name
                title_line = lines[0]
                # Match "XXX. Name" or just take name after number
                m = re.search(r'\d+\.\s*(.*)', title_line)
                if m:
                    name_val = m.group(1).strip()
                    name_norm = normalize_name(name_val)
                    if name_norm:
                        existing_names.add(name_norm)
                
                # Check for Phone in lines
                for line in lines:
                    if 'Telefon:' in line or 'Tel:' in line:
                        phone_val = line.split(':')[-1].strip()
                        phone_norm = normalize_phone(phone_val)
                        if phone_norm:
                            existing_phones.add(phone_norm)

    # 3. Parse lista_claude_siteuri.txt
    claude_path = "lista_claude_siteuri.txt"
    if os.path.exists(claude_path):
        with open(claude_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            entries = content.split('--------------------------------------------------------------------------------')
            for entry in entries:
                lines = [l.strip() for l in entry.strip().split('\n') if l.strip()]
                if not lines:
                    continue
                title_line = lines[0]
                m = re.search(r'\d+\.\s*(.*)', title_line)
                if m:
                    name_val = m.group(1).strip()
                    name_norm = normalize_name(name_val)
                    if name_norm:
                        existing_names.add(name_norm)
                
                for line in lines:
                    if 'Telefon:' in line or 'Tel:' in line:
                        phone_val = line.split(':')[-1].strip()
                        phone_norm = normalize_phone(phone_val)
                        if phone_norm:
                            existing_phones.add(phone_norm)

    # 3.5. Parse agy_lista1
    agy_path = "agy_lista1"
    if os.path.exists(agy_path):
        with open(agy_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            entries = content.split('--------------------------------------------------------------------------------')
            for entry in entries:
                lines = [l.strip() for l in entry.strip().split('\n') if l.strip()]
                if not lines:
                    continue
                title_line = lines[0]
                m = re.search(r'\d+\.\s*(.*)', title_line)
                if m:
                    name_val = m.group(1).strip()
                    name_norm = normalize_name(name_val)
                    if name_norm:
                        existing_names.add(name_norm)
                
                for line in lines:
                    if 'Telefon:' in line or 'Tel:' in line:
                        phone_val = line.split(':')[-1].strip()
                        phone_norm = normalize_phone(phone_val)
                        if phone_norm:
                            existing_phones.add(phone_norm)


    # 4. Check files in mockupuri
    mockup_dir = "mockupuri"
    if os.path.exists(mockup_dir):
        for fname in os.listdir(mockup_dir):
            if fname.endswith(".html"):
                base = fname[:-5] # remove .html
                # Clean prefix of categories like electrician_, instalator_, vidanjare_, tractari_, lacatus_, sticlari_, pest_control_, frigorifice_
                for prefix in ["electrician_", "instalator_", "vidanjare_", "tractari_", "lacatus_", "sticlari_", "pest_control_", "frigorifice_", "frigotehnist_"]:
                    if base.startswith(prefix):
                        base = base[len(prefix):]
                name_norm = normalize_name(base)
                if name_norm:
                    existing_names.add(name_norm)

    return {
        "phones": list(existing_phones),
        "names": list(existing_names)
    }

if __name__ == "__main__":
    data = get_existing_leads()
    print(f"Total existing unique normalized names: {len(data['names'])}")
    print(f"Total existing unique normalized phones: {len(data['phones'])}")
    with open("existing_leads_db.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print("Saved to existing_leads_db.json")
