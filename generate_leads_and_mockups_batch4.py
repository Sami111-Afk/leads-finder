# -*- coding: utf-8 -*-
import os
import re
import random
import json
import subprocess

LEADS = [
    {
        "niche": "servicii_mutari",
        "emoji": "🚚",
        "name": "Moving Express București",
        "phone": "0722 888 444",
        "location": "Bulevardul Timișoara nr. 26, Sector 6, București",
        "program": "Luni - Duminică: 07:00 - 22:00 (Non-Stop Urgențe)",
        "slogan_part1": "Servicii mutări & transport",
        "slogan_part2": "mobilă în siguranță deplină",
        "desc_niche": "servicii profesionale de mutări, relocări și transport marfă",
        "services": [
            {"icon": "📦", "name": "Mutări Apartamente & Case", "desc": "Asigurăm servicii complete de mutare: demontare/montare mobilier, împachetare în folie cu bule și cutii rezistente, manipulare și așezare pe poziție."},
            {"icon": "🏢", "name": "Relocări Sedii Firme", "desc": "Mutări rapide de birouri, arhive, calculatoare și echipamente de birotică, programate inclusiv în weekend pentru a nu perturba activitatea."},
            {"icon": "🚛", "name": "Transport Marfă & Taxi Marfă", "desc": "Transport rutier de mobilier, electrocasnice sau bagaje cu autoutilitare de 3.5 tone curate și echipate cu chingi de ancorare."}
        ],
        "image_url": "https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=600&q=80",
        "prefix": "servicii_mutari_"
    },
    {
        "niche": "servicii_mutari",
        "emoji": "📦",
        "name": "Transport Marfă & Mutări Rapid Andrei",
        "phone": "0764 111 555",
        "location": "Strada Valea Oltului nr. 56, Sector 6, București",
        "program": "Luni - Duminică: 08:00 - 20:00",
        "slogan_part1": "Transport marfă ieftin &",
        "slogan_part2": "băieți pentru manipulare",
        "desc_niche": "transport marfă, relocări și manipulare mobilier",
        "services": [
            {"icon": "🚛", "name": "Transport Marfă Rapid", "desc": "Curse rapide de transport în București și Ilfov pentru materiale de construcții, mobilier nou de la magazin sau electrocasnice."},
            {"icon": "💪", "name": "Manipulare Mobilier Grea", "desc": "Echipați cu echipamente speciale pentru manipularea obiectelor grele (pianine, seifuri, frigidere industriale) pe scări sau lift."},
            {"icon": "🗑️", "name": "Evacuare Mobilă Veche", "desc": "Demontare și evacuare mobilier vechi, electrocasnice nefuncționale sau moloz la saci și transportul lor la groapa de gunoi."}
        ],
        "image_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=600&q=80",
        "prefix": "servicii_mutari_"
    },
    {
        "niche": "servicii_mutari",
        "emoji": "🚚",
        "name": "Mutări Relocări București Marius",
        "phone": "0733 222 333",
        "location": "Strada Avrig nr. 12, Sector 2, București",
        "program": "Luni - Sâmbătă: 08:00 - 20:00 | Duminică: Închis",
        "slogan_part1": "Relocări naționale &",
        "slogan_part2": "depozitare mobilă temporară",
        "desc_niche": "relocări naționale, depozitare și servicii de mutări",
        "services": [
            {"icon": "🗺️", "name": "Mutări Interjudețene", "desc": "Mutări din București către orice oraș din România cu autoutilitare moderne și șoferi cu experiență pe trasee lungi."},
            {"icon": "🔑", "name": "Depozitare Boxe/Storage", "desc": "Oferim spații de depozitare sigure, uscate și păzite pentru depozitarea temporară a mobilei pe durata renovărilor."},
            {"icon": "📦", "name": "Livrare Ambalaje Mutare", "desc": "Livrăm din timp cutii de carton de diverse dimensiuni, folie stretch, bandă adezivă și hârtie pentru împachetat porțelanuri."}
        ],
        "image_url": "https://images.unsplash.com/photo-1512756290469-ec0629b1cc7e?auto=format&fit=crop&w=600&q=80",
        "prefix": "servicii_mutari_"
    },
    {
        "niche": "servicii_mutari",
        "emoji": "🚛",
        "name": "Taxi Marfă București Gabi",
        "phone": "0765 333 444",
        "location": "Șoseaua Olteniței nr. 102, Sector 4, București",
        "program": "Luni - Duminică: 07:30 - 21:30",
        "slogan_part1": "Taxi marfă rapid &",
        "slogan_part2": "mutări mobilier electrocasnice",
        "desc_niche": "taxi marfă rapid și servicii de mutări de mici dimensiuni",
        "services": [
            {"icon": "⚡", "name": "Taxi Marfă Non-Stop", "desc": "Servicii de transport rapid pentru 1-2 piese de mobilier sau electrocasnice cumpărate din magazine (IKEA, Dedeman, Leroy)."},
            {"icon": "📦", "name": "Mutări Garsoniere Rapid", "desc": "Pachete optimizate pentru mutarea rapidă a garsonierelor, incluzând duba și 2 manipulatori la un preț fix avantajos."},
            {"icon": "🛡️", "name": "Asigurare Marfă inclusă", "desc": "Toate transporturile noastre beneficiază de asigurare CMR pentru ca bunurile dumneavoastră să fie protejate pe tot parcursul drumului."}
        ],
        "image_url": "https://images.unsplash.com/photo-1549058917-0c6a85060999?auto=format&fit=crop&w=600&q=80",
        "prefix": "servicii_mutari_"
    },
    {
        "niche": "cardiologie",
        "emoji": "❤️",
        "name": "Cabinet Cardiologie Dr. Adrian Popescu",
        "phone": "0723 555 777",
        "location": "Strada Viitorului nr. 142, Sector 2, București",
        "program": "Luni - Vineri: 09:00 - 19:00 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Consultații cardiologie &",
        "slogan_part2": "ecografii cardiace Doppler",
        "desc_niche": "consultații cardiologie, ecografie cardiacă și monitorizare Holter",
        "services": [
            {"icon": "❤️", "name": "Consultații Cardiologie", "desc": "Evaluare clinică, diagnosticare și tratament pentru hipertensiune arterială, cardiopatie ischemică, aritmii sau insuficiență cardiacă."},
            {"icon": "📟", "name": "Ecografie Cardiacă Doppler", "desc": "Investigație ecografică non-invazivă pentru vizualizarea structurii inimii, valvelor și măsurarea fluxurilor de sânge."},
            {"icon": "📊", "name": "Monitorizare Holter EKG/TA", "desc": "Montare dispozitive Holter pentru monitorizarea activității electrice a inimii (EKG) sau a tensiunii arteriale pe 24/48 de ore."}
        ],
        "image_url": "https://images.unsplash.com/photo-1579684389782-64d84b5e901d?auto=format&fit=crop&w=600&q=80",
        "prefix": "cardiologie_"
    },
    {
        "niche": "cardiologie",
        "emoji": "⚕️",
        "name": "Clinica Cardiologie Dr. Elena Georgescu",
        "phone": "0744 666 888",
        "location": "Bulevardul Primăverii nr. 12, Sector 1, București",
        "program": "Luni - Vineri: 09:00 - 19:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Prevenție & diagnostic",
        "slogan_part2": "cardiovascular de înaltă precizie",
        "desc_niche": "cardiologie clinică, ecografie cardiacă și teste de efort",
        "services": [
            {"icon": "🏃", "name": "Test de Efort EKG", "desc": "Evaluarea funcționării inimii în timpul efortului fizic controlat pe banda de alergat sau bicicleta ergometrică."},
            {"icon": "🔬", "name": "Profil Lipidoric & Analize", "desc": "Recomandare și interpretare analize specifice: colesterol, trigliceride, markeri cardiaci și stabilire tratamente preventive."},
            {"icon": "❤️", "name": "Evaluare Risc Cardiovascular", "desc": "Calcularea scorului de risc pentru infarct miocardic sau accident vascular și ghidaj nutrițional adaptat inimii."}
        ],
        "image_url": "https://images.unsplash.com/photo-1530026405186-ed1ea0ac7a63?auto=format&fit=crop&w=600&q=80",
        "prefix": "cardiologie_"
    },
    {
        "niche": "cardiologie",
        "emoji": "🩺",
        "name": "Cabinet Cardiologie Dr. Mihai Radu",
        "phone": "0722 888 555",
        "location": "Calea Dudești nr. 188, Sector 3, București",
        "program": "Luni - Vineri: 08:30 - 20:00 | Sâmbătă: 09:00 - 13:00 | Duminică: Închis",
        "slogan_part1": "Consultații cardiace &",
        "slogan_part2": "ecografii cardiace rapide",
        "desc_niche": "cabinet medical de cardiologie, ecografii de rutină și EKG",
        "services": [
            {"icon": "📟", "name": "Ecografie Doppler Vasculară", "desc": "Evaluarea arterelor și venelor de la picioare sau gât (carotidiană) pentru depistarea depunerilor de calciu sau trombozelor."},
            {"icon": "📉", "name": "Electrocardiogramă (EKG) 12 Canale", "desc": "Înregistrarea rapidă a activității electrice a inimii pentru depistarea modificărilor de ritm sau semnelor de infarct."},
            {"icon": "💊", "name": "Tratamente Hipertensiune", "desc": "Diagnosticarea cauzelor hipertensiunii și optimizarea tratamentului medicamentos pentru controlul valorilor tensionale."}
        ],
        "image_url": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&w=600&q=80",
        "prefix": "cardiologie_"
    },
    {
        "niche": "cardiologie",
        "emoji": "❤️",
        "name": "Consult Cardiologic Dr. Stancu",
        "phone": "0761 222 444",
        "location": "Șoseaua Olteniței nr. 35, Sector 4, București",
        "program": "Luni - Vineri: 09:00 - 18:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Sănătatea inimii tale",
        "slogan_part2": "asigurată de medici primari",
        "desc_niche": "cardiologie clinică, diagnostic imagistic și consultații preventive",
        "services": [
            {"icon": "❤️", "name": "Control Cardiologic Anual", "desc": "Control de rutină esențial pentru persoanele de peste 40 de ani, fumători sau cu antecedente în familie."},
            {"icon": "📋", "name": "Avize Medicale Cardiologie", "desc": "Eliberare referate medicale sau avize cardiologice pentru intervenții chirurgicale, angajări sau permise auto."},
            {"icon": "💊", "name": "Tratament Angină Pectorală", "desc": "Evaluarea durerilor în piept de natură cardiacă, stabilire tratament și monitorizare periodică."}
        ],
        "image_url": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=600&q=80",
        "prefix": "cardiologie_"
    },
    {
        "niche": "podologie",
        "emoji": "👣",
        "name": "Cabinet Podologie Dr. Roxana Popa",
        "phone": "0723 999 111",
        "location": "Strada Horei nr. 12, Sector 2, București",
        "program": "Luni - Vineri: 09:00 - 20:00 | Sâmbătă: 09:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Pedichiură medicală &",
        "slogan_part2": "tratamente podologie profesionale",
        "desc_niche": "podologie, pedichiură medicală și tratamente unghii încarnate/bătături",
        "services": [
            {"icon": "👣", "name": "Pedichiură Medicală Completă", "desc": "Tratamente specifice pentru unghii îngroșate, micoze (onicomicoză), bătături dureroase (clavus) și călcâie crăpate."},
            {"icon": "🩹", "name": "Tratament Unghii Încarnate", "desc": "Corectarea creșterii unghiei prin sisteme speciale non-invazive de sârmulițe (ortonexie) sau rezecție parțială fără durere."},
            {"icon": "🦶", "name": "Tratamente Veruci Plantare", "desc": "Îndepărtarea verucilor (negi în talpă) prin proceduri sigure de crioterapie sau tratamente topice de specialitate."}
        ],
        "image_url": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=600&q=80",
        "prefix": "podologie_"
    },
    {
        "niche": "podologie",
        "emoji": "👣",
        "name": "Podologie Medicală București Alina",
        "phone": "0744 888 222",
        "location": "Calea Dorobanți nr. 104, Sector 1, București",
        "program": "Luni - Vineri: 09:00 - 19:00 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Picioare sănătoase &",
        "slogan_part2": "pedichiură terapeutică premium",
        "desc_niche": "podiatrie, pedichiură terapeutică și tratament picior diabetic",
        "services": [
            {"icon": "🩺", "name": "Tratament Picior Diabetic", "desc": "Îngrijire preventivă și curățare specială a picioarelor pentru pacienții cu diabet, prevenind apariția ulcerelor."},
            {"icon": "👣", "name": "Curățare Ciupercă Unghie", "desc": "Tratarea unghiilor afectate de ciupercă prin curățare mecanică detaliată și aplicare de tratamente topice antifungice."},
            {"icon": "👟", "name": "Orteze Personalizate Silicon", "desc": "Realizare orteze din silicon medical pentru protecția monturilor sau corectarea degetelor în ciocan."}
        ],
        "image_url": "https://images.unsplash.com/photo-1519824145371-296894a0daa9?auto=format&fit=crop&w=600&q=80",
        "prefix": "podologie_"
    },
    {
        "niche": "podologie",
        "emoji": "👣",
        "name": "Cabinet Podiatrie Sector 3",
        "phone": "0722 666 777",
        "location": "Bulevardul Camil Ressu nr. 42, Sector 3, București",
        "program": "Luni - Vineri: 08:30 - 20:00 | Sâmbătă: 09:00 - 13:00 | Duminică: Închis",
        "slogan_part1": "Tratament bătături &",
        "slogan_part2": "reconstrucție unghii deteriorate",
        "desc_niche": "podologie clinică, pedichiură medicală și protezări unghiale",
        "services": [
            {"icon": "🩹", "name": "Reconstrucție Unghie cu Gel", "desc": "Protezarea unghiilor traumatizate sau parțial lipsă cu geluri terapeutice speciale care permit creșterea unghiei naturale."},
            {"icon": "👣", "name": "Îndepărtare Bătături Dureroase", "desc": "Curățarea profundă a bătăturilor din talpă sau dintre degete folosind freze speciale, oferind ușurare instantanee la mers."},
            {"icon": "🔬", "name": "Analiză Plantară & Talonete", "desc": "Evaluarea modului de pășire și recomandări pentru talonete personalizate pentru corectarea mersului și posturii."}
        ],
        "image_url": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=600&q=80",
        "prefix": "podologie_"
    },
    {
        "niche": "podologie",
        "emoji": "👣",
        "name": "Tratamente Podologie Sector 4",
        "phone": "0761 333 555",
        "location": "Șoseaua Olteniței nr. 82, Sector 4, București",
        "program": "Luni - Vineri: 09:00 - 18:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Pedichiură medicală rapidă",
        "slogan_part2": "fără durere în sectorul 4",
        "desc_niche": "pedichiură terapeutică, îndepărtare calozități și îngrijire picior",
        "services": [
            {"icon": "👣", "name": "Curățare Calozități & Fisuri", "desc": "Îndepărtarea stratului gros de piele moartă și tratarea fisurilor dureroase din călcâie cu unguente hidratante."},
            {"icon": "🩹", "name": "Tratamente Unghii Fisurate", "desc": "Aplicarea de cleme speciale pentru repararea și ghidarea creșterii unghiilor care se crapă vertical."},
            {"icon": "🛡️", "name": "Sterilizare Instrumentar Premium", "desc": "Garantăm siguranță maximă prin sterilizarea instrumentelor în autoclav medical de clasa B după fiecare pacient."}
        ],
        "image_url": "https://images.unsplash.com/photo-1607860108855-64acf2078ed9?auto=format&fit=crop&w=600&q=80",
        "prefix": "podologie_"
    },
    {
        "niche": "tehnica_dentara",
        "emoji": "🦷",
        "name": "Art Dental Laboratory",
        "phone": "0722 121 212",
        "location": "Strada Baba Novac nr. 15, Sector 3, București",
        "program": "Luni - Vineri: 09:00 - 18:00 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Tehnică dentară premium &",
        "slogan_part2": "lucrări protetice digitale CAD-CAM",
        "desc_niche": "laborator tehnică dentară, protetică fixă și mobilă CAD-CAM",
        "services": [
            {"icon": "👑", "name": "Coroane & Punți Zirconiu", "desc": "Executăm coroane și punți dentare din zirconiu monolitic sau ceramică pe suport de zirconiu, prin frezare digitală 3D."},
            {"icon": "🦷", "name": "Proteze Dentare Elastice / Acrilice", "desc": "Realizare proteze mobile totale sau parțiale acrilice și proteze moderne elastice (BioDentaplast) rezistente și estetice."},
            {"icon": "💎", "name": "Lucrări pe Implante Dentare", "desc": "Execuție bonturi personalizate din titan/zirconiu și coroane înșurubate sau cimentate pe sisteme diverse de implante."}
        ],
        "image_url": "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?auto=format&fit=crop&w=600&q=80",
        "prefix": "tehnica_dentara_"
    },
    {
        "niche": "tehnica_dentara",
        "emoji": "🦷",
        "name": "Tehnică Dentară Pro-Estetic",
        "phone": "0765 232 323",
        "location": "Strada Agricultori nr. 56, Sector 2, București",
        "program": "Luni - Vineri: 08:30 - 18:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Restaurări dentare estetice &",
        "slogan_part2": "fațete din ceramică presată",
        "desc_niche": "tehnică dentară de înaltă estetică, fațete Emax și coroane ceramice",
        "services": [
            {"icon": "✨", "name": "Fațete Ceramice Emax", "desc": "Executăm fațete dentare ultra-subțiri din ceramică presată Emax pentru zâmbete perfecte cu minimă șlefuire."},
            {"icon": "👑", "name": "Coroane Metal-Ceramice", "desc": "Lucrări clasice rezistente din ceramică arsă pe suport metalic realizat prin sinterizare laser sau turnare."},
            {"icon": "🦷", "name": "Gutiere Bruxism & Albire", "desc": "Realizare gutiere personalizate din material termoplastic pentru bruxism (scrâșnit dinți) sau tratamente albire acasă."}
        ],
        "image_url": "https://images.unsplash.com/photo-1445527815219-ecbfec67492e?auto=format&fit=crop&w=600&q=80",
        "prefix": "tehnica_dentara_"
    },
    {
        "niche": "tehnica_dentara",
        "emoji": "🦷",
        "name": "Dental Lab Premium Mihai",
        "phone": "0733 454 545",
        "location": "Bulevardul Iuliu Maniu nr. 82, Sector 6, București",
        "program": "Luni - Vineri: 09:00 - 19:00 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Tehnică dentară CAD-CAM &",
        "slogan_part2": "gutiere printate 3D rapide",
        "desc_niche": "tehnică dentară digitală, gutiere și scheletate pe implante",
        "services": [
            {"icon": "🦷", "name": "Proteze Scheletate cu Sisteme", "desc": "Proiectăm și executăm proteze scheletate metalice rezistente cu sisteme speciale de ancorare (culise, capse)."},
            {"icon": "🖨️", "name": "Printare 3D Modele & Gutiere", "desc": "Printare rapidă 3D a modelelor de studiu, gutierelor de transfer și modelelor de lucru pe bază de scanări intraorale."},
            {"icon": "🔧", "name": "Reparații Proteze Dentare", "desc": "Adăugare dinți pe proteză, lipire proteze rupte sau crăpate și rebazări rapide pentru potrivire perfectă."}
        ],
        "image_url": "https://images.unsplash.com/photo-1598256989800-fe5f95da9787?auto=format&fit=crop&w=600&q=80",
        "prefix": "tehnica_dentara_"
    },
    {
        "niche": "tehnica_dentara",
        "emoji": "🦷",
        "name": "Atelier Tehnică Dentară Sector 4",
        "phone": "0765 565 656",
        "location": "Șoseaua Olteniței nr. 120, Sector 4, București",
        "program": "Luni - Vineri: 09:00 - 18:00 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Lucrări protetice de încredere",
        "slogan_part2": "pentru cabinete stomatologice",
        "desc_niche": "servicii tehnică dentară B2B pentru cabinete și clinici stomatologice",
        "services": [
            {"icon": "🦷", "name": "Coroane Provizorii PMMA", "desc": "Realizare coroane provizorii prin frezare PMMA din blocuri colorate, asigurând estetică excelentă pe durata vindecării."},
            {"icon": "👑", "name": "Inlay & Onlay Ceramic/Compozit", "desc": "Obturații indirecte realizate în laborator pentru refacerea dinților cu distrucții mari, potrivire ideală."},
            {"icon": "🤝", "name": "Colaborare B2B & Livrare Rapidă", "desc": "Serviciu curierat propriu pentru preluarea amprentelor fizice din cabinete și livrarea lucrărilor la timp."}
        ],
        "image_url": "https://images.unsplash.com/photo-1606811971618-4486d14f3f99?auto=format&fit=crop&w=600&q=80",
        "prefix": "tehnica_dentara_"
    },
    {
        "niche": "organizare_evenimente",
        "emoji": "✨",
        "name": "Wedding Decor București Simona",
        "phone": "0722 444 999",
        "location": "Strada Viitorului nr. 56, Sector 2, București",
        "program": "Luni - Duminică: 09:00 - 20:00 (Evenimente 24/7)",
        "slogan_part1": "Decoruri de nuntă elegante &",
        "slogan_part2": "aranjamente florale spectaculoase",
        "desc_niche": "organizare și decorare nunți, botezuri și evenimente private",
        "services": [
            {"icon": "🌸", "name": "Decor Nuntă Complet", "desc": "Amenajare prezidiu, mese invitați, decor intrare, panou foto (photocorner) cu flori naturale sau flori de mătase premium."},
            {"icon": "🌸", "name": "Buchete Mireasă & Lumânări", "desc": "Realizare buchete de mireasă/nașă unice, cocarde invitați și lumânări decorate de cununie și botez din flori proaspete."},
            {"icon": "💒", "name": "Decor Ceremonie Religioasă", "desc": "Amenajare covor roșu/alb, stâlpi decorativi cu flori, arcadă florală pentru cununie civilă în aer liber sau biserică."}
        ],
        "image_url": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=600&q=80",
        "prefix": "organizare_evenimente_"
    },
    {
        "niche": "organizare_evenimente",
        "emoji": "🎈",
        "name": "Organizare Evenimente Premium Alex",
        "phone": "0765 888 111",
        "location": "Calea Dorobanți nr. 182, Sector 1, București",
        "program": "Luni - Sâmbătă: 09:00 - 19:30 | Duminică: Evenimente",
        "slogan_part1": "Planificare evenimente corporate &",
        "slogan_part2": "petreceri private memorabile",
        "desc_niche": "organizare completă evenimente corporate și petreceri tematice",
        "services": [
            {"icon": "💼", "name": "Evenimente Corporate & Gale", "desc": "Planificare petreceri de Crăciun pentru firme, lansări de produse, gale festive, conferințe cu logistică completă inclusă."},
            {"icon": "🎈", "name": "Decoruri Baloane Organic", "desc": "Instalare arcade de baloane organice spectaculoase, panouri foto tematice pentru majorate, botezuri și aniversări."},
            {"icon": "🎧", "name": "Coordonare Furnizori Eveniment", "desc": "Selectare și coordonare DJ, sisteme sunet și lumini, servicii foto-video, cabine foto și catering pentru succesul petrecerii."}
        ],
        "image_url": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=600&q=80",
        "prefix": "organizare_evenimente_"
    },
    {
        "niche": "organizare_evenimente",
        "emoji": "🌸",
        "name": "Decoruri Florale Festive Ioana",
        "phone": "0731 222 999",
        "location": "Strada Dristorului nr. 22, Sector 3, București",
        "program": "Luni - Sâmbătă: 08:30 - 19:30 | Duminică: Evenimente",
        "slogan_part1": "Aranjamente florale premium",
        "slogan_part2": "pentru botezuri & nunți",
        "desc_niche": "aranjamente florale, decorare săli evenimente și accesorii festive",
        "services": [
            {"icon": "🌸", "name": "Aranjamente Mese Invitați", "desc": "Creații florale pe suporturi înalte din metal gold sau boluri de sticlă, realizate artistic în concordanță cu cromatica sălii."},
            {"icon": "🧸", "name": "Decor Botez & Ursitoare", "desc": "Panou foto tematic pentru botez (baloane, elemente din lemn personalizate, norișori), masa de prezidiu și aranjamente mese."},
            {"icon": "🎀", "name": "Accesorii Festive & Mărturii", "desc": "Mărturii handmade pentru invitați, meniuri printate personalizat, numere de masă, panou așezare invitați (seating chart)."}
        ],
        "image_url": "https://images.unsplash.com/photo-1519225495810-7512c696505a?auto=format&fit=crop&w=600&q=80",
        "prefix": "organizare_evenimente_"
    },
    {
        "niche": "organizare_evenimente",
        "emoji": "✨",
        "name": "Atelierul de Evenimente București",
        "phone": "0764 777 888",
        "location": "Strada Dealul Țugulea nr. 15, Sector 6, București",
        "program": "Luni - Duminică: 09:00 - 20:00",
        "slogan_part1": "Planificare nunți la cheie",
        "slogan_part2": "și consultanță organizare",
        "desc_niche": "wedding planning, coordonare evenimente și concepte tematice",
        "services": [
            {"icon": "💒", "name": "Wedding Planning (Planificare)", "desc": "Consultanță completă în stabilirea bugetului, alegerea restaurantului ideal, stabilirea temei, contractarea tuturor furnizorilor."},
            {"icon": "🤝", "name": "Coordonare în Ziua Nunții", "desc": "Coordonator dedicat prezent pe tot parcursul zilei pentru a supraveghea livrările, respectarea programului și rezolvarea urgențelor."},
            {"icon": "✨", "name": "Concepte & Tematici Custom", "desc": "Crearea unui concept vizual unic pentru petrecerea ta, definirea paletei de culori și asistență la achiziția elementelor."}
        ],
        "image_url": "https://images.unsplash.com/photo-1469371670807-013ccf25f16a?auto=format&fit=crop&w=600&q=80",
        "prefix": "organizare_evenimente_"
    }
]

PALETTES = {
    "servicii_mutari": {
        "primary": "#ea580c",
        "rgb": "234, 88, 12",
        "secondary": "#0f172a",
        "bg": "#fff7ed",
        "tag": "Servicii Mutări & Transport"
    },
    "cardiologie": {
        "primary": "#e11d48",
        "rgb": "225, 29, 72",
        "secondary": "#1e1b4b",
        "bg": "#fff1f2",
        "tag": "Cabinet Cardiologie & Ecografie"
    },
    "podologie": {
        "primary": "#0d9488",
        "rgb": "13, 148, 136",
        "secondary": "#0f172a",
        "bg": "#f0fdfa",
        "tag": "Cabinet Podologie Medicală"
    },
    "tehnica_dentara": {
        "primary": "#0ea5e9",
        "rgb": "14, 165, 233",
        "secondary": "#1e293b",
        "bg": "#f0f9ff",
        "tag": "Laborator Tehnică Dentară"
    },
    "organizare_evenimente": {
        "primary": "#d946ef",
        "rgb": "217, 70, 239",
        "secondary": "#2e0854",
        "bg": "#fdf4ff",
        "tag": "Organizare Evenimente & Decoruri"
    }
}

REVIEWS_TEMPLATES = {
    "servicii_mutari": [
        "Echipa Moving Express a fost extraordinară! Au demontat și remontat mobila de bucătărie extrem de rapid și curat. Nicio zgârietură pe obiecte. Recomand!",
        "Cel mai bun serviciu de transport mobilă din București. Au sosit la timp cu o dubă curată, au împachetat totul în folie și au lucrat foarte eficient. Preț excelent.",
        "Profesioniști desăvârșiți. S-au ocupat de relocarea sediului nostru de birouri în weekend, rapid și organizat. Mulțumim mult pentru ajutor!",
        "Recomand cu încredere Taxi Marfă. Am mutat o garsonieră și băieții au fost de mare ajutor cu manipularea pe scări. Foarte serioși și rapizi."
    ],
    "cardiologie": [
        "Domnul Dr. Adrian Popescu este un cardiolog de un profesionalism rar întâlnit. Mi-a explicat pe larg diagnosticul și ecografia cardiacă a fost făcută cu mare atenție.",
        "Cabinet foarte modern și curat. Serviciile de ecografie Doppler și montarea Holterului au decurs perfect. Recomand cabinetul din tot sufletul.",
        "Am avut o experiență excelentă la consultul de cardiologie. Personal amabil, explicații clare pentru tratamentul de tensiune și prețuri corecte.",
        "Evaluare cardiovasculară minuțioasă. Recomand cu căldură testul de efort și consultațiile oferite de medicii de la clinică. Mulțumesc."
    ],
    "podologie": [
        "Cabinet de podologie de nota 10! Pedichiura medicală a fost complet nedureroasă și călcâiele mele crăpate arată din nou perfect. Mulțumesc mult Roxana!",
        "Am urmat un tratament pentru o unghie încarnată extrem de dureroasă. Clemele aplicate au rezolvat problema fără operație. Recomand cu încredere!",
        "Recomand pentru tratamentul unghiilor afectate de ciupercă (micoză). Curățare mecanică atentă, sterilizare impecabilă și rezultate excelente.",
        "Foarte mulțumit de tratarea bătăturilor dureroase din talpă. Mă pot mișca din nou liber, fără niciun disconfort la mers. Profesionalism desăvârșit."
    ],
    "tehnica_dentara": [
        "Laboratorul Art Dental execută cele mai estetice coroane de zirconiu CAD-CAM. Potrivire marginală ideală și adaptare rapidă în cabinet.",
        "Profesioniști în lucrări pe implante dentare și proteze scheletate. Timpul de execuție este mereu respectat și calitatea este excepțională.",
        "Echipa stomatologică a lăudat calitatea fațetelor Emax realizate în acest laborator. Rezultatul estetic a fost pur și simplu spectaculos. Recomand!",
        "Gutiere de bruxism realizate rapid și cu precizie maximă. Colaborare B2B excelentă cu echipa laboratorului de tehnică dentară. Mulțumim."
    ],
    "organizare_evenimente": [
        "Aranjamentele florale realizate la nunta noastră au fost absolut spectaculoase! Toți invitații au lăudat panoul foto și decorul sălii. Mulțumim Simona!",
        "Alex ne-a ajutat cu organizarea completă a galei corporate. Logistică excelentă, atenție la detalii și o coordonare în ziua evenimentului ireproșabilă.",
        "Decorul cu baloane organice la botezul băiețelului nostru a fost de-a dreptul superb! Mulțumim Ioana pentru implicare, creativitate și promptitudine.",
        "Consultanță nuntă la cheie salvatoare! Ne-au recomandat cei mai buni furnizori, s-au încadrat în bugetul propus și au coordonat totul impecabil."
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
    
    niche_templates = REVIEWS_TEMPLATES.get(niche, REVIEWS_TEMPLATES["servicii_mutari"])
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
        num = 481 + idx
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
        html_content = html_content.replace("__DESC__", f"Servicii de {item['desc_niche']} în {item['location']}. Standarde ridicate de siguranță, promptitudine și servicii garantate cu echipamente profesionale.")
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
    siteuri_new_path = "/home/sol/Projects/leads-finder/SITEURI.TXT"
    
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
        
    # Write ONLY the new entries to SITEURI.TXT
    with open(siteuri_new_path, "w", encoding="utf-8") as f:
        f.write("\n".join(siteuri_entries))
        
    print("Registries updated successfully.")

if __name__ == "__main__":
    main()
