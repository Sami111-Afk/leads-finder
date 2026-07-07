# -*- coding: utf-8 -*-
import os
import re
import random
import json
import subprocess

LEADS = [
    # 1. Psihiatrie & Neurologie
    {
        "niche": "psihiatrie_neurologie", "emoji": "🧠", "name": "Cabinet Psihiatrie Dr. Andrei Marinescu",
        "phone": "0723 111 999", "location": "Calea Moșilor nr. 222, Sector 2, București",
        "program": "Luni - Vineri: 09:00 - 19:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Sănătate mintală &", "slogan_part2": "consiliere psihiatrică specializată",
        "desc_niche": "psihiatrie, evaluare psihologică și terapie de suport",
        "services": [
            {"icon": "🧠", "name": "Consultații Psihiatrie", "desc": "Diagnosticare și tratament anxietate, depresie, atacuri de panică, tulburări de somn sau burnout."},
            {"icon": "📝", "name": "Avize & Referate Medicale", "desc": "Eliberare certificate medicale pentru comisie, referate psihiatrice, avize pentru angajare sau port-armă."},
            {"icon": "🤝", "name": "Psihoterapie & Consiliere", "desc": "Ședințe individuale de psihoterapie cognitiv-comportamentală pentru gestionarea crizelor emoționale."}
        ],
        "image_url": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=600&q=80", "prefix": "psihiatrie_"
    },
    {
        "niche": "psihiatrie_neurologie", "emoji": "🧠", "name": "Cabinet Neurologie Dr. Simona Popescu",
        "phone": "0744 222 000", "location": "Bulevardul Primăverii nr. 35, Sector 1, București",
        "program": "Luni - Vineri: 08:30 - 18:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Diagnostic neurologie &", "slogan_part2": "tratamente afecțiuni neurologice",
        "desc_niche": "neurologie clinică, ecografii Doppler și consultații de specialitate",
        "services": [
            {"icon": "⚡", "name": "Consultații Neurologie", "desc": "Evaluare clinică pentru dureri de cap, migrene, vertij, furnicături, hernii de disc sau tulburări de memorie."},
            {"icon": "📟", "name": "Doppler Vase Carotidiene", "desc": "Investigație ecografică Doppler color a arterelor gâtului pentru evaluarea riscului de accident vascular."},
            {"icon": "💊", "name": "Tratament Nevralgii & Durere", "desc": "Infiltrații locale și scheme moderne de tratament medicamentos pentru nevralgii sau dureri cronice de spate."}
        ],
        "image_url": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&w=600&q=80", "prefix": "neurologie_"
    },
    {
        "niche": "psihiatrie_neurologie", "emoji": "🧠", "name": "Consult Psihiatric & Psihoterapie Dr. Radu",
        "phone": "0722 333 111", "location": "Strada Dristorului nr. 24, Sector 3, București",
        "program": "Luni - Vineri: 09:00 - 20:00 | Sâmbătă: 10:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Evaluări psihiatrice &", "slogan_part2": "ședințe de psihoterapie",
        "desc_niche": "cabinet medical de psihiatrie și psihoterapie individuală",
        "services": [
            {"icon": "🧠", "name": "Evaluare Psihiatrică Inițială", "desc": "Consult clinic detaliat pentru stabilirea diagnosticului și elaborarea schemei terapeutice adecvate."},
            {"icon": "💊", "name": "Urmărire Tratamente", "desc": "Monitorizarea evoluției sub tratament medicamentos și ajustarea dozelor pentru siguranță maximă."},
            {"icon": "🗣️", "name": "Terapie de Familie / Cuplu", "desc": "Consiliere psihoterapeutică pentru rezolvarea conflictelor de cuplu sau gestionarea dinamicilor familiale."}
        ],
        "image_url": "https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=600&q=80", "prefix": "psihiatrie_"
    },
    {
        "niche": "psihiatrie_neurologie", "emoji": "🧠", "name": "Clinica Neurologie & Psihiatrie Sector 4",
        "phone": "0761 444 222", "location": "Șoseaua Olteniței nr. 112, Sector 4, București",
        "program": "Luni - Vineri: 09:00 - 19:00 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Diagnostic neuro-psihiatric",
        "slogan_part2": "și tratament integrat",
        "desc_niche": "cabinet integrat de neurologie, psihiatrie și psihologie",
        "services": [
            {"icon": "🩺", "name": "Consult Diagnostic Integrat", "desc": "Abordare multidisciplinară a afecțiunilor care implică atât componenta neurologică, cât și cea psihiatrică."},
            {"icon": "📟", "name": "Electroencefalogramă (EEG)", "desc": "Înregistrare non-invazivă a activității creierului pentru diagnosticarea epilepsiei sau tulburărilor de somn."},
            {"icon": "💊", "name": "Tratament Tulburări Demență", "desc": "Ghidaj terapeutic și suport pentru pacienții cu Alzheimer sau alte forme de demență cognitivă."}
        ],
        "image_url": "https://images.unsplash.com/photo-1530026405186-ed1ea0ac7a63?auto=format&fit=crop&w=600&q=80", "prefix": "neurologie_"
    },

    # 2. Endocrinologie
    {
        "niche": "endocrinologie", "emoji": "🩺", "name": "Cabinet Endocrinologie Dr. Elena Georgescu",
        "phone": "0723 555 111", "location": "Strada Viitorului nr. 82, Sector 2, București",
        "program": "Luni - Vineri: 09:00 - 19:00 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Consultații endocrine &", "slogan_part2": "ecografii tiroidiene detaliate",
        "desc_niche": "cabinet endocrinologie, ecografie tiroidă și tratamente hormonale",
        "services": [
            {"icon": "🩺", "name": "Consultații Endocrinologie", "desc": "Diagnosticare și tratament afecțiuni tiroidiene, hipofizare, suprarenale sau tulburări de metabolism."},
            {"icon": "📟", "name": "Ecografie Glandă Tiroidă", "desc": "Examinare ecografică de înaltă rezoluție pentru depistarea nodulilor tiroidieni sau semnelor de tiroidită (Autoimună Hashimoto)."},
            {"icon": "🔬", "name": "Profil Hormonal Complet", "desc": "Interpretare analize de laborator: TSH, FT4, hormoni sexuali și stabilirea schemelor terapeutice optime."}
        ],
        "image_url": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=600&q=80", "prefix": "endocrinologie_"
    },
    {
        "niche": "endocrinologie", "emoji": "🩺", "name": "Clinica Endocrinologie Dr. Maria Ionescu",
        "phone": "0744 666 222", "location": "Bulevardul Lascăr Catargiu nr. 12, Sector 1, București",
        "program": "Luni - Vineri: 09:00 - 19:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Sănătate hormonală &", "slogan_part2": "tratamente endocrine personalizate",
        "desc_niche": "endocrinologie clinică, osteoporoză și planning hormonal",
        "services": [
            {"icon": "🦴", "name": "Diagnostic Osteoporoză", "desc": "Evaluarea metabolismului calciu-fosfor, recomandări osteodensitometrie (DEXA) și tratamente de combatere a osteoporozei."},
            {"icon": "🔬", "name": "Endocrinologie Pediatrică", "desc": "Monitorizarea creșterii și dezvoltării pubertare a copiilor, depistarea din timp a deficitelor de hormon de creștere."},
            {"icon": "💊", "name": "Terapie Ovare Polichistice", "desc": "Diagnosticarea sindromului de ovare polichistice (SOPC), tratament hormonal și nutrițional pentru echilibrare."}
        ],
        "image_url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=600&q=80", "prefix": "endocrinologie_"
    },
    {
        "niche": "endocrinologie", "emoji": "🩺", "name": "Consult Endocrinologic Dr. Popa",
        "phone": "0722 777 333", "location": "Calea Dudești nr. 104, Sector 3, București",
        "program": "Luni - Vineri: 08:30 - 20:00 | Sâmbătă: 09:00 - 13:00 | Duminică: Închis",
        "slogan_part1": "Ecografie tiroidiană &", "slogan_part2": "consultații rapide endocrinologie",
        "desc_niche": "cabinet medical de endocrinologie clinică și ecografie Doppler",
        "services": [
            {"icon": "🔬", "name": "Diagnostic Tiroidită Autoimună", "desc": "Identificarea anticorpilor specifici (ATPO) și gestionarea tratamentului de substituție hormonală (Euthyrox)."},
            {"icon": "📟", "name": "Ecografie Doppler Glande", "desc": "Evaluarea vascularizației glandei tiroide pentru depistarea nodulilor activi sau proceselor inflamatorii."},
            {"icon": "💊", "name": "Endocrinologie & Infertilitate", "desc": "Evaluarea disfuncțiilor endocrine care pot împiedica apariția unei sarcini și tratamente specifice de cuplu."}
        ],
        "image_url": "https://images.unsplash.com/photo-1579684389782-64d84b5e901d?auto=format&fit=crop&w=600&q=80", "prefix": "endocrinologie_"
    },
    {
        "niche": "endocrinologie", "emoji": "🩺", "name": "Cabinet Diabet & Nutriție Dr. Stancu",
        "phone": "0761 888 444", "location": "Șoseaua Olteniței nr. 22, Sector 4, București",
        "program": "Luni - Vineri: 09:00 - 18:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Diabet zaharat &", "slogan_part2": "nutriție clinică personalizată",
        "desc_niche": "consult diabet, stabilire scheme insulină și diete clinice",
        "services": [
            {"icon": "🩸", "name": "Monitorizare Diabet Tip 1 / Tip 2", "desc": "Diagnosticare, prescriere scheme de tratament cu antidiabetice orale sau scheme complexe de insulinoterapie."},
            {"icon": "🥗", "name": "Dietoterapie Personalizată", "desc": "Elaborare diete personalizate pentru diabetici, combaterea obezității sau reglarea indicelui glicemic."},
            {"icon": "🩺", "name": "Screening Picior Diabetic", "desc": "Evaluare periodică neurologică și vasculară a picioarelor pentru prevenirea complicațiilor grave ale diabetului."}
        ],
        "image_url": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=600&q=80", "prefix": "diabet_"
    },

    # 3. Ortopedie
    {
        "niche": "ortopedie", "emoji": "🦴", "name": "Cabinet Ortopedie Dr. Adrian Radu",
        "phone": "0723 999 555", "location": "Calea Moșilor nr. 120, Sector 2, București",
        "program": "Luni - Vineri: 09:00 - 19:30 | Sâmbătă: 09:00 - 13:00 | Duminică: Închis",
        "slogan_part1": "Diagnostic ortopedic &", "slogan_part2": "infiltrații intra-articulare acid hialuronic",
        "desc_niche": "ortopedie-traumatologie, infiltrații genunchi/umăr și recuperare",
        "services": [
            {"icon": "🦴", "name": "Consultații Ortopedie", "desc": "Diagnosticare și tratament artroză (gonartroză, coxartroză), tendinite, entorse, fracturi sau luxații."},
            {"icon": "💉", "name": "Infiltrații Acid Hialuronic / PRP", "desc": "Proceduri terapeutice intra-articulare cu acid hialuronic premium sau plasmă îmbogățită cu trombocite (PRP/Terapie Vampir)."},
            {"icon": "🩹", "name": "Imobilizări Ghipsate Moderne", "desc": "Aplicare atele sau fașe ghipsate moderne din fibră de sticlă, mult mai ușoare și rezistente la apă."}
        ],
        "image_url": "https://images.unsplash.com/photo-1579684389782-64d84b5e901d?auto=format&fit=crop&w=600&q=80", "prefix": "ortopedie_"
    },
    {
        "niche": "ortopedie", "emoji": "🦴", "name": "Clinica Ortopedie Dr. Mihai Popescu",
        "phone": "0744 888 666", "location": "Strada Paris nr. 18, Sector 1, București",
        "program": "Luni - Vineri: 09:00 - 19:00 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Consultații chirurgie ortopedică",
        "slogan_part2": "și diagnosticare avansată",
        "desc_niche": "chirurgie ortopedică, artroscopie și protezări articulare",
        "services": [
            {"icon": "🏥", "name": "Chirurgie Artroscopică Genunchi", "desc": "Consult pre-operator și recomandări de artroscopie pentru leziuni de menisc, ligament încrucișat anterior (LIA)."},
            {"icon": "🦴", "name": "Evaluare Protezare Șold/Genunchi", "desc": "Diagnosticare artroze severe și evaluare în vederea intervențiilor de artroplastie (proteză șold/genunchi)."},
            {"icon": "🩹", "name": "Tratament Traumatologie Sportivă", "desc": "Managementul leziunilor articulare la sportivi: rupturi musculare, entorse severe, tendinopatii."}
        ],
        "image_url": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=600&q=80", "prefix": "ortopedie_"
    },
    {
        "niche": "ortopedie", "emoji": "🦴", "name": "Consult Ortopedic Sector 3",
        "phone": "0722 666 999", "location": "Calea Dudești nr. 188, Sector 3, București",
        "program": "Luni - Vineri: 08:30 - 20:00 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Ecografie musculo-scheletală &",
        "slogan_part2": "recuperare funcțională",
        "desc_niche": "ortopedie, ecografie aparat locomotor și infiltrații",
        "services": [
            {"icon": "📟", "name": "Ecografie Musculo-Scheletală", "desc": "Examinare ecografică rapidă a tendoanelor, mușchilor și articulațiilor pentru depistarea rupturilor sau inflamațiilor."},
            {"icon": "💉", "name": "Terapie Infiltrații antiinflamatorii", "desc": "Infiltrații ghidate ecografic cu substanțe antiinflamatoare pentru ameliorarea rapidă a durerilor acute."},
            {"icon": "🩹", "name": "Ortezare & Suport", "desc": "Recomandare orteze personalizate pentru gleznă, genunchi sau coloană în vederea recuperării optime."}
        ],
        "image_url": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&w=600&q=80", "prefix": "ortopedie_"
    },
    {
        "niche": "ortopedie", "emoji": "🦴", "name": "Recuperare Ortopedică Sector 4",
        "phone": "0761 333 888", "location": "Șoseaua Olteniței nr. 14, Sector 4, București",
        "program": "Luni - Vineri: 09:00 - 18:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Remediere dureri articulare &",
        "slogan_part2": "recuperare după fracturi",
        "desc_niche": "traumatologie clinică, infiltrații articulare și urmărire post-operatorie",
        "services": [
            {"icon": "🦴", "name": "Control Post-Operator", "desc": "Scoatere fire sutură, evaluare radiografii de control și stabilirea planului de kinetoterapie post-operator."},
            {"icon": "💉", "name": "Infiltrații PRP (Trombocite)", "desc": "Injectare concentrat propriu de trombocite pentru stimularea regenerării tendoanelor și cartilajului deteriorat."},
            {"icon": "📋", "name": "Referate Comisie Expertiză", "desc": "Eliberare referate detaliate de diagnostic pentru comisiile de expertiză medicală a capacității de muncă."}
        ],
        "image_url": "https://images.unsplash.com/photo-1530026405186-ed1ea0ac7a63?auto=format&fit=crop&w=600&q=80", "prefix": "ortopedie_"
    },

    # 4. Spălătorie Profesională Covoare
    {
        "niche": "spalatorie_covoare", "emoji": "🧼", "name": "Eco Clean Covoare București",
        "phone": "0722 121 343", "location": "Strada Lucrețiu Pătrășcanu nr. 12, Sector 3, București",
        "program": "Luni - Sâmbătă: 08:00 - 20:00 | Duminică: Închis",
        "slogan_part1": "Spălare profesională covoare &",
        "slogan_part2": "ridicare/livrare gratuită la domiciliu",
        "desc_niche": "spălătorie automată de covoare cu detergenți ecologici",
        "services": [
            {"icon": "🧼", "name": "Spălare Automată Covoare", "desc": "Spălare în linie automată cu tren de perii rotative, clătire abundentă și centrifugare pentru eliminarea 95% a apei."},
            {"icon": "🚚", "name": "Livrare Gratuită Domiciliu", "desc": "Preluăm covoarele murdare direct de la ușa ta și ți le aducem înapoi curate, uscate și parfumate în 48-72 de ore."},
            {"icon": "💨", "name": "Uscare în Cameră Climatizată", "desc": "Uscare rapidă în spațiu special cu dezumidificatoare industriale, eliminând complet riscul apariției mirosului de igrasie."}
        ],
        "image_url": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=600&q=80", "prefix": "spalatorie_covoare_"
    },
    {
        "niche": "spalatorie_covoare", "emoji": "🧼", "name": "Spălătoria de Covoare Premium Mihai",
        "phone": "0765 232 454", "location": "Strada Apusului nr. 62, Sector 6, București",
        "program": "Luni - Sâmbătă: 08:30 - 19:30 | Duminică: Închis",
        "slogan_part1": "Curățare profundă covoare",
        "slogan_part2": "cu utilaje de ultimă generație",
        "desc_niche": "spălătorie covoare, eliminare pete și igienizare",
        "services": [
            {"icon": "🧼", "name": "Eliminare Pete & Mirosuri", "desc": "Tratamente speciale pentru îndepărtarea urmelor de cafea, vin, grăsimi sau miros de urină de animale de companie."},
            {"icon": "🌀", "name": "Bătut & Desprăfuit Mecanic", "desc": "Desprăfuire profundă cu utilaj vibro-aspirator înainte de spălarea umedă, eliminând tot nisipul din baza covorului."},
            {"icon": "✨", "name": "Finisare & Ambalare în Folie", "desc": "Aspirare finală de finisare, periere pentru ridicarea pufului, parfumare discretă și ambalare în folie de protecție."}
        ],
        "image_url": "https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?auto=format&fit=crop&w=600&q=80", "prefix": "spalatorie_covoare_"
    },
    {
        "niche": "spalatorie_covoare", "emoji": "🧼", "name": "Curățare Covoare Rapid Andrei",
        "phone": "0733 454 656", "location": "Strada Agricultori nr. 110, Sector 2, București",
        "program": "Luni - Duminică: 08:00 - 21:00",
        "slogan_part1": "Spălătorie covoare rapidă",
        "slogan_part2": "livrare în 48 de ore",
        "desc_niche": "spălare automată covoare și covoare persane sensibile",
        "services": [
            {"icon": "🎨", "name": "Spălare Covoare Lână / Persane", "desc": "Curățare manuală sau ecologică la temperaturi joase cu detergenți neutri pentru a nu afecta culorile și fibrele de lână."},
            {"icon": "⚡", "name": "Serviciu Express 48h", "desc": "Spălare și uscare rapidă în regim de urgență cu livrare în maxim 48 de ore direct la domiciliul tău."},
            {"icon": "🛏️", "name": "Curățare Saltele & Canapele", "desc": "Echipă mobilă dotată cu aspiratoare injecție-extracție pentru curățarea tapițeriilor direct la adresa ta."}
        ],
        "image_url": "https://images.unsplash.com/photo-1540518614846-7eded433c457?auto=format&fit=crop&w=600&q=80", "prefix": "spalatorie_covoare_"
    },
    {
        "niche": "spalatorie_covoare", "emoji": "🧼", "name": "Atelier Curățătorie Covoare Sector 4",
        "phone": "0765 565 767", "location": "Șoseaua Olteniței nr. 142, Sector 4, București",
        "program": "Luni - Vineri: 09:00 - 18:30 | Sâmbătă: 09:00 - 15:00 | Duminică: Închis",
        "slogan_part1": "Igienizare antibacteriană covoare",
        "slogan_part2": "și tratamente anti-acarieni",
        "desc_niche": "curățătorie covoare, igienizare profundă și periere",
        "services": [
            {"icon": "🛡️", "name": "Igienizare Sanytol / Ozon", "desc": "Tratamente specifice dezinfectante pentru eliminarea bacteriilor, virusurilor și acarienilor din covoare și mochete."},
            {"icon": "🧼", "name": "Spălare Mochete Mari", "desc": "Preluare și curățare mochete de mari dimensiuni din birouri sau pensiuni, oferind factură și prețuri avantajoase."},
            {"icon": "🌀", "name": "Tratament Balsam & Înmuiere", "desc": "Utilizare balsam profesional care lasă fibrele moi la atingere și redă culorile inițiale ale covorului."}
        ],
        "image_url": "https://images.unsplash.com/photo-1607860108855-64acf2078ed9?auto=format&fit=crop&w=600&q=80", "prefix": "spalatorie_covoare_"
    },

    # 5. Service Biciclete & Trotinete
    {
        "niche": "service_biciclete", "emoji": "🚲", "name": "BiciFix Service Biciclete Sector 3",
        "phone": "0722 123 456", "location": "Strada Baba Novac nr. 10, Sector 3, București",
        "program": "Luni - Vineri: 10:00 - 19:30 | Sâmbătă: 10:00 - 15:00 | Duminică: Închis",
        "slogan_part1": "Reparații biciclete rapid &",
        "slogan_part2": "revizii complete sezoniere",
        "desc_niche": "service biciclete, reglaje frâne/schimbătoare și centrat roți",
        "services": [
            {"icon": "🔧", "name": "Revizie Generală Biciclete", "desc": "Verificare generală strângeri, ungere lanț/cabluri, reglaj fin frâne și schimbătoare, centrat roți și umflare pneuri."},
            {"icon": "🛑", "name": "Service Frâne Hidraulice", "desc": "Înlocuire plăcuțe, aerisire și schimbare ulei mineral/DOT, înlocuire discuri frână și calibrare etriere."},
            {"icon": "⚙️", "name": "Schimbare Transmisie & Lanț", "desc": "Înlocuire lanț uzat, casetă pinioane, foi angrenaj, cabluri și cămăși schimbător pentru o rulare lină."}
        ],
        "image_url": "https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=600&q=80", "prefix": "service_biciclete_"
    },
    {
        "niche": "service_biciclete", "emoji": "⚡", "name": "Service Trotinete Electrice Militari",
        "phone": "0765 987 654", "location": "Bulevardul Iuliu Maniu nr. 56, Sector 6, București",
        "program": "Luni - Vineri: 09:30 - 18:30 | Sâmbătă: 10:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Reparații trotinete electrice",
        "slogan_part2": "și înlocuire anvelope pline",
        "desc_niche": "service trotinete electrice Xiaomi, Ninebot, Dualtron și reparații baterii",
        "services": [
            {"icon": "🚲", "name": "Montaj Anvelope Pline / Camere", "desc": "Schimbăm rapid camere sparte sau montăm anvelope pline anti-pană pentru Xiaomi m365 și alte modele uzuale."},
            {"icon": "⚡", "name": "Reparații Electronice & Baterii", "desc": "Remedieri erori software/hardware, lipire celule baterie, înlocuire controllere arse sau porturi de încărcare defecte."},
            {"icon": "🛑", "name": "Reglaje Frâne & Joc Ghidon", "desc": "Eliminare joc în ghidon (pliere), montaj amortizoare suplimentare, reglaj frână disc sau frână electromagnetică."}
        ],
        "image_url": "https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=600&q=80", "prefix": "service_trotinete_"
    },
    {
        "niche": "service_biciclete", "emoji": "🚲", "name": "Atelier Biciclete & Trotinete Marius",
        "phone": "0733 112 233",
        "location": "Strada Avrig nr. 42, Sector 2, București",
        "program": "Luni - Sâmbătă: 09:00 - 19:00 | Duminică: Închis",
        "slogan_part1": "Centrat roți & reparații",
        "slogan_part2": "furci și suspensii biciclete",
        "desc_niche": "atelier de reparații biciclete, service furci și piese schimb",
        "services": [
            {"icon": "🌀", "name": "Centrat Roți & Spire", "desc": "Centrări roți optice (strâmbe), înlocuire spițe rupte, tensionare și remontare anvelope și camere noi."},
            {"icon": "🔧", "name": "Service Furci & Amortizoare", "desc": "Revizie furci pe aer sau arc (RockShox, Fox), curățare, schimbare semeringuri și ulei pentru o suspensie optimă."},
            {"icon": "🚲", "name": "Montaj Accesorii Custom", "desc": "Montăm aripi, portbagaje, suporturi bidon, ciclocomputere, lumini LED sau kituri de conversie electrică."}
        ],
        "image_url": "https://images.unsplash.com/photo-1508962914676-134849a727f0?auto=format&fit=crop&w=600&q=80", "prefix": "service_biciclete_"
    },
    {
        "niche": "service_biciclete", "emoji": "🚲", "name": "Velo Clinic București Sector 4",
        "phone": "0765 444 333",
        "location": "Șoseaua Olteniței nr. 18, Sector 4, București",
        "program": "Luni - Vineri: 10:00 - 19:00 | Sâmbătă: 10:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Service biciclete profesional",
        "slogan_part2": "piese originale în stoc",
        "desc_niche": "reparații biciclete de oraș, cursiere și MTB-uri direct în sectorul 4",
        "services": [
            {"icon": "🔧", "name": "Spălare & Degresare Transmisie", "desc": "Curățare profundă în baie ecologică a casetei, lanțului și schimbătoarelor de depuneri de vaselină și praf."},
            {"icon": "🚲", "name": "Service Butuci & Cuve Cadru", "desc": "Înlocuire rulmenți sau bile butuc roată, curățare și gresare cuve cadru (cuvete ghidon) și monobloc pedalier."},
            {"icon": "🛑", "name": "Pregătire pentru Sezonul Rece", "desc": "Conservem bicicleta pe timp de iarnă: aplicare ceară protectoare pe cadru, ungere specială anti-rugină."}
        ],
        "image_url": "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?auto=format&fit=crop&w=600&q=80", "prefix": "service_biciclete_"
    },

    # 6. Închirieri Rochii & Costume
        {
        "niche": "burgeri_fastfood",
        "emoji": "🍔",
        "name": "MgBurger Dorobanți",
        "phone": "0720 533 223",
        "location": "Piața Dorobanți nr. 6, Sector 1, București",
        "program": "Luni - Duminică: 08:00 - 01:00",
        "slogan_part1": "Burgeri suculenți premium",
        "slogan_part2": "în Piața Dorobanți",
        "desc_niche": "burgeri gourmet din carne de vită premium, sosuri speciale și cartofi proaspeți",
        "services": [
            {"icon": "🍔", "name": "Burgeri Gourmet", "desc": "Burgeri din carne de vită Black Angus, cheddar topit, bacon crocant și sos special."},
            {"icon": "🍟", "name": "Garnituri delicioase", "desc": "Cartofi prăjiți cu parmezan și usturoi, inele de ceapă și sosuri preparate zilnic."},
            {"icon": "🥤", "name": "Meniuri combo", "desc": "Meniu complet cu burgerul preferat, cartofi crocanți și băutură răcoritoare la preț redus."}
        ],
        "image_url": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=600&q=80",
        "prefix": "mgburger_"
    },
    {
        "niche": "inchirieri_rochii", "emoji": "👗", "name": "Bridal Rent București",
        "phone": "0765 888 999", "location": "Strada Viitorului nr. 122, Sector 2, București",
        "program": "Luni - Sâmbătă: 10:00 - 19:30 | Duminică: Închis",
        "slogan_part1": "Rochii de mireasă elegante",
        "slogan_part2": "disponibile spre închiriere",
        "desc_niche": "închiriere rochii de mireasă, rochii de ocazie și retușuri croitorie",
        "services": [
            {"icon": "👗", "name": "Rochii de Mireasă tip Prințesă / Sirenă", "desc": "Colecții variate croite din materiale fine: dantelă franțuzească, mătase naturală, tulle fin și aplicații manuale."},
            {"icon": "✂️", "name": "Serviciu Retuș Gratuit", "desc": "Croitoarele noastre fac retușurile necesare pe silueta ta (scurtat, strâmtat, adăugare bretele) gratuit în prețul închirierii."},
            {"icon": "🧼", "name": "Curățare Ecologică inclusă", "desc": "Nu îți face griji pentru murdăria de după petrecere. Curățarea chimică profesională a rochiei este asigurată complet de noi."}
        ],
        "image_url": "https://images.unsplash.com/photo-1549570652-97324981a6fd?auto=format&fit=crop&w=600&q=80", "prefix": "inchirieri_rochii_"
    },
    {
        "niche": "inchirieri_rochii", "emoji": "👔", "name": "Închirieri Costume & Tuxedo Alex",
        "phone": "0731 222 111", "location": "Calea Văcărești nr. 12, Sector 3, București",
        "program": "Luni - Sâmbătă: 09:30 - 19:30 | Duminică: Închis",
        "slogan_part1": "Costume de ginere &",
        "slogan_part2": "tuxedo premium de închiriat",
        "desc_niche": "închiriere costume bărbătești, tuxedo și accesorii pentru domni",
        "services": [
            {"icon": "👔", "name": "Închiriere Tuxedo / Smoking", "desc": "Costume elegante de tip smoking negru sau navy cu guler din satin, pantaloni asortați și cămăși de ceremonie fine."},
            {"icon": "👔", "name": "Costume Business & Evenimente", "desc": "Costume clasice din lână pentru interviuri, prezentări, botezuri sau balul bobocilor, ajustate pe măsura ta."},
            {"icon": "👞", "name": "Accesorii Domni (Papion, Butoni)", "desc": "Închiriere accesorii complete: papioane din mătase, lavaliere, butoni manșetă, curele din piele și pantofi eleganți."}
        ],
        "image_url": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=600&q=80", "prefix": "inchirieri_costume_"
    },
    {
        "niche": "inchirieri_rochii", "emoji": "👗", "name": "Rochii de Seară Rent Ioana",
        "phone": "0764 777 999", "location": "Strada Apusului nr. 22, Sector 6, București",
        "program": "Luni - Sâmbătă: 10:00 - 19:00 | Duminică: Probe cu programare",
        "slogan_part1": "Rochii de ocazie de închiriat",
        "slogan_part2": "pentru orice petrecere",
        "desc_niche": "închirieri rochii de seară scurte/lungi și consiliere vestimentară",
        "services": [
            {"icon": "👗", "name": "Rochii Corporate / Cocktail", "desc": "Tinute elegante potrivite pentru evenimente corporate, banchete sau petreceri de tip cocktail."},
            {"icon": "👗", "name": "Rochii Domnișoare Onoare", "desc": "Pachete promoționale pentru închirierea de rochii asortate ca model și culoare pentru toate domnișoarele de onoare."},
            {"icon": "🤝", "name": "Consiliere Stilistică Gratuită", "desc": "Stilistul nostru te ajută să alegi croiala și culorile care te avantajează cel mai bine în funcție de eveniment."}
        ],
        "image_url": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=600&q=80", "prefix": "inchirieri_rochii_"
    },

    # 7. Școală de Dans & Balet
    {
        "niche": "scoala_dans", "emoji": "💃", "name": "Dance Studio București Simona",
        "phone": "0722 333 888", "location": "Strada Viitorului nr. 45, Sector 2, București",
        "program": "Luni - Vineri: 14:00 - 22:00 | Sâmbătă: 10:00 - 16:00 | Duminică: Închis",
        "slogan_part1": "Cursuri de dans copii &",
        "slogan_part2": "cursuri dans de nuntă (Valsul Mirilor)",
        "desc_niche": "școală de dans, coregrafie valsul mirilor și dansuri moderne",
        "services": [
            {"icon": "👰", "name": "Coregrafie Valsul Mirilor", "desc": "Lecții private 1-la-1 pentru realizarea unei coregrafii unice pe melodia preferată pentru deschiderea nunții dumneavoastră."},
            {"icon": "👶", "name": "Dans Modern & Streetdance Copii", "desc": "Cursuri de dans pline de energie pentru copii de 4-14 ani: dezvoltare ritm, coordonare și coregrafii spectaculoase."},
            {"icon": "🕺", "name": "Dansuri de Societate & Latino", "desc": "Cursuri de grup pentru adulți: salsa, bachata, tango, vals, cha-cha. Perfect pentru socializare și mișcare."}
        ],
        "image_url": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=600&q=80", "prefix": "scoala_dans_"
    },
    {
        "niche": "scoala_dans", "emoji": "🩰", "name": "Școala de Balet pentru Copii Alina",
        "phone": "0765 555 444", "location": "Strada Paris nr. 10, Sector 1, București",
        "program": "Luni - Vineri: 12:00 - 20:00 | Sâmbătă: 09:00 - 15:00 | Duminică: Închis",
        "slogan_part1": "Balet clasic copii &",
        "slogan_part2": "gimnastică ritmică balet",
        "desc_niche": "cursuri balet clasic copii, postură și flexibilitate",
        "services": [
            {"icon": "🩰", "name": "Inițiere Balet Copii (3-6 ani)", "desc": "Ședințe jucăușe axate pe descoperirea ritmului, flexibilității, coordonării de bază și dezvoltarea posturii corecte."},
            {"icon": "🩰", "name": "Balet Avansați (7-14 ani)", "desc": "Antrenamente riguroase pe poante, studiu la bară, coregrafii clasice și pregătire pentru spectacole și concursuri."},
            {"icon": "🤸", "name": "Gimnastică & Flexibilitate", "desc": "Exerciții specifice pentru dezvoltarea elasticității musculare și mobilității articulare în siguranță."}
        ],
        "image_url": "https://images.unsplash.com/photo-1518834107812-67b0b7c58434?auto=format&fit=crop&w=600&q=80", "prefix": "scoala_balet_"
    },
    {
        "niche": "scoala_dans", "emoji": "🕺", "name": "Zumba & Latino Dance Club Dristor",
        "phone": "0731 111 222", "location": "Strada Dristorului nr. 8, Sector 3, București",
        "program": "Luni - Vineri: 16:30 - 21:30 | Sâmbătă: 10:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Zumba fitness &",
        "slogan_part2": "cursuri salsa bachata Dristor",
        "desc_niche": "cursuri zumba fitness, dansuri latino-americane și mișcare",
        "services": [
            {"icon": "🔥", "name": "Ședințe Zumba Fitness", "desc": "Antrenamente cardio distractive pe ritmuri latino care te ajută să arzi calorii, să te distrezi și să te tonifiezi rapid."},
            {"icon": "🕺", "name": "Cursuri Salsa & Bachata", "desc": "Învățarea pașilor de bază, ritmului și figurilor de dans pentru petreceri de profil. Grupe de începători lunare."},
            {"icon": "🤸", "name": "Dansuri Populare Adulți", "desc": "Cursuri recreative de dansuri populare românești (hore, sârbe), perfecte pentru petrecerile de nuntă."}
        ],
        "image_url": "https://images.unsplash.com/photo-1504609773096-104ff2c73ba4?auto=format&fit=crop&w=600&q=80", "prefix": "scoala_dans_"
    },
    {
        "niche": "scoala_dans", "emoji": "💃", "name": "Atelierul de Dans Sector 6",
        "phone": "0764 555 444", "location": "Strada Apusului nr. 12, Sector 6, București",
        "program": "Luni - Vineri: 15:00 - 22:00 | Sâmbătă: 10:00 - 15:00 | Duminică: Închis",
        "slogan_part1": "Streetdance & modern dance",
        "slogan_part2": "cursuri dinamice de dans",
        "desc_niche": "școală de streetdance, hip-hop, dans modern și breakdance",
        "services": [
            {"icon": "⚡", "name": "Streetdance & Hip-Hop", "desc": "Cursuri de dans urban cu coregrafi tineri, axate pe freestyle, coordonare, ritm și mișcări dinamice."},
            {"icon": "🤸", "name": "Breakdance & Acrobatie", "desc": "Inițiere în mișcările spectaculoase de breakdance (toprock, downrock, freeze-uri) combinate cu elemente de acrobatică."},
            {"icon": "🎉", "name": "Pregătire Show-uri & Flashmobs", "desc": "Creare de momente coregrafice deosebite pentru spectacole, evenimente private sau flashmob-uri la cerere."}
        ],
        "image_url": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=600&q=80", "prefix": "scoala_dans_"
    },

    # 8. Clinică Oftalmologie & Optică
    {
        "niche": "oftalmologie_optica", "emoji": "👓", "name": "Cabinet Oftalmologie Dr. Maria Popa",
        "phone": "0723 112 211", "location": "Calea Moșilor nr. 280, Sector 2, București",
        "program": "Luni - Vineri: 09:00 - 19:00 | Sâmbătă: 09:00 - 13:00 | Duminică: Închis",
        "slogan_part1": "Consultații oftalmologice &",
        "slogan_part2": "prescriere ochelari lentile contact",
        "desc_niche": "oftalmologie clinică, determinare dioptrii și optică medicală",
        "services": [
            {"icon": "🩺", "name": "Consultații Oftalmologie", "desc": "Examinare fund de ochi, măsurare tensiune oculară (prevenție glaucom), diagnosticare cataractă și prescriere rețete ochelari."},
            {"icon": "👓", "name": "Determinare Dioptrii computerizată", "desc": "Măsurători exacte cu refractometru computerizat pentru determinarea miopiei, hipermetropiei sau astigmatismului."},
            {"icon": "🔬", "name": "Adaptare Lentile de Contact", "desc": "Probe și instruire completă pentru aplicarea, igienizarea și purtarea sigură a lentilelor de contact moi sau rigide."}
        ],
        "image_url": "https://images.unsplash.com/photo-1579684389782-64d84b5e901d?auto=format&fit=crop&w=600&q=80", "prefix": "oftalmologie_"
    },
    {
        "niche": "oftalmologie_optica", "emoji": "👓", "name": "Clinica Oftalmologică Dr. Elena Rădulescu",
        "phone": "0744 223 322", "location": "Bulevardul Lascăr Catargiu nr. 42, Sector 1, București",
        "program": "Luni - Vineri: 09:00 - 19:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Investigații oftalmologice avansate",
        "slogan_part2": "oftalmologie pediatrică sector 1",
        "desc_niche": "oftalmologie avansată, oftalmopediatrie și tratament strabism",
        "services": [
            {"icon": "👶", "name": "Oftalmologie Pediatrică", "desc": "Consultații special concepute pentru copii mici: testare acuitate vizuală prin jocuri, depistare strabism sau ambliopie."},
            {"icon": "🔬", "name": "Măsurare Tensiune Oculară", "desc": "Tonometrie non-contact (cu jet de aer), absolut nedureroasă, esențială pentru screeningul glaucomului."},
            {"icon": "👁️", "name": "Tratament Ochi Uscat & Inflamații", "desc": "Diagnosticare sindrom de ochi uscat, prescriere lacrimi artificiale potrivite, tratamente pentru conjunctivite sau blefarite."}
        ],
        "image_url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=600&q=80", "prefix": "oftalmologie_"
    },
    {
        "niche": "oftalmologie_optica", "emoji": "👓", "name": "Optică Medicală Dristor Mihai",
        "phone": "0722 334 433", "location": "Strada Dristorului nr. 12, Sector 3, București",
        "program": "Luni - Vineri: 09:30 - 19:30 | Sâmbătă: 10:00 - 15:00 | Duminică: Închis",
        "slogan_part1": "Ochelari de vedere premium &",
        "slogan_part2": "rame moderne lentile Essilor",
        "desc_niche": "optică medicală, montaj ochelari la comandă și rame ochelari",
        "services": [
            {"icon": "👓", "name": "Execuție Ochelari de Vedere", "desc": "Montaj computerizat rapid de lentile monofocale, bifocale sau progresive (Essilor, Zeiss, Hoya) pe ramele alese."},
            {"icon": "🕶️", "name": "Rame Ochelari & Accesorii", "desc": "Gamă variată de rame din acetat, titan sau metal de la branduri renumite și accesorii (tocuri, lavete, lanțuri)."},
            {"icon": "🛠️", "name": "Reparații Ochelari Rapide", "desc": "Înlocuire pernuțe nazale, șuruburi, ajustare brațe strâmbe, lipire sau sudare rame metalice avariate."}
        ],
        "image_url": "https://images.unsplash.com/photo-1508296695146-257a814070b4?auto=format&fit=crop&w=600&q=80", "prefix": "optica_"
    },
    {
        "niche": "oftalmologie_optica", "emoji": "👓", "name": "Consult Oftalmologic Sector 4",
        "phone": "0761 445 544", "location": "Șoseaua Olteniței nr. 42, Sector 4, București",
        "program": "Luni - Vineri: 09:00 - 18:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Determinare dioptrii gratuită",
        "slogan_part2": "la achiziția ochelarilor",
        "desc_niche": "cabinet oftalmologic, determinări dioptrii și ochelari ieftini",
        "services": [
            {"icon": "👓", "name": "Determinare Dioptrii Gratuită", "desc": "Testare computerizată a vederii gratuită dacă alegeți să realizați ochelarii în atelierul nostru."},
            {"icon": "👓", "name": "Ochelari Citit & Distanță", "desc": "Realizare rapidă ochelari pentru citit sau distanță cu lentile cu protecție PC (filtru lumină albastră)."},
            {"icon": "🛡️", "name": "Lentile cu Protecție Solară", "desc": "Montaj lentile heliomate (Transitions) care se închid la soare sau lentile de soare cu dioptrii și polarizare."}
        ],
        "image_url": "https://images.unsplash.com/photo-1590486803833-1c5dc8ddd4c8?auto=format&fit=crop&w=600&q=80", "prefix": "oftalmologie_"
    },

    # 9. Cazare Inedită Tiny House
    {
        "niche": "cazare_tiny_house", "emoji": "🏡", "name": "Tiny House Snagov Retreat",
        "phone": "0722 888 111", "location": "Strada Principală nr. 120, Snagov, Ilfov",
        "program": "Luni - Duminică: Recepție / Check-in 14:00 - 22:00",
        "slogan_part1": "Cazare inedită tiny house",
        "slogan_part2": "lângă pădure pe malul lacului",
        "desc_niche": "cazare tiny house premium, glamping și relaxare în natură",
        "services": [
            {"icon": "🏡", "name": "Cazare Tiny House Modern", "desc": "Casă mică din lemn, complet utilată: pat la mansardă, chicinetă, baie modernă, aer condiționat și ferestre mari panoramice."},
            {"icon": "🛀", "name": "Hot Tub / Ciubăr Privată", "desc": "Ciubăr din fibră de sticlă cu hidromasaj exterior, încălzit cu lemne, amplasat privat pe terasa căsuței tale."},
            {"icon": "🚲", "name": "Plimbări Biciclete & Kayak", "desc": "Biciclete de munte și kayak-uri disponibile gratuit pentru explorarea pădurii și lacului Snagov."}
        ],
        "image_url": "https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=600&q=80", "prefix": "cazare_tiny_"
    },
    {
        "niche": "cazare_tiny_house", "emoji": "🏡", "name": "Glamping Tiny House Cernica",
        "phone": "0745 222 333", "location": "Strada Principală nr. 82, Cernica, Ilfov",
        "program": "Luni - Duminică: Recepție 09:00 - 21:00",
        "slogan_part1": "Căsuțe tiny house Cozy",
        "slogan_part2": "experiență inedită lângă Cernica",
        "desc_niche": "cazare cozy tiny house, zonă de grătar și hamace",
        "services": [
            {"icon": "🏡", "name": "Căsuțe Cozy Tiny House", "desc": "Căsuțe din lemn de tip A-Frame sau design minimalist, perfect izolate termic, dotate cu terase private exterioare."},
            {"icon": "🍖", "name": "Zonă Grătar & Foișor", "desc": "Foișor central utilat cu grătar pe cărbuni, plită și masă mare, ideal pentru seri relaxante alături de prieteni."},
            {"icon": "🌿", "name": "Zonă Relaxare Hamace", "desc": "Grădină liniștită umbrită de copaci mari, amenajată cu hamace și pufuri mari de relaxare (lazy bags)."}
        ],
        "image_url": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=600&q=80", "prefix": "cazare_tiny_"
    },
    {
        "niche": "cazare_tiny_house", "emoji": "🏡", "name": "Eco Tiny House Corbeanca",
        "phone": "0763 444 222", "location": "Strada Florilor nr. 56, Corbeanca, Ilfov",
        "program": "Luni - Duminică: Rezervări 09:00 - 21:00",
        "slogan_part1": "Tiny house sustenabil eco",
        "slogan_part2": "relaxare smart în Corbeanca",
        "desc_niche": "cazare tiny house ecologic, design minimalist și panouri solare",
        "services": [
            {"icon": "🏡", "name": "Eco Tiny House (Sustenabil)", "desc": "Căsuțe alimentate cu energie solară, finisate doar cu vopsele și uleiuri ecologice și sisteme de reciclare a apei."},
            {"icon": "🛀", "name": "Saună Umedă exterioară", "desc": "Acces la sauna umedă comună din sticlă și lemn, ideală pentru relaxare musculară și detoxifiere."},
            {"icon": "☕", "name": "Cafea de specialitate inclusă", "desc": "Fiecare căsuță este dotată cu espressor premium și cafea proaspătă de specialitate boabe pentru dimineți perfecte."}
        ],
        "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=600&q=80", "prefix": "cazare_tiny_"
    },
    {
        "niche": "cazare_tiny_house", "emoji": "🏡", "name": "Păstrăvăria & Cabana Runcu Ilfov",
        "phone": "0731 555 444", "location": "Strada Principală nr. 210, Runcu, Ilfov",
        "program": "Luni - Duminică: Recepție Non-Stop (24/7)",
        "slogan_part1": "Cazare cabană din lemn &",
        "slogan_part2": "păstrăvărie cu restaurant propriu",
        "desc_niche": "cazare cabană forestieră, păstrăvărie și restaurant pescăresc",
        "services": [
            {"icon": "🏡", "name": "Cazare Cabană Forestieră", "desc": "Cazare în camere decorate rustic cu accente din lemn masiv și piatră de munte, cu balcoane mari spre râu."},
            {"icon": "🐟", "name": "Păstrăvărie Privată & Pescuit", "desc": "Posibilitate de pescuit sportiv în bazinele noastre populate cu păstrăv curcubeu și pregătirea peștelui pe grătar."},
            {"icon": "🍳", "name": "Restaurant Pescăresc traditional", "desc": "Restaurant cu specific pescăresc (păstrăv la grătar, saramură, borș de pește) preparate după rețete locale tradiționale."}
        ],
        "image_url": "https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=600&q=80", "prefix": "cazare_cabana_"
    },

    # 10. Sisteme Securitate & Alarme
    {
        "niche": "securitate_alarme", "emoji": "🛡️", "name": "Smart Security Systems București",
        "phone": "0722 990 220", "location": "Calea Rahovei nr. 182, Sector 5, București",
        "program": "Luni - Vineri: 08:30 - 18:30 | Sâmbătă: 09:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Sisteme alarmă smart &",
        "slogan_part2": "camere supraveghere profesionale",
        "desc_niche": "proiectare, instalare și avizare sisteme de alarmă și supraveghere video",
        "services": [
            {"icon": "🚨", "name": "Instalare Sisteme Alarmă Ajax", "desc": "Montaj sisteme de alarmă wireless Ajax sau cablate DSC cu senzori de mișcare, geam spart, fum și inundație conectate la dispecerat."},
            {"icon": "📹", "name": "Camere Supraveghere Video IP", "desc": "Instalare camere de supraveghere IP 4K cu vizualizare pe telefonul mobil, detecție oameni și vehicule și stocare securizată."},
            {"icon": "🔐", "name": "Sisteme Control Acces & Interfoane", "desc": "Montaj video-interfoane inteligente IP, yale electromagnetice, cititoare de carduri și pontaj electronic pentru firme."}
        ],
        "image_url": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=600&q=80", "prefix": "securitate_alarme_"
    },
    {
        "niche": "securitate_alarme", "emoji": "🛡️", "name": "Sisteme Alarme & Supraveghere Otopeni",
        "phone": "0764 888 444", "location": "Calea Bucureștilor nr. 56, Otopeni, Ilfov",
        "program": "Luni - Vineri: 08:00 - 18:00 | Sâmbătă: 09:00 - 15:00 | Duminică: Închis",
        "slogan_part1": "Instalare camere video Hikvision",
        "slogan_part2": "sisteme de securitate Ilfov",
        "desc_niche": "instalare camere video, alarme efracție și mentenanță tehnică",
        "services": [
            {"icon": "📹", "name": "Montaj Camere Hikvision / Dahua", "desc": "Instalare camere video analog HD sau IP, configurare DVR/NVR, vizualizare la distanță prin aplicație mobilă securizată."},
            {"icon": "🚨", "name": "Alarme Efracție cu Senzori", "desc": "Sisteme de alarmă antiefracție cu tastaturi, sirene exterioare cu flash, senzori infraroșu și bariere perimetrice pentru curte."},
            {"icon": "🛠️", "name": "Mentenanță & Service Sisteme", "desc": "Remediere defecțiuni camere video offline, înlocuire acumulatori descărcați alarme, recalibrare senzori falși."}
        ],
        "image_url": "https://images.unsplash.com/photo-1508514177221-188b1cf16e9d?auto=format&fit=crop&w=600&q=80", "prefix": "securitate_alarme_"
    },
    {
        "niche": "securitate_alarme", "emoji": "🛡️", "name": "Montaj Camere Supraveghere Mihai",
        "phone": "0733 111 333", "location": "Strada Dezrobirii nr. 12, Sector 6, București",
        "program": "Luni - Sâmbătă: 08:00 - 19:00 | Duminică: Închis",
        "slogan_part1": "Camere video IP de securitate",
        "slogan_part2": "în București & Ilfov",
        "desc_niche": "reparații și montaj camere supraveghere și rețele IT",
        "services": [
            {"icon": "📹", "name": "Montaj Camere IP & Cablare", "desc": "Instalare camere de supraveghere video de tip IP prin cablu de rețea UTP (PoE), eliminând cablurile de alimentare vizibile."},
            {"icon": "📶", "name": "Configurare Rețea & Switch-uri", "desc": "Configurare routere, switch-uri cu management, rețea Wi-Fi stabilă pentru transmiterea fluidă a fluxurilor video."},
            {"icon": "🔧", "name": "Înlocuire Camere Vechi", "desc": "Modernizarea sistemului vechi analog cu camere moderne de înaltă rezoluție (Full HD/4K) folosind cablurile existente."}
        ],
        "image_url": "https://images.unsplash.com/photo-1613665813446-82a78c468a1d?auto=format&fit=crop&w=600&q=80", "prefix": "securitate_alarme_"
    },
    {
        "niche": "securitate_alarme", "emoji": "🛡️", "name": "Securitate Pro-Install Alex",
        "phone": "0765 222 444", "location": "Strada Turnu Măgurele nr. 12, Sector 4, București",
        "program": "Luni - Sâmbătă: 08:30 - 18:30 | Duminică: Închis",
        "slogan_part1": "Sisteme securitate certificate IGP",
        "slogan_part2": "proiectare avizare sisteme alarme",
        "desc_niche": "proiectare și instalare sisteme de securitate licențiate de Poliție (IGPR)",
        "services": [
            {"icon": "📜", "name": "Proiectare Sisteme de Securitate", "desc": "Elaborarea proiectelor tehnice obligatorii pentru firme, necesare pentru avizarea de către Direcția de Poliție competentă."},
            {"icon": "🚨", "name": "Alarme Efracție cu Licență", "desc": "Instalare sisteme de alarmă conforme normativelor legale, eliberarea jurnalului de service și punerea în funcțiune legală."},
            {"icon": "📹", "name": "Analiză Risc la Securitate", "desc": "Consultanță și evaluare a riscurilor la securitate fizică pentru spații comerciale sau case particulare."}
        ],
        "image_url": "https://images.unsplash.com/photo-1548613053-22087dd8edb8?auto=format&fit=crop&w=600&q=80", "prefix": "securitate_alarme_"
    }
]

PALETTES = {
    "psihiatrie_neurologie": {
        "primary": "#8b5cf6", "rgb": "139, 92, 246", "secondary": "#1e1b4b", "bg": "#faf5ff", "tag": "Cabinet Psihiatrie & Neurologie"
    },
    "endocrinologie": {
        "primary": "#06b6d4", "rgb": "6, 182, 212", "secondary": "#0f172a", "bg": "#ecfeff", "tag": "Cabinet Endocrinologie & Diabet"
    },
    "ortopedie": {
        "primary": "#3b82f6", "rgb": "59, 130, 246", "secondary": "#1e293b", "bg": "#eff6ff", "tag": "Cabinet Ortopedie & Recuperare"
    },
    "spalatorie_covoare": {
        "primary": "#0d9488", "rgb": "13, 148, 136", "secondary": "#0f172a", "bg": "#f0fdfa", "tag": "Spălătorie Profesională Covoare"
    },
    "service_biciclete": {
        "primary": "#16a34a", "rgb": "22, 163, 74", "secondary": "#111827", "bg": "#f0fdf4", "tag": "Service Biciclete & Trotinete"
    },
    "inchirieri_rochii": {
        "primary": "#db2777", "rgb": "219, 39, 119", "secondary": "#2e0821", "bg": "#fdf2f8", "tag": "Închirieri Rochii & Costume"
    },
    "scoala_dans": {
        "primary": "#ec4899", "rgb": "236, 72, 153", "secondary": "#2a0c1e", "bg": "#fdf2f8", "tag": "Școală de Dans & Balet"
    },
    "oftalmologie_optica": {
        "primary": "#0ea5e9", "rgb": "14, 165, 233", "secondary": "#0f172a", "bg": "#f0f9ff", "tag": "Clinică Oftalmologie & Optică"
    },
    "cazare_tiny_house": {
        "primary": "#d97706", "rgb": "217, 119, 6", "secondary": "#1e293b", "bg": "#faf7f5", "tag": "Cazare Inedită Tiny House"
    },
    "securitate_alarme": {
        "primary": "#dc2626", "rgb": "220, 38, 38", "secondary": "#0f172a", "bg": "#fef2f2", "tag": "Sisteme Securitate & Alarme"
    }
}

REVIEWS_TEMPLATES = {
    "psihiatrie_neurologie": [
        "Domnul Dr. Marinescu m-a ajutat să trec peste o perioadă extrem de grea de burnout și anxietate severă. Un medic extrem de cald și profesionist. Îi mulțumesc!",
        "Cabinet foarte curat, discuții deschise fără nicio judecată. Am primit tratamentul potrivit pentru insomnie și viața mea s-a îmbunătățit complet.",
        "Recomand din tot sufletul consultul neurologie oferit de doamna Dr. Popescu. Ecografia Doppler a fost extrem de amănunțită și m-am liniștit pe deplin.",
        "Colaborare excelentă pentru obținerea referatului psihiatric de comisie. Profesionalism desăvârșit, punctualitate și prețuri corecte."
    ],
    "endocrinologie": [
        "Am fost diagnosticată cu Tiroidită Hashimoto. Doamna Dr. Georgescu mi-a reglat doza de tratament și acum mă simt excelent, am energie din nou.",
        "Consultația de endocrinologie a fost extrem de detaliată, ecografia tiroidiană s-a făcut fără grabă. Recomand cabinetul cu multă căldură.",
        "Servicii de diabet și nutriție de top. Dr. Stancu m-a ajutat să îmi controlez diabetul prin dietă corectă și tratament optimizat. Vă mulțumesc!",
        "Recomand clinica pentru profesionalismul medicilor și atenția acordată pacientului. Am obținut planul de tratament pentru osteoporoză foarte repede."
    ],
    "ortopedie": [
        "Infiltrațiile cu acid hialuronic făcute de domnul Dr. Radu în genunchi au făcut minuni! Durerile de gonartroză au dispărut și mă pot plimba din nou.",
        "Recomand clinica. M-au operat de menisc și recuperarea a fost extraordinar de rapidă. Medic ortoped foarte experimentat și dedicat.",
        "Ecografia musculo-scheletală a identificat imediat ruptura de tendon pe care alții o trecuseră cu vederea. Un diagnostic extrem de precis. Mulțumesc!",
        "Control post-operator, scos fire și ghidaj recuperare excelent. Profesioniști adevărați în ortopedie și traumatologie în Sectorul 4."
    ],
    "spalatorie_covoare": [
        "Covoarele noastre de lână au fost spălate minunat. Au scos toate petele vechi făcute de copii și mirosurile neplăcute. Livrarea la domiciliu a fost perfectă!",
        "Cel mai bun serviciu de spălătorie de covoare din București. Vin, le iau de la ușă și le aduc curate, uscate complet și ambalate în folie în 3 zile. Recomand!",
        "Uscarea în cameră climatizată face diferența. Covoarele nu miros deloc a igrasie, sunt pufoase și foarte curate. Servicii de nota 10 cu felicitări.",
        "Recomand cu mare drag. Prețuri foarte bune pe metru pătrat, promptitudine în colectare și livrare gratuită pentru comenzi mai mari."
    ],
    "service_biciclete": [
        "Revizia generală la bicicletă a fost realizată impecabil. Reglajul schimbătoarelor este perfect, lanțul rulează extrem de lin. Mecanici excelenți!",
        "Service-ul de trotinete electrice din Militari mi-a înlocuit roțile cu camere cu anvelope pline anti-pană foarte rapid. Lucru bine făcut și preț avantajos.",
        "Centratul roților a decurs rapid, chiar în aceeași zi. Au spițat roata perfect și mi-au rezolvat jocul din ghidon la trotinetă. Recomand Marius!",
        "Foarte mulțumit de degresarea completă a transmisiei la cursiera mea. Bicicleta funcționează ca nouă. Un service de biciclete de încredere."
    ],
    "inchirieri_rochii": [
        "Rochia de mireasă închiriată a fost de-a dreptul superbă și retușurile croitoresei s-au potrivit la milimetru. M-am simțit ca o prințesă, mulțumesc Bella Sposa!",
        "Am închiriat o rochie lungă de seară spectaculoasă pentru o gală corporate. Prețul a fost excelent și a inclus curățarea chimică finală. Foarte serioși.",
        "Costumul tuxedo închiriat pentru nuntă a fost de înaltă clasă. Am primit butoni, papion și cămașă asortate. Ajustare impecabilă pe corp. Recomand Alex!",
        "Gama largă de rochii de seară de lux disponibile la prețuri rezonabile spre închiriere. Servicii de retuș și curățare de nota 10, fără bătăi de cap."
    ],
    "scoala_dans": [
        "Coregrafia creată pentru Valsul Mirilor a fost minunată și foarte ușor de învățat! Antrenoarea Simona a avut o răbdare de fier cu noi. Invitații au fost uimiți.",
        "Fetița mea merge cu mare plăcere la cursurile de balet clasic ale Alinei. Postura ei s-a îmbunătățit vizibil și merge mereu cu drag. Recomand!",
        "Ședințele de Zumba fitness sunt pline de distracție și energie! Arzi calorii dansând pe muzică latino excelentă. Cea mai bună modalitate de mișcare.",
        "Streetdance de calitate pentru adolescenți în Sectorul 6. Coregrafi tineri, antrenamente distractive și atmosferă foarte primitoare. Recomand clubul!"
    ],
    "oftalmologie_optica": [
        "Doamna Dr. Maria Popa mi-a oferit o consultație oftalmologică extrem de detaliată și mi-a prescris rețeta corectă de dioptrii. Cabinet foarte modern.",
        "Determinarea dioptriilor a fost computerizată și gratuită la achiziția ochelarilor de vedere. Ochelarii au fost gata a doua zi. Servicii prompte!",
        "Rame de ochelari moderne și lentile de calitate Essilor montate cu precizie în atelierul lor din Dristor. Recomand cu încredere serviciile lor.",
        "Consultație oftalmologică pediatrică excelentă. Medicul a avut multă răbdare cu băiețelul meu și i-a prescris ochelari potriviți. Mulțumim mult!"
    ],
    "cazare_tiny_house": [
        "O noapte petrecută în Tiny House la Snagov a fost o evadare perfectă din agitația Bucureștiului. Ciubărul cu apă fierbinte sub stele este genial!",
        "Căsuțele cozy de lângă Cernica sunt decorate superb și au o terasă imensă privată. Zona de grătar și hamacele din curte sunt perfecte. Recomand!",
        "Tiny House eco-sustenabil superb în Corbeanca. Design minimalist premium, saună exterioară fierbinte și cafea de specialitate delicioasă inclusă.",
        "Cazarea la cabana din Runcu cu păstrăvăria proprie a fost o experiență tradițională minunată. Mâncarea din restaurantul pescăresc a fost excepțională."
    ],
    "securitate_alarme": [
        "Instalarea sistemului de alarmă wireless Ajax a decurs extrem de rapid și curat, fără fire prin casă. Aplicația mobilă este foarte simplă. Recomand!",
        "Am montat camere de supraveghere IP 4K Hikvision în curte. Vizualizarea pe telefon este extrem de clară și detectează noaptea orice mișcare. Profesioniști.",
        "Echipa condusă de Mihai a configurat întreaga rețea IT și camerele video la sediul firmei noastre. Foarte rapizi, atenți și la prețuri corecte.",
        "Consultanta oferita pentru proiectul tehnic de securitate cerut de Politie a fost salvatoare. Totul a fost aprobat rapid, fără probleme. Recomand Alex!"
    ]
}

def make_slug(name):
    name_clean = name.lower()
    name_clean = re.sub(r'[^a-z0-9]', '_', name_clean)
    name_clean = re.sub(r'_+', '_', name_clean).strip('_')
    return name_clean

def get_sector(address):
    m = re.search(r"Sector\s*(\d)", address, re.IGNORECASE)
    if m:
        return m.group(1)
    return "București"

def generate_cui_reg():
    cui_num = random.randint(10000000, 99999999)
    reg_num = random.randint(1000, 9999)
    year = random.randint(2010, 2025)
    return f"RO{cui_num}", f"J40/{reg_num}/{year}"

def get_deterministic_reviews(i, name, niche):
    rng = random.Random(i)
    first_names = ["Mihai", "Andrei", "Cristian", "Stefan", "Alexandru", "Ioan", "Gabriel", "Elena", "Maria", "Ana", "Mihaela", "Florentina", "Raluca", "Adrian", "Florin", "Daniel", "Catalin", "Bogdan", "George", "Nicoleta", "Simona", "Denisa", "Marius", "Robert", "Gabriela"]
    last_names = ["Ionescu", "Popescu", "Radu", "Marin", "Dumitrescu", "Nistor", "Constantinescu", "Gheorghe", "Stancu", "Mihalcea", "Stoica", "Diaconu", "Savu", "Vasilescu", "Petrescu", "Nica", "Lupu", "Grosu", "Serban", "Voinea"]
    
    niche_templates = REVIEWS_TEMPLATES.get(niche, REVIEWS_TEMPLATES["securitate_alarme"])
    selected_templates = rng.sample(niche_templates, 3)
    
    reviews = []
    for t in selected_templates:
        first = rng.choice(first_names)
        last = rng.choice(last_names)
        rating = rng.choice([5, 5, 5, 4])
        rand_str = "".join(rng.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=17))
        google_link = f"https://share.google/{rand_str}"
        reviews.append({
            "author": f"{first} {last}",
            "text": t.format(name=name),
            "rating": rating,
            "google_link": google_link
        })
    return reviews

def make_reviews_html(reviews):
    html = '<div class="testimonials-grid reveal-group" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 30px;">'
    for r in reviews:
        stars = '★' * r['rating'] + '☆' * (5 - r['rating'])
        html += f"""
                <div class="testimonial-card">
                    <div>
                        <div class="testimonial-stars" style="color: #fbbf24; font-size: 1.2rem; margin-bottom: 12px;">{stars}</div>
                        <p class="testimonial-text" style="font-style: italic; color: var(--text-dark); line-height: 1.5; margin-bottom: 20px; font-size: 0.95rem;">"{r['text']}"</p>
                    </div>
                    <div class="testimonial-footer" style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color); padding-top: 12px; margin-top: auto; font-size: 0.85rem;">
                        <span class="testimonial-author" style="font-weight: 700; color: var(--text-dark);">{r['author']}</span>
                        <a href="{r['google_link']}" target="_blank" rel="noopener noreferrer" class="testimonial-link" style="color: var(--primary); text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;">Google 🔗</a>
                    </div>
                </div>"""
    html += '</div>'
    return html

def main():
    template_dir = "/home/sol/Projects/leads-finder/templates/local-business-onepage/src"
    dest_dir = "/home/sol/Projects/leads-finder/mockupuri"
    skeleton_path = "/home/sol/Projects/leads-finder/mockup_skeleton.html"
    
    style_path = os.path.join(template_dir, "style.css")
    app_js_path = os.path.join(template_dir, "app.js")
    
    with open(style_path, "r", encoding="utf-8") as f:
        style_content = f.read()
        
    with open(app_js_path, "r", encoding="utf-8") as f:
        app_js_content = f.read()
        
    with open(skeleton_path, "r", encoding="utf-8") as f:
        html_skeleton = f.read()
        
    os.makedirs(dest_dir, exist_ok=True)
    
    generated_mockups = []
    
    for idx, item in enumerate(LEADS):
        num = 501 + idx
        niche = item["niche"]
        name = item["name"]
        
        palette = PALETTES[niche]
        primary_color = palette["primary"]
        primary_rgb = palette["rgb"]
        secondary_color = palette["secondary"]
        bg_color = palette["bg"]
        tag = palette["tag"]
        
        sector = get_sector(item["location"])
        badge_text = f"{tag} Sector {sector}" if sector.isdigit() else f"{tag} {sector}"
        
        words = item["slogan_part1"].split() + item["slogan_part2"].split()
        mid = len(words) // 2
        part1 = " ".join(words[:mid])
        part2 = " ".join(words[mid:])
        
        phone_slug = item["phone"].replace(" ", "")
        phone_wa = "40" + phone_slug[1:] if phone_slug.startswith("0") else phone_slug
        
        maps_query = item["location"].replace(" ", "+").replace(",", "")
        maps_link = f"https://maps.google.com/?q={maps_query}"
        waze_link = f"https://waze.com/ul?q={maps_query}"
        
        cui, reg_com = generate_cui_reg()
        
        reviews = get_deterministic_reviews(num, name, niche)
        reviews_html = make_reviews_html(reviews)
        
        html_content = html_skeleton
        html_content = html_content.replace("__NAME__", name)
        html_content = html_content.replace("__EMOJI__", item["emoji"])
        html_content = html_content.replace("__SUBTITLE__", tag)
        html_content = html_content.replace("__SLOGAN_PART1__", part1)
        html_content = html_content.replace("__SLOGAN_PART2__", part2)
        html_content = html_content.replace("__DESC__", f"Servicii de {item['desc_niche']} în {item['location']}. Calitate superioară, promptitudine și servicii asigurate de specialiști atestați.")
        html_content = html_content.replace("__PHONE__", item["phone"])
        html_content = html_content.replace("__PHONE_FIXED_TEXT__", "")
        html_content = html_content.replace("__LOCATION__", item["location"])
        html_content = html_content.replace("__PROGRAM__", item["program"])
        html_content = html_content.replace("__PRIMARY_COLOR__", primary_color)
        html_content = html_content.replace("__PRIMARY_RGB__", primary_rgb)
        html_content = html_content.replace("__SECONDARY_COLOR__", secondary_color)
        html_content = html_content.replace("__BG_COLOR__", bg_color)
        html_content = html_content.replace("__BADGE_TEXT__", badge_text)
        
        html_content = html_content.replace("__SERVICE1_ICON__", item["services"][0]["icon"])
        html_content = html_content.replace("__SERVICE1_NAME__", item["services"][0]["name"])
        html_content = html_content.replace("__SERVICE1_DESC__", item["services"][0]["desc"])
        html_content = html_content.replace("__SERVICE2_ICON__", item["services"][1]["icon"])
        html_content = html_content.replace("__SERVICE2_NAME__", item["services"][1]["name"])
        html_content = html_content.replace("__SERVICE2_DESC__", item["services"][1]["desc"])
        html_content = html_content.replace("__SERVICE3_ICON__", item["services"][2]["icon"])
        html_content = html_content.replace("__SERVICE3_NAME__", item["services"][2]["name"])
        html_content = html_content.replace("__SERVICE3_DESC__", item["services"][2]["desc"])
        
        html_content = html_content.replace("__IMAGE_URL__", item["image_url"])
        html_content = html_content.replace("__PHONE_SLUG__", phone_slug)
        html_content = html_content.replace("__PHONE_WA__", phone_wa)
        html_content = html_content.replace("__CUI__", cui)
        html_content = html_content.replace("__REG_COM__", reg_com)
        html_content = html_content.replace("__MAPS_LINK__", maps_link)
        html_content = html_content.replace("__WAZE_LINK__", waze_link)
        html_content = html_content.replace("__REVIEWS_GRID__", reviews_html)
        
        html_content = html_content.replace("__STYLE_CSS__", style_content)
        
        js_replaced = app_js_content
        js_replaced = js_replaced.replace("[NUME_AFACERE]", name)
        js_replaced = js_replaced.replace("[NUMAR_WHATSAPP]", phone_wa)
        js_replaced = js_replaced.replace("[ID_GA4]", "G-LEAD" + str(num))
        
        html_content = html_content.replace("__APP_JS__", js_replaced)
        
        filename = f"{item['prefix']}{make_slug(name)}.html"
        file_path = os.path.join(dest_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        generated_mockups.append({
            "num": num,
            "name": name,
            "emoji": item["emoji"],
            "phone": item["phone"],
            "location": item["location"],
            "program": item["program"],
            "filename": filename,
            "live_url": f"https://sami111-afk.github.io/leads-finder/mockupuri/{filename}"
        })
        print(f"Generated {num}: {filename}")
        
    # Append to registers
    tested_path = "/home/sol/Projects/leads-finder/tested_leads.txt"
    siteuri_path = "/home/sol/Projects/leads-finder/siteuri_clienti.txt"
    agy_path = "/home/sol/Projects/leads-finder/agy_lista1"
    
    tested_entries = []
    siteuri_entries = []
    agy_entries = []
    
    for item in generated_mockups:
        # tested_leads.txt format
        tested_entries.append(f"{item['num']:03d}. {item['name']:50s} | Tel: {item['phone']:25s} | Status: ACTIV (Mockup păstrat)")
        
        # agy_lista1 format
        agy_block = (
            f"--------------------------------------------------------------------------------\n"
            f"{item['emoji']} {item['num']}. {item['name']}\n"
            f"--------------------------------------------------------------------------------\n"
            f"*   Locație: {item['location']}\n"
            f"*   Telefon: {item['phone']}\n"
            f"*   Program de Lucru: {item['program']}\n"
            f"*   Link Prototip Live: {item['live_url']}\n"
            f"*   Stare: Activ, nu deține site web propriu.\n"
        )
        agy_entries.append(agy_block)
        
        # siteuri_clienti.txt format (same as agy but with pitch)
        pitch_msg = (
            f"Bună ziua! Numele meu este Savu Mihai Samuel, sunt programator local în Sectorul 2/3. "
            f"Căutând servicii bune din cartier, am găsit recomandările excelente pentru afacerea dumneavoastră, "
            f"dar am observat că nu aveți un site web de prezentare propriu. Am creat un prototip de site mobil "
            f"premium, optimizat complet, unde clienții vă pot găsi rapid orarul, adresa și serviciile oferite și "
            f"vă pot trimite mesaje sau programări direct pe WhatsApp. Îl puteți testa live la acest link:\n"
            f"{item['live_url']}\n\n"
            f"Dacă doriți să îl adaptăm cu detaliile exacte și să îl lansăm ca site oficial, vă ajut cu mare drag. "
            f"O zi excelentă!"
        )
        siteuri_block = agy_block + f"*   Pitch (Mesaj WhatsApp de trimis):\n{pitch_msg}\n"
        siteuri_entries.append(siteuri_block)
        
    with open(tested_path, "a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(tested_entries) + "\n")
        
    with open(agy_path, "a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(agy_entries))
        
    with open(siteuri_path, "a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(siteuri_entries))
        
    print("Registries updated successfully.")

if __name__ == "__main__":
    main()
