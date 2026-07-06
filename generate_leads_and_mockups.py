# -*- coding: utf-8 -*-
import os
import re
import random
import json
import subprocess

LEADS = [
    {
        "niche": "detailing_auto",
        "emoji": "✨",
        "name": "Grig's Auto Detailing",
        "phone": "0765 612 424",
        "location": "Strada Mehadia Nr. 39, Sector 6, București",
        "program": "Luni - Vineri: 09:00 - 18:00 | Sâmbătă: 09:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Cosmetică auto &",
        "slogan_part2": "detailing profesional",
        "desc_niche": "detailing interior și exterior profesional",
        "services": [
            {"icon": "🚗", "name": "Detailing Interior Complet", "desc": "Curățare profundă tapițerie (piele/textil), igienizare cu ozon, curățare plafon, mochetă și plastice."},
            {"icon": "✨", "name": "Polish Exterior & Corecție", "desc": "Eliminare zgârieturi fine, redare luciu intens vopsea și aplicare ceară protectoare de lungă durată."},
            {"icon": "🛡️", "name": "Protecție Ceramică Gtechniq", "desc": "Aplicare strat ceramic profesional pentru protecție maximă împotriva razelor UV, zgârieturilor și murdăriei."}
        ],
        "image_url": "https://images.unsplash.com/photo-1607860108855-64acf2078ed9?auto=format&fit=crop&w=600&q=80",
        "prefix": "detailing_auto_"
    },
    {
        "niche": "detailing_auto",
        "emoji": "🚗",
        "name": "SKR Detailing",
        "phone": "0769 919 936",
        "location": "Bulevardul Theodor Pallady nr. 42, Sector 3, București",
        "program": "Luni - Sâmbătă: 08:30 - 19:00 | Duminică: Închis",
        "slogan_part1": "Protecții ceramice &",
        "slogan_part2": "curățare tapițerii",
        "desc_niche": "detailing auto profesional de interior și exterior",
        "services": [
            {"icon": "🧼", "name": "Igienizare Detaliată Interior", "desc": "Demontare scaune, aspirare umed-uscată cu injecție-extracție, curățare detaliată a grilelor de aerisire."},
            {"icon": "🛡️", "name": "Polish Faruri & Stopuri", "desc": "Recondiționare faruri mătuite, eliminare oxizi și aplicare folie de protecție regenerabilă (PPF)."},
            {"icon": "💎", "name": "Tratament Hidrofob Geamuri", "desc": "Aplicare tratament special pentru respingerea apei și murdăriei pe parbriz, lunetă și geamuri laterale."}
        ],
        "image_url": "https://images.unsplash.com/photo-1520340356584-f9917d1ecc6f?auto=format&fit=crop&w=600&q=80",
        "prefix": "detailing_auto_"
    },
    {
        "niche": "detailing_auto",
        "emoji": "🧼",
        "name": "Detailing Auto Profesional Sector 5",
        "phone": "0733 131 133",
        "location": "Strada Echinoctiului nr. 52, Sector 5, București",
        "program": "Luni - Vineri: 09:00 - 18:00 | Sâmbătă: 09:00 - 15:00 | Duminică: Închis",
        "slogan_part1": "Redă strălucirea",
        "slogan_part2": "mașinii tale",
        "desc_niche": "servicii complete de cosmetică și detailing auto",
        "services": [
            {"icon": "🚗", "name": "Cosmetică Auto Interior", "desc": "Curățare scaune cu spumă activă, hidratare elemente din piele, curățare portbagaj și compartiment roată rezervă."},
            {"icon": "✨", "name": "Detailing Motor & Conservare", "desc": "Spălare sigură a motorului cu aburi sau soluții dielectrice și aplicare dressing de protecție pentru plastice."},
            {"icon": "🔥", "name": "Decontaminare Argilă & Polish", "desc": "Eliminare particule de fier și bitum de pe caroserie urmată de un polish fin pentru luciu intens."}
        ],
        "image_url": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=600&q=80",
        "prefix": "detailing_auto_"
    },
    {
        "niche": "kinetoterapie",
        "emoji": "🪢",
        "name": "Cabinet Kinetoterapie Adriana Șerban",
        "phone": "0723 206 954",
        "location": "Strada Gaetano Donizetti nr. 3, Sector 2, București",
        "program": "Luni - Vineri: 08:00 - 20:00 | Sâmbătă: 09:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Recuperare medicală &",
        "slogan_part2": "kinetoterapie personalizată",
        "desc_niche": "kinetoterapie și fizioterapie la cabinet și domiciliu",
        "services": [
            {"icon": "💪", "name": "Kinetoterapie Adulți & Copii", "desc": "Programe personalizate de exerciții fizice pentru recuperare post-traumatică, post-operatorie sau corectarea posturii."},
            {"icon": "🦴", "name": "Terapie Manuală & Mobilizări", "desc": "Tehnici speciale de manipulare osteo-articulară pentru reducerea durerilor și redobândirea mobilității."},
            {"icon": "🩹", "name": "Kinesiotaping (Benzi Kinesiologice)", "desc": "Aplicare benzi elastice speciale pentru susținerea musculară, drenaj limfatic și reducerea inflamațiilor."}
        ],
        "image_url": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=600&q=80",
        "prefix": "kinetoterapie_"
    },
    {
        "niche": "kinetoterapie",
        "emoji": "🧘",
        "name": "Kineto Med Expert",
        "phone": "0755 162 362",
        "location": "Calea Dudești nr. 188, Sector 3, București",
        "program": "Luni - Vineri: 08:30 - 20:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Fără dureri de spate &",
        "slogan_part2": "mobilitate redobândită",
        "desc_niche": "kinetoterapie, fizioterapie și masaj terapeutic de specialitate",
        "services": [
            {"icon": "🏥", "name": "Recuperare Afecțiuni Coloană", "desc": "Tratamente eficiente pentru hernii de disc, scolioze, cifoze, spondiloze prin tehnici moderne de kinetoterapie."},
            {"icon": "💆", "name": "Masaj Terapeutic & Decontracturant", "desc": "Masaj medical profund pentru relaxarea musculaturii tensionate, îmbunătățirea circulației și eliminarea punctelor trigger."},
            {"icon": "⚡", "name": "Fizioterapie & Electroterapie", "desc": "Proceduri de electroterapie, ultrasunete și laser pentru stimularea vindecării țesuturilor și reducerea durerilor."}
        ],
        "image_url": "https://images.unsplash.com/photo-1519824145371-296894a0daa9?auto=format&fit=crop&w=600&q=80",
        "prefix": "kinetoterapie_"
    },
    {
        "niche": "kinetoterapie",
        "emoji": "🏃",
        "name": "Kinetoterapie Domiciliu București",
        "phone": "0799 476 119",
        "location": "București & Ilfov (Serviciu la Domiciliu)",
        "program": "Luni - Sâmbătă: 08:00 - 21:00 | Duminică: Urgențe",
        "slogan_part1": "Recuperare medicală la",
        "slogan_part2": "tine acasă",
        "desc_niche": "servicii profesionale de kinetoterapie direct la domiciliul pacientului",
        "services": [
            {"icon": "🏠", "name": "Kinetoterapie la Domiciliu", "desc": "Venim cu toate echipamentele necesare direct la tine acasă. Ideal pentru pacienți nedeplasabili sau cu timp limitat."},
            {"icon": "👶", "name": "Gimnastică Medicală Bebeluși", "desc": "Ședințe specializate pentru sugari și copii mici: stimulare motorie, tratament torticolis sau tal valg."},
            {"icon": "👴", "name": "Recuperare Geriatrică", "desc": "Kinetoterapie adaptată vârstei a treia pentru menținerea tonusului muscular, echilibrului și independenței de mișcare."}
        ],
        "image_url": "https://images.unsplash.com/photo-1581071805260-c4e97669d67b?auto=format&fit=crop&w=600&q=80",
        "prefix": "kinetoterapie_"
    },
    {
        "niche": "foraje_puturi",
        "emoji": "🚰",
        "name": "Petcu Foraje Puțuri",
        "phone": "0721 863 715",
        "location": "Calea Giulești nr. 310, Sector 6, București",
        "program": "Luni - Duminică: 08:00 - 20:00 (Non-Stop Urgențe)",
        "slogan_part1": "Apă curată &",
        "slogan_part2": "foraje de mare adâncime",
        "desc_niche": "foraje puțuri de apă, denisipări și piloni de consolidare",
        "services": [
            {"icon": "💧", "name": "Foraje Puțuri Apă", "desc": "Executăm foraje la mică, medie și mare adâncime cu tubulatură PVC ecologică și filtre profesionale."},
            {"icon": "🧼", "name": "Denisipări & Curățări Puțuri", "desc": "Îndepărtarea nisipului depus, spălarea filtrelor și tratarea apei cu substanțe speciale pentru recăpătarea debitului."},
            {"icon": "🏗️", "name": "Piloni Consolidare & Foraje Micropiloni", "desc": "Foraje speciale pentru piloni de susținere, fundații și consolidări terenuri pentru construcții rezidențiale."}
        ],
        "image_url": "https://images.unsplash.com/photo-1618220179428-22790b461013?auto=format&fit=crop&w=600&q=80",
        "prefix": "foraje_puturi_"
    },
    {
        "niche": "foraje_puturi",
        "emoji": "⛲",
        "name": "Doru Foraje Puțuri",
        "phone": "0745 405 391",
        "location": "Strada Principală nr. 145, Tunari, Ilfov",
        "program": "Luni - Sâmbătă: 08:00 - 18:00 | Duminică: Închis",
        "slogan_part1": "Foraje puțuri profesionale",
        "slogan_part2": "la prețuri corecte",
        "desc_niche": "servicii profesionale de foraj puțuri și sisteme de alimentare cu apă",
        "services": [
            {"icon": "🔧", "name": "Foraje Absorbante & Drenaje", "desc": "Realizare puțuri absorbante pentru captarea apelor pluviale sau drenarea eficientă a curților și terenurilor."},
            {"icon": "💧", "name": "Denisipări Profesionale", "desc": "Curățarea puțurilor prin sistem airlift de înaltă presiune pentru eliminarea nisipului și limpezirea apei."},
            {"icon": "🛠️", "name": "Montaj Pompe & Hidrofoare", "desc": "Echiparea puțului cu pompe submersibile de calitate, tablouri de automatizare, vase de expansiune și filtre."}
        ],
        "image_url": "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?auto=format&fit=crop&w=600&q=80",
        "prefix": "foraje_puturi_"
    },
    {
        "niche": "foraje_puturi",
        "emoji": "🌀",
        "name": "Florin Nedelcu - Foraje & Reabilitări",
        "phone": "0761 929 742",
        "location": "Șoseaua Cernica nr. 82, Pantelimon, Ilfov",
        "program": "Luni - Duminică: 07:30 - 21:00",
        "slogan_part1": "Reabilitări puțuri &",
        "slogan_part2": "denisipări rapide",
        "desc_niche": "servicii complete de foraje, denisipări și întreținere puțuri de apă",
        "services": [
            {"icon": "🧼", "name": "Denisipare Rapidă (Airlift)", "desc": "Curățare ecologică a puțului prin barbotare cu aer comprimat pentru eliminarea depunerilor de nisip și nămol."},
            {"icon": "🔬", "name": "Tratare & Dezinfectare Apă", "desc": "Pielografiere puț și tratament chimic de șoc cu substanțe avizate pentru sterilizarea bacteriologică a forajului."},
            {"icon": "💧", "name": "Foraje Diametru Mic/Mediu", "desc": "Foraje rapide pentru alimentarea caselor de vacanță, grădinilor sau pentru pompe de căldură geotermale."}
        ],
        "image_url": "https://images.unsplash.com/photo-1581094288338-2314dddb7ecc?auto=format&fit=crop&w=600&q=80",
        "prefix": "foraje_puturi_"
    },
    {
        "niche": "reparatii_termopane",
        "emoji": "🪟",
        "name": "TermoFix București",
        "phone": "0722 839 999",
        "location": "Șoseaua Olteniței nr. 104, Sector 4, București",
        "program": "Luni - Duminică: Non-Stop (Urgențe Reparații)",
        "slogan_part1": "Reparații termopane &",
        "slogan_part2": "reglaje ferestre non-stop",
        "desc_niche": "servicii de reparații termopane, reglaje ferestre și înlocuire accesorii",
        "services": [
            {"icon": "🔧", "name": "Reglaje & Mentenanță Feronerie", "desc": "Ungere, calibrare și reglare feronerie pentru ferestre și uși care se închid greu sau lasă aerul să treacă."},
            {"icon": "🪟", "name": "Înlocuire Geamuri Sparte", "desc": "Măsurare și înlocuire rapidă pentru sticle termopan sparte, fisurate sau aburite la interior (condens)."},
            {"icon": "🛡️", "name": "Garnituri Ultra-Izolante", "desc": "Schimbarea garniturilor uzate din cauciuc cu modele premium EPDM pentru izolație termică și fonică maximă."}
        ],
        "image_url": "https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=600&q=80",
        "prefix": "reparatii_termopane_"
    },
    {
        "niche": "reparatii_termopane",
        "emoji": "🛠️",
        "name": "Marian - Service Termopane PVC",
        "phone": "0741 052 758",
        "location": "Strada Baba Novac nr. 16, Sector 3, București",
        "program": "Luni - Sâmbătă: 08:00 - 19:00 | Duminică: Închis",
        "slogan_part1": "Modificări termopane &",
        "slogan_part2": "plase anti-insecte",
        "desc_niche": "reparații, reglaje termopane și execuție plase țânțari la comandă",
        "services": [
            {"icon": "🦟", "name": "Plase Țânțari & Insecte", "desc": "Executăm și montăm plase de insecte pe balamale, tip rulou sau plise, pe profile de aluminiu rezistente."},
            {"icon": "🔄", "name": "Modificări Deschideri (Oscilobatant)", "desc": "Transformăm ferestre simple cu deschidere normală în deschideri oscilobatante (cu rabatare de sus)."},
            {"icon": "🔐", "name": "Sisteme Siguranță & Mânere", "desc": "Montaj mânere cu cheie pentru protecția copiilor, blocatoare suplimentare și închizători uși balcon."}
        ],
        "image_url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=600&q=80",
        "prefix": "reparatii_termopane_"
    },
    {
        "niche": "reparatii_termopane",
        "emoji": "🚪",
        "name": "Reparații Termopane Dristor",
        "phone": "0722 408 934",
        "location": "Strada Dristorului nr. 10, Sector 3, București",
        "program": "Luni - Sâmbătă: 08:30 - 18:30 | Duminică: Urgențe",
        "slogan_part1": "Reparații uși balcon &",
        "slogan_part2": "reglaje termopane rapide",
        "desc_niche": "servicii de reparații termopane, ferestre PVC/Aluminiu și uși de balcon",
        "services": [
            {"icon": "🚪", "name": "Reparații Uși de Balcon", "desc": "Reglaje balamale uși grele de balcon, înlocuire broaște, amortizoare, balamale rupte sau mânere defecte."},
            {"icon": "🔧", "name": "Înlocuire Feronerie Completă", "desc": "Schimbăm mecanisme de închidere multipunct uzate sau blocate (Maco, Roto, Vorne, G-U)."},
            {"icon": "📐", "name": "Calibrare Geam prin Cale", "desc": "Demontarea baghetelor și repoziționarea calelor de sticlă pentru ridicarea colțurilor ferestrelor lăsate."}
        ],
        "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80",
        "prefix": "reparatii_termopane_"
    },
    {
        "niche": "service_gsm",
        "emoji": "📱",
        "name": "Glass Repair Service GSM",
        "phone": "0765 325 325",
        "location": "Calea Văcărești nr. 220, Sector 4, București",
        "program": "Luni - Vineri: 10:00 - 19:00 | Sâmbătă: 10:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Schimbare sticlă ecran &",
        "slogan_part2": "reparații telefoane pe loc",
        "desc_niche": "service gsm specializat în înlocuire sticlă ecran și reparații hardware telefoane",
        "services": [
            {"icon": "📱", "name": "Înlocuire Sticlă Ecran OCA", "desc": "Schimbăm doar sticla spartă a ecranului prin laminare industrială OCA, păstrând display-ul original al telefonului."},
            {"icon": "🔋", "name": "Înlocuire Baterii & Port Încărcare", "desc": "Schimbăm acumulatori uzați care se descarcă rapid și porturi de încărcare USB-C sau Lightning defecte."},
            {"icon": "💧", "name": "Reparații Telefoane Udate", "desc": "Curățare profesională în baie ultrasunete pentru eliminarea oxizilor și reparații circuite afectate de lichide."}
        ],
        "image_url": "https://images.unsplash.com/photo-1597740985671-2a8a3b80f01e?auto=format&fit=crop&w=600&q=80",
        "prefix": "service_gsm_"
    },
    {
        "niche": "service_gsm",
        "emoji": "🔌",
        "name": "BITS Service GSM & IT",
        "phone": "0728 943 333",
        "location": "Strada Apusului nr. 81, Sector 6, București",
        "program": "Luni - Vineri: 09:00 - 18:30 | Sâmbătă: 09:30 - 14:00 | Duminică: Închis",
        "slogan_part1": "Reparații telefoane &",
        "slogan_part2": "laptopuri în Militari",
        "desc_niche": "service gsm și reparații calculatoare/laptopuri hardware și software",
        "services": [
            {"icon": "📱", "name": "Înlocuire Ecrane & Carcases", "desc": "Montaj display-uri originale sau compatibile pentru iPhone, Samsung, Huawei, Xiaomi și înlocuire capace spate."},
            {"icon": "💻", "name": "Service Laptop & PC", "desc": "Curățare praf, înlocuire pastă termică, upgrade SSD/RAM, reinstalare Windows și devirusări rapide."},
            {"icon": "💾", "name": "Recuperare Date & Decodări", "desc": "Recuperăm date de pe dispozitive blocate sau defecte și oferim decodări de rețea autorizate."}
        ],
        "image_url": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=600&q=80",
        "prefix": "service_gsm_"
    },
    {
        "niche": "service_gsm",
        "emoji": "📲",
        "name": "GSM Express Vitan",
        "phone": "0799 288 535",
        "location": "Calea Vitan nr. 12, Sector 3, București",
        "program": "Luni - Sâmbătă: 09:00 - 20:00 | Duminică: Închis",
        "slogan_part1": "Reparații rapide telefoane",
        "slogan_part2": "la prețuri avantajoase",
        "desc_niche": "service gsm rapid pentru orice model de telefon sau tabletă",
        "services": [
            {"icon": "⚡", "name": "Reparații Express pe Loc", "desc": "Înlocuire ecran, baterie, microfon sau cască audio în maxim 30-60 de minute pentru modelele uzuale în stoc."},
            {"icon": "🔬", "name": "Reparații Plăci de Bază", "desc": "Micro-lipituri pe placa de bază, înlocuire controllere de încărcare (U2), reparații cip audio și touchscreen."},
            {"icon": "🛡️", "name": "Accesorii & Folii Protecție", "desc": "Debitare și montaj folii de protecție din silicon regenerabil (TPU) și comercializare încărcătoare originale."}
        ],
        "image_url": "https://images.unsplash.com/photo-1581092921461-eab62e97a780?auto=format&fit=crop&w=600&q=80",
        "prefix": "service_gsm_"
    },
    {
        "niche": "servicii_funerare",
        "emoji": "🕯️",
        "name": "Servicii Funerare Baidoc",
        "phone": "0766 402 060",
        "location": "Șoseaua Giurgiului nr. 110, Sector 5, București",
        "program": "Luni - Duminică: Non-Stop (24/7)",
        "slogan_part1": "Servicii funerare non-stop",
        "slogan_part2": "cu respect și decență",
        "desc_niche": "servicii funerare complete non-stop în București și Ilfov",
        "services": [
            {"icon": "🕯️", "name": "Servicii Funerare Complete", "desc": "Pregătire defunct, îmbălsămare autorizată, toaletare, sicrie complet echipate din diverse esențe de lemn."},
            {"icon": "🚚", "name": "Transport Funerar Autorizat", "desc": "Transport mortuar intern cu autospeciale funerare omologate și repatrieri decedați din Europa în condiții sigure."},
            {"icon": "📜", "name": "Acte & Dosar Ajutor Înmormântare", "desc": "Întocmirea rapidă a actelor (certificat deces, adeverință înhumare) și decontare prin ajutorul de înmormântare CNPP."}
        ],
        "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=600&q=80",
        "prefix": "servicii_funerare_"
    },
    {
        "niche": "servicii_funerare",
        "emoji": "🌹",
        "name": "Anima Funerare București",
        "phone": "0722 274 177",
        "location": "Strada Lizeanu nr. 18, Sector 2, București",
        "program": "Luni - Duminică: Non-Stop (24/7)",
        "slogan_part1": "Servicii funerare de încredere",
        "slogan_part2": "în momente dificile",
        "desc_niche": "pompe funebre complete, repatrieri și aranjamente funerare non-stop",
        "services": [
            {"icon": "🌹", "name": "Pachete Funerare Personalizate", "desc": "Oferim pachete adaptate bugetului dumneavoastră, inclusiv pachete speciale pentru pensionari decontate 100%."},
            {"icon": "🥖", "name": "Organizare Colivă & Parastase", "desc": "Pregătire pachete de pomană, colivă, colaci, catering pentru parastase și închiriere capelă funerară."},
            {"icon": "🌸", "name": "Coroane & Aranjamente Florale", "desc": "Realizare coroane, jerbe și aranjamente din flori naturale (garoafe, trandafiri, crini) cu mesaje funerare personalizate."}
        ],
        "image_url": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?auto=format&fit=crop&w=600&q=80",
        "prefix": "servicii_funerare_"
    },
    {
        "niche": "mobila_la_comanda",
        "emoji": "🪵",
        "name": "Atelier Mobilă Lemn Masiv",
        "phone": "0783 202 247",
        "location": "Strada Horei nr. 12, Sector 2, București",
        "program": "Luni - Sâmbătă: 08:00 - 18:00 | Duminică: Închis",
        "slogan_part1": "Mobilier din lemn masiv",
        "slogan_part2": "la comandă în București",
        "desc_niche": "atelier de tâmplărie specializat în mobilier din lemn masiv și MDF vopsit",
        "services": [
            {"icon": "🪵", "name": "Mobilier Lemn Masiv Custom", "desc": "Mese din lemn masiv (stejar, nuc), paturi, dulapuri, biblioteci și uși de interior executate la dimensiunile dorite."},
            {"icon": "📐", "name": "Măsurători & Proiectare 3D", "desc": "Deplasare la domiciliu pentru măsurători exacte și realizarea schiței de proiectare 3D a mobilierului."},
            {"icon": "🎨", "name": "Recondiționare Mobilă Veche", "desc": "Restaurare mobilier de epocă, șlefuire, aplicare baiț, lacuri ecologice și refacere elemente din lemn deteriorate."}
        ],
        "image_url": "https://images.unsplash.com/photo-1538688525198-9b88f6f53126?auto=format&fit=crop&w=600&q=80",
        "prefix": "mobila_la_comanda_"
    },
    {
        "niche": "mobila_la_comanda",
        "emoji": "📐",
        "name": "Mobilier Custom Bragadiru",
        "phone": "0765 212 100",
        "location": "Strada Principală nr. 88, Bragadiru, Ilfov",
        "program": "Luni - Sâmbătă: 08:30 - 19:00 | Duminică: Închis",
        "slogan_part1": "Bucătării & dressinguri",
        "slogan_part2": "la comandă din PAL și MDF",
        "desc_niche": "producător de mobilier la comandă din PAL melaminat și MDF înfoliat/vopsit",
        "services": [
            {"icon": "🍳", "name": "Mobilier de Bucătărie Custom", "desc": "Bucătării moderne cu feronerie Blum (închideri amortizate), blat termorezistent, spații integrate electrocasnice."},
            {"icon": "👗", "name": "Dressinguri & Dulapuri Glisante", "desc": "Dulapuri spațioase cu uși glisante, compartimentare optimizată cu sertare, umerașe lift și organizatoare."},
            {"icon": "🛋️", "name": "Mobilier Living & Dormitoare", "desc": "Comode TV suspendate, noptiere, paturi tapițate și mobilier complet pentru camere de copii."}
        ],
        "image_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=600&q=80",
        "prefix": "mobila_la_comanda_"
    },
    {
        "niche": "curatare_canapele",
        "emoji": "🛋️",
        "name": "Eco Clean Canapele",
        "phone": "0733 125 125",
        "location": "Bulevardul Camil Ressu nr. 45, Sector 3, București",
        "program": "Luni - Duminică: 08:00 - 21:00",
        "slogan_part1": "Curățare canapele & saltele",
        "slogan_part2": "la domiciliu în București",
        "desc_niche": "servicii profesionale de curățare canapele, fotolii și saltele la domiciliu",
        "services": [
            {"icon": "🛋️", "name": "Curățare Canapele & Colțare", "desc": "Spălare prin injecție-extracție cu detergenți ecologici pentru eliminarea petelor dificile, acarienilor și mirosurilor."},
            {"icon": "🛏️", "name": "Igienizare Saltele Domiciliu", "desc": "Curățare profundă saltele de pat, eliminare bacterii, transpirație și pete de urină cu echipamente Karcher."},
            {"icon": "🚗", "name": "Spălare Tapițerii Auto & Scaune", "desc": "Curățare completă scaune auto textile, mochete, portbagaj și igienizare sistem climatizare cu aburi."}
        ],
        "image_url": "https://images.unsplash.com/photo-1540518614846-7eded433c457?auto=format&fit=crop&w=600&q=80",
        "prefix": "curatare_canapele_"
    }
]

PALETTES = {
    "detailing_auto": {
        "primary": "#fbbf24",
        "rgb": "251, 191, 36",
        "secondary": "#0f172a",
        "bg": "#1e293b",
        "tag": "Servicii Detailing Premium"
    },
    "kinetoterapie": {
        "primary": "#0d9488",
        "rgb": "13, 148, 136",
        "secondary": "#1e1b4b",
        "bg": "#f0fdfa",
        "tag": "Cabinet Recuperare Medicală"
    },
    "foraje_puturi": {
        "primary": "#0284c7",
        "rgb": "2, 132, 199",
        "secondary": "#0f172a",
        "bg": "#f0f9ff",
        "tag": "Servicii Foraje Profesionale"
    },
    "reparatii_termopane": {
        "primary": "#06b6d4",
        "rgb": "6, 182, 212",
        "secondary": "#1e293b",
        "bg": "#ecfeff",
        "tag": "Reparații & Reglaje Termopane"
    },
    "service_gsm": {
        "primary": "#ea580c",
        "rgb": "234, 88, 12",
        "secondary": "#111827",
        "bg": "#fbfaf9",
        "tag": "Service GSM Rapid"
    },
    "servicii_funerare": {
        "primary": "#ca8a04",
        "rgb": "202, 138, 4",
        "secondary": "#18181b",
        "bg": "#f4f4f5",
        "tag": "Servicii Funerare Non-Stop"
    },
    "mobila_la_comanda": {
        "primary": "#d97706",
        "rgb": "217, 119, 6",
        "secondary": "#27272a",
        "bg": "#faf7f5",
        "tag": "Mobilier la Comandă"
    },
    "curatare_canapele": {
        "primary": "#10b981",
        "rgb": "16, 185, 129",
        "secondary": "#0f172a",
        "bg": "#ecfdf5",
        "tag": "Curățenie & Igienizare Domiciliu"
    }
}

REVIEWS_TEMPLATES = {
    "detailing_auto": [
        "Am adus mașina pentru un detailing interior și exterior complet plus protecție ceramică. Rezultatul a fost peste așteptări! Mașina arată mai bine decât când a ieșit din fabrică.",
        "Curățare excepțională a tapițeriei! Au scos pete vechi de cafea și suc pe care credeam că nu le mai pot curăța niciodată. Foarte serioși și rapizi.",
        "Polish profesional de nota 10. Au eliminat toate zgârieturile fine de pe caroserie și vopseaua și-a recăpătat strălucirea de altădată. Recomand Grig's Auto Detailing!",
        "Recomand cu încredere. Atenție incredibilă la detalii, au curățat până și cele mai greu accesibile zone din mașină. Raport calitate-preț excelent."
    ],
    "kinetoterapie": [
        "Am urmat un program de recuperare după o operație de menisc. Kinetoterapeutul a fost extrem de răbdător și profesionist, iar recuperarea a fost un succes rapid.",
        "Ședințele de kinetoterapie pentru durerile lombare au făcut minuni. După doar 5 ședințe mă pot mișca liber și durerile au dispărut complet.",
        "Recomand cu toată încrederea! Profesioniști, atenți la detalii și foarte bine pregătiți. Cabinet curat și atmosferă relaxantă.",
        "Terapie manuală excelentă. Durerile de ceafă și spate cauzate de lucrul la birou s-au ameliorat considerabil chiar de la prima ședință."
    ],
    "foraje_puturi": [
        "Echipa a forat un puț la 35 de metri adâncime în curtea mea. Debitul este excelent, iar apa este foarte curată. Au lucrat rapid și curat. Recomand!",
        "Denisiparea puțului vechi a fost realizată cu succes. Au readus debitul inițial de apă și au curățat perfect instalația. Servicii serioase la preț bun.",
        "Profesioniști în foraje puțuri. Ne-au recomandat soluția optimă pentru solul nostru și au terminat lucrarea în timpul promis, fără costuri ascunse.",
        "Recomand cu căldură. Au sosit cu utilaje moderne și au realizat forajul rapid și profesionist, lăsând curtea curată în urma lor."
    ],
    "reparatii_termopane": [
        "Ferestrele mele nu se mai închideau bine și lăsau curent. După reglajele făcute și înlocuirea garniturilor uzate, în casă este cald și liniște. Mulțumesc!",
        "Mi s-a spart sticla la o ușă de balcon. Au venit în aceeași zi, au luat măsurile și a doua zi geamul nou a fost montat. Rapid, curat și eficient.",
        "Service de reparații termopane excelent. Au transformat o fereastră simplă în oscilobatantă foarte rapid. Meseriaș politicos și prețuri corecte.",
        "Foarte mulțumit de reparațiile efectuate la ușile de PVC. Reglaj perfect, acum se închid cu un singur deget. Recomand cu încredere!"
    ],
    "service_gsm": [
        "Mi-am schimbat sticla la ecranul telefonului pe loc. Display-ul a rămas cel original și costul a fost mult mai mic decât înlocuirea completă a ecranului. Servicii impecabile!",
        "Baterie nouă la telefon schimbată în 20 de minute. Telefonul funcționează ca nou și nu se mai descarcă repede. Tehnicieni profesioniști și amabili.",
        "Service gsm excelent în București. Au reparat telefonul udat rapid, curățându-l în baie ultrasunete. Foarte serioși și transparenți.",
        "Punctualitate și reparații rapide. Recomand cu încredere BITS pentru orice problemă hardware sau software la telefoane sau laptopuri."
    ],
    "servicii_funerare": [
        "În momentele extrem de grele ale decesului tatălui meu, echipa a oferit sprijin total și servicii funerare complete cu mult respect și profesionalism. Vă mulțumim din suflet.",
        "Consiliere excelentă și organizare impecabilă a întregului proces. S-au ocupat de toate actele de deces și decontarea ajutorului de înmormântare CNPP rapid.",
        "Transport funerar realizat în siguranță și condiții de maxim respect. Pachetul funerar ales a fost corect ca preț și complet utilat. Recomand agentia.",
        "Recomand Servicii Funerare Baidoc pentru seriozitate, decență și atenție în organizarea pomenilor și parastaselor în momente dificile."
    ],
    "mobila_la_comanda": [
        "Am comandat mobilierul de bucătărie din MDF vopsit și rezultatul este spectaculos. Finisaje premium, feronerie rezistentă și montaj curat. Recomand!",
        "Masa de stejar masiv comandată la ei este piesa de rezistență din living. Lemn prelucrat superb și finisaj de înaltă clasă. Tâmplari adevărați.",
        "Bucătărie proiectată 3D și executată perfect. Toate electrocasnicele încorporabile s-au potrivit la milimetru. Foarte serioși și atenți la măsurători.",
        "Dressing spațios cu uși glisante realizat exact după dorințele noastre. Calitate foarte bună a materialelor și montaj rapid. Mulțumim!"
    ],
    "curatare_canapele": [
        "Canapeaua noastră de colț arată din nou ca nouă! Detergenții folosiți au scos toate petele făcute de copii și au eliminat mirosul de animal de companie. Recomand!",
        "Spălare saltea la domiciliu realizată extrem de profesional. Echipamente puternice care au extras toată murdăria și au uscat rapid salteaua.",
        "Profesioniști în curățarea tapițeriilor auto și canapelelor. Au venit la ora stabilită și au lucrat curat, cu atenție la detalii. Preț excelent.",
        "Eco Clean a făcut o treabă minunată cu fotoliile și mocheta din living. Recomand pentru promptitudine, eficiență și amabilitate."
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
    
    niche_templates = REVIEWS_TEMPLATES.get(niche, REVIEWS_TEMPLATES["curatare_canapele"])
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
        num = 421 + idx
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
        html_content = html_content.replace("__DESC__", f"Servicii de {item['desc_niche']} în {item['location']}. Intervenim rapid și oferim garanție completă pentru toate lucrările executate.")
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
