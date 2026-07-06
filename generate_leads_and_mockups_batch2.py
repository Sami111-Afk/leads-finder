# -*- coding: utf-8 -*-
import os
import re
import random
import json
import subprocess

LEADS = [
    {
        "niche": "peisagistica",
        "emoji": "🏡",
        "name": "Green Garden Design București",
        "phone": "0722 558 221",
        "location": "Strada Jandarmeriei nr. 14, Sector 1, București",
        "program": "Luni - Sâmbătă: 08:00 - 19:00 | Duminică: Închis",
        "slogan_part1": "Amenajări grădini &",
        "slogan_part2": "peisagistică rezidențială",
        "desc_niche": "peisagistică, proiectare și amenajare grădini",
        "services": [
            {"icon": "🌿", "name": "Amenajare & Gazonare Grădini", "desc": "Pregătirea solului, montaj rulouri gazon natural sau însămânțare, plantare arbori și arbuști ornamentali."},
            {"icon": "💦", "name": "Sisteme Automate Irigații", "desc": "Proiectare și instalare sisteme de irigații prin picurare sau aspersie cu automatizări Hunter sau Rain Bird."},
            {"icon": "✂️", "name": "Întreținere Gazon & Plante", "desc": "Tundere gazon, scarificare, fertilizare sezonieră, toaletare gard viu și tratamente fitosanitare plante."}
        ],
        "image_url": "https://images.unsplash.com/photo-1558904541-efa8c3a30fc9?auto=format&fit=crop&w=600&q=80",
        "prefix": "peisagistica_"
    },
    {
        "niche": "peisagistica",
        "emoji": "🌳",
        "name": "Amenajări Grădini Ilfov Marius",
        "phone": "0764 121 212",
        "location": "Strada Griviței nr. 56, Bragadiru, Ilfov",
        "program": "Luni - Sâmbătă: 08:00 - 18:00 | Duminică: Închis",
        "slogan_part1": "Gazon rulou &",
        "slogan_part2": "amenajări curți exterioare",
        "desc_niche": "amenajări grădini, montaj gazon și întreținere spații verzi",
        "services": [
            {"icon": "🏡", "name": "Pregătire & Nivelare Teren", "desc": "Decopertare iarbă veche, adăugare pământ vegetal fertil, nivelare mecanică și compactare sol."},
            {"icon": "🧱", "name": "Montaj Dale & Alei Grădină", "desc": "Realizare alei din piatră naturală, dale din beton vibrat și delimitări cu borduri de grădină."},
            {"icon": "🍃", "name": "Curățenie de Primăvară/Toamnă", "desc": "Strângere frunze, tăieri de curățare arbori, toaletare arbuști și curățare generală curți."}
        ],
        "image_url": "https://images.unsplash.com/photo-1592417817098-8f3d6eb19675?auto=format&fit=crop&w=600&q=80",
        "prefix": "peisagistica_"
    },
    {
        "niche": "hvac_clima",
        "emoji": "❄️",
        "name": "Clima Install București Mihai",
        "phone": "0724 998 889",
        "location": "Bulevardul Constantin Brâncoveanu nr. 35, Sector 4, București",
        "program": "Luni - Vineri: 08:00 - 20:00 | Sâmbătă: 09:00 - 15:00 | Duminică: Urgențe",
        "slogan_part1": "Montaj aer condiționat &",
        "slogan_part2": "reparații climatizare",
        "desc_niche": "montaj, igienizare și service aer condiționat",
        "services": [
            {"icon": "⚙️", "name": "Montaj Aer Condiționat", "desc": "Instalare profesională unități AC de tip split, multi-split sau casetă, cu pompă de vid și console rezistente."},
            {"icon": "🧼", "name": "Igienizare & Curățare Chimică", "desc": "Spălare cu soluții antibacteriene a filtrelor și vaporizatorului, combatere mucegai și eliminare mirosuri neplăcute."},
            {"icon": "🧪", "name": "Service & Încărcare Freon", "desc": "Detectare pierderi refrigerant, sudură conducte cupru, vidare și încărcare cu freon ecologic R32 sau R410A."}
        ],
        "image_url": "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=600&q=80",
        "prefix": "hvac_clima_"
    },
    {
        "niche": "hvac_clima",
        "emoji": "💨",
        "name": "Aer Condiționat Rapid Robert",
        "phone": "0733 445 445",
        "location": "Strada Baba Novac nr. 22, Sector 3, București",
        "program": "Luni - Duminică: 08:00 - 21:00",
        "slogan_part1": "Montaj rapid climatizare",
        "slogan_part2": "în București & Ilfov",
        "desc_niche": "instalare aer condiționat și reparații HVAC rapide",
        "services": [
            {"icon": "💨", "name": "Montaj în 48 de Ore", "desc": "Intervenții ultra-rapide pentru montaj aer condiționat cu kitul clientului sau echipamente asigurate de noi."},
            {"icon": "🛠️", "name": "Reparații Plăci Electronice", "desc": "Diagnosticare și remediere defecte la placa electronică, senzori de temperatură, motor ventilator sau compresor."},
            {"icon": "🔌", "name": "Traseu Frigoric & Străpungeri", "desc": "Realizare găuri prin carotare umedă/uscată, prelungiri trasee frigorifice și mascare în canal cablu."}
        ],
        "image_url": "https://images.unsplash.com/photo-1581094271901-8022ec446665?auto=format&fit=crop&w=600&q=80",
        "prefix": "hvac_clima_"
    },
    {
        "niche": "fotografie_evenimente",
        "emoji": "📸",
        "name": "Alex Popescu Photo-Video",
        "phone": "0765 898 989",
        "location": "Calea Victoriei nr. 120, Sector 1, București",
        "program": "Luni - Duminică: 09:00 - 21:00 (Evenimente 24/7)",
        "slogan_part1": "Fotografie de nuntă &",
        "slogan_part2": "clipuri video de poveste",
        "desc_niche": "servicii profesionale de fotografie și videografie pentru evenimente",
        "services": [
            {"icon": "👰", "name": "Fotografie Nuntă & Botez", "desc": "Ședințe foto dedicate, pregătiri, ceremonie, petrecere, prelucrare profesională a tuturor cadrelor livrate rapid."},
            {"icon": "🎥", "name": "Videografie & Clip Nuntă (4K)", "desc": "Filmări cinematografice de înaltă rezoluție, montaj dinamic video, clip de tip Best Moments și înregistrări audio separate."},
            {"icon": "🛸", "name": "Filmări cu Dronă 4K", "desc": "Imagini aeriene spectaculoase de la biserică sau restaurant cu operator autorizat și echipament DJI de ultimă generație."}
        ],
        "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=600&q=80",
        "prefix": "fotografie_evenimente_"
    },
    {
        "niche": "fotografie_evenimente",
        "emoji": "🎞️",
        "name": "Studio Foto București Alina Sandu",
        "phone": "0728 112 233",
        "location": "Strada Vasile Lascăr nr. 62, Sector 2, București",
        "program": "Luni - Sâmbătă: 10:00 - 19:30 | Duminică: Evenimente",
        "slogan_part1": "Ședințe foto studio &",
        "slogan_part2": "fotografie portret / brand",
        "desc_niche": "studio foto profesional, ședințe de studio, portret și brand personal",
        "services": [
            {"icon": "👤", "name": "Portrete de Business & Brand", "desc": "Fotografii profesionale pentru profiluri sociale (LinkedIn), site-uri corporative și portofolii personale."},
            {"icon": "🤰", "name": "Ședințe Maternitate & Familie", "desc": "Ședințe foto în studio decorat călduros, capturând momentele prețioase ale sarcinii sau imagini de familie vesele."},
            {"icon": "👜", "name": "Fotografie de Produs & E-commerce", "desc": "Fotografii clare pentru magazine online, realizate pe fundal alb sau în decor stilizat pentru rețelele sociale."}
        ],
        "image_url": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=600&q=80",
        "prefix": "fotografie_evenimente_"
    },
    {
        "niche": "curatenie_profesionala",
        "emoji": "✨",
        "name": "Professional Clean București",
        "phone": "0763 333 444",
        "location": "Bulevardul Decebal nr. 12, Sector 3, București",
        "program": "Luni - Sâmbătă: 08:00 - 20:00 | Duminică: Închis",
        "slogan_part1": "Curățenie generală &",
        "slogan_part2": "igienizare post-constructor",
        "desc_niche": "servicii de curățenie generală, post-constructor și birouri",
        "services": [
            {"icon": "🏗️", "name": "Curățenie Post-Constructor", "desc": "Îndepărtarea resturilor de vopsea, ciment, praf de glet, spălare geamuri și curățare profundă pardoseli după renovări."},
            {"icon": "🏠", "name": "Curățenie Generală Locuințe", "desc": "Spălare faianță/gresie, aspirare covoare, ștergere praf mobilă, dezinfectare băi și bucătării, spălare geamuri."},
            {"icon": "🏢", "name": "Curățenie Birouri & Spații", "desc": "Abonamente lunare pentru menținerea curățeniei în spații comerciale, birouri, clinici sau scări de bloc."}
        ],
        "image_url": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=600&q=80",
        "prefix": "curatenie_profesionala_"
    },
    {
        "niche": "curatenie_profesionala",
        "emoji": "🧼",
        "name": "Eco Cleaning Services Simona",
        "phone": "0722 777 888",
        "location": "Strada Dealul Țugulea nr. 42, Sector 6, București",
        "program": "Luni - Vineri: 08:30 - 18:30 | Sâmbătă: 09:00 - 15:00 | Duminică: Închis",
        "slogan_part1": "Servicii ecologice curățenie",
        "slogan_part2": "la prețuri atractive",
        "desc_niche": "curățenie la domiciliu cu detergenți ecologici non-toxici",
        "services": [
            {"icon": "🍃", "name": "Curățenie Eco la Domiciliu", "desc": "Spălare și curățare exclusiv cu detergenți bio, siguri pentru copii și animale de companie, fără mirosuri iritante."},
            {"icon": "🪟", "name": "Spălare Geamuri & Vitrine", "desc": "Curățare geamuri exterioare/interioare la apartamente, case sau vitrine de magazine, fără urme sau dungi."},
            {"icon": "💨", "name": "Curățare Tapisat & Saltele", "desc": "Igienizare cu injecție-extracție și tratament cu aburi pentru saltele, fotolii sau covoare direct acasă."}
        ],
        "image_url": "https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?auto=format&fit=crop&w=600&q=80",
        "prefix": "curatenie_profesionala_"
    },
    {
        "niche": "catering",
        "emoji": "🍳",
        "name": "Atelierul de Catering",
        "phone": "0731 223 344",
        "location": "Strada Lucrețiu Pătrășcanu nr. 9, Sector 3, București",
        "program": "Luni - Duminică: 07:00 - 20:00 (Comenzi evenimente)",
        "slogan_part1": "Catering evenimente &",
        "slogan_part2": "meniuri zilnice delicioase",
        "desc_niche": "servicii de catering corporate și evenimente private",
        "services": [
            {"icon": "🎉", "name": "Catering Evenimente Private", "desc": "Meniuri adaptate pentru nunți, botezuri, aniversări sau petreceri de familie, preparate calde și reci livrate cald."},
            {"icon": "💼", "name": "Catering Corporate & Business", "desc": "Mese de prânz pentru angajați, platouri office, dineuri, dineuri tip bufet suedez sau coffee breaks pentru conferințe."},
            {"icon": "🍢", "name": "Platouri Finger Food & Aperitive", "desc": "Platouri asortate de mini-aperitive, frigărui, mini-burgers, quiche-uri, ideale pentru orice tip de petrecere."}
        ],
        "image_url": "https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=600&q=80",
        "prefix": "catering_"
    },
    {
        "niche": "catering",
        "emoji": "🧁",
        "name": "Candy Bar Premium București",
        "phone": "0765 443 322",
        "location": "Calea Dorobanți nr. 142, Sector 1, București",
        "program": "Luni - Sâmbătă: 09:00 - 19:00 | Duminică: Închis",
        "slogan_part1": "Candy bar personalizat",
        "slogan_part2": "pentru momente dulci",
        "desc_niche": "candy bar evenimente, prăjituri premium și decoruri tematice",
        "services": [
            {"icon": "🧁", "name": "Candy Bar Evenimente", "desc": "Mini-prăjituri delicioase (macarons, cupcakes, pop-cakes, mousse) asortate colorat cu tema evenimentului tău."},
            {"icon": "🎂", "name": "Torturi Aniversare & Nuntă", "desc": "Torturi personalizate ca design și compoziție, preparate doar din ingrediente naturale premium (friscă naturală, ciocolată belgiană)."},
            {"icon": "🍡", "name": "Fruit Bar & Fântână Ciocolată", "desc": "Fructe proaspete tăiate artistic și fântână de ciocolată caldă Callebaut pentru deliciul tuturor invitaților."}
        ],
        "image_url": "https://images.unsplash.com/photo-1535141192574-5d4897c13636?auto=format&fit=crop&w=600&q=80",
        "prefix": "catering_"
    },
    {
        "niche": "dermatologie",
        "emoji": "🩺",
        "name": "Dermacare Estetic Dr. Radu",
        "phone": "0723 555 666",
        "location": "Strada Viitorului nr. 102, Sector 2, București",
        "program": "Luni - Vineri: 09:00 - 20:00 | Sâmbătă: 10:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Tratamente dermatologice &",
        "slogan_part2": "estetică medicală premium",
        "desc_niche": "consultații dermatologice și micro-proceduri estetice",
        "services": [
            {"icon": "🩺", "name": "Consultații Dermatologie", "desc": "Diagnosticare și tratament acnee, dermatite, psoriazis, infecții piele, precum și dermatoscopie examinare alunițe."},
            {"icon": "💉", "name": "Proceduri Estetice Injectabile", "desc": "Tratamente cu acid hialuronic buze/riduri, injectări toxina botulinică pentru riduri mimice și mezoterapie skin-glow."},
            {"icon": "🔬", "name": "Micro-Chirurgie Dermatologică", "desc": "Excizii dermatologice pentru papiloame, veruci sau nevi, realizate cu anestezie locală și tehnologie laser/electrocauter."}
        ],
        "image_url": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=600&q=80",
        "prefix": "dermatologie_"
    },
    {
        "niche": "dermatologie",
        "emoji": "⚕️",
        "name": "Cabinet Dermatologie Dr. Elena Popa",
        "phone": "0744 990 011",
        "location": "Bulevardul Primăverii nr. 18, Sector 1, București",
        "program": "Luni - Joi: 10:00 - 18:30 | Vineri: 09:00 - 16:00 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Consultații dermatologice pentru",
        "slogan_part2": "adulți și copii",
        "desc_niche": "dermatologie clinică, pediatrică și tratamente laser",
        "services": [
            {"icon": "👶", "name": "Dermatologie Pediatrică", "desc": "Consultații adaptate și tratamente blânde pentru bebeluși și copii: dermatită atopică, iritații de scutec, eczeme."},
            {"icon": "✨", "name": "Peeling Chimic & Laser", "desc": "Proceduri de peeling chimic controlat pentru tratarea urmelor de acnee, pigmentare și laser reîntinerire facială."},
            {"icon": "🩹", "name": "Tratament Cicatrici & Vergeturi", "desc": "Terapii moderne minim-invazive de microneedling și rejuvenare pentru estomparea cicatricilor post-acneice sau operatorii."}
        ],
        "image_url": "https://images.unsplash.com/photo-1579684389782-64d84b5e901d?auto=format&fit=crop&w=600&q=80",
        "prefix": "dermatologie_"
    },
    {
        "niche": "logopedie",
        "emoji": "🗣️",
        "name": "Cabinet Logopedie Ioana Radu",
        "phone": "0724 445 566",
        "location": "Bulevardul Camil Ressu nr. 22, Sector 3, București",
        "program": "Luni - Vineri: 08:30 - 19:30 | Sâmbătă: 09:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Terapie logopedică &",
        "slogan_part2": "dezvoltare vorbire copii",
        "desc_niche": "evaluare logopedică și corectare pronunție copii",
        "services": [
            {"icon": "🗣️", "name": "Corectare Tulburări Pronunție", "desc": "Terapie logopedică pentru dislalie (pronunțarea incorectă a sunetelor, ex: R, S, L), dislexie, disgrafie și balbism."},
            {"icon": "🧠", "name": "Evaluare Logopedică Completă", "desc": "Testarea nivelului limbajului, vocabularului, structurii gramaticale și stabilirea unui plan de intervenție personalizat."},
            {"icon": "🧸", "name": "Logopedie prin Joc (Interactive)", "desc": "Ședințe interactive și atractive concepute sub formă de joc, special pentru copii mici de 3-7 ani."}
        ],
        "image_url": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=600&q=80",
        "prefix": "logopedie_"
    },
    {
        "niche": "logopedie",
        "emoji": "💬",
        "name": "Logopedie & Dezvoltare Andreea",
        "phone": "0761 889 889",
        "location": "Bulevardul Iuliu Maniu nr. 59, Sector 6, București",
        "program": "Luni - Vineri: 09:00 - 19:00 | Sâmbătă: 10:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Ajută-ți copilul să",
        "slogan_part2": "comunice cu încredere",
        "desc_niche": "ședințe de logopedie, dezvoltare limbaj și pregătire școlară",
        "services": [
            {"icon": "💬", "name": "Stimulare Vorbire Întârziată", "desc": "Programe speciale pentru stimularea apariției limbajului la copiii care nu vorbesc sau au vocabular limitat."},
            {"icon": "📖", "name": "Pregătire Logopedică Școlară", "desc": "Dezvoltarea auzului fonematic, silabisire, scriere-citire corectă, pregătire pentru integrarea în ciclul primar."},
            {"icon": "👨‍👩‍👧", "name": "Consiliere Părinți & Teme", "desc": "Ghidaj complet pentru părinți, recomandări de exerciții și jocuri distractive de exersat zilnic acasă."}
        ],
        "image_url": "https://images.unsplash.com/photo-1543269865-cbf427effbad?auto=format&fit=crop&w=600&q=80",
        "prefix": "logopedie_"
    },
    {
        "niche": "inchirieri_auto",
        "emoji": "🔑",
        "name": "Rent a Car Otopeni Express",
        "phone": "0733 999 111",
        "location": "Calea Bucureștilor nr. 224D, Otopeni, Ilfov",
        "program": "Luni - Duminică: Non-Stop (Livrare Aeroport 24/7)",
        "slogan_part1": "Închirieri auto aeroport",
        "slogan_part2": "fără garanție sau costuri ascunse",
        "desc_niche": "servicii de închirieri auto rent-a-car la Aeroportul Otopeni",
        "services": [
            {"icon": "✈️", "name": "Predare / Preluare la Aeroport", "desc": "Serviciu gratuit de predare și preluare direct la terminalul Sosiri/Plecări din Aeroportul Henri Coandă Otopeni."},
            {"icon": "🚗", "name": "Flotă Auto Diversificată", "desc": "Gama largă de mașini bine întreținute, economice, SUV-uri, automate sau compacte, cu asigurare completă RCA/CASCO."},
            {"icon": "🛡️", "name": "Opțiune Fără Depozit (Zero Risc)", "desc": "Posibilitate de închiriere auto cu depozit/garanție zero, prin achitarea unei asigurări zilnice complete."}
        ],
        "image_url": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?auto=format&fit=crop&w=600&q=80",
        "prefix": "inchirieri_auto_"
    },
    {
        "niche": "inchirieri_auto",
        "emoji": "🚘",
        "name": "Auto Rent București Non-Stop",
        "phone": "0766 888 777",
        "location": "Bulevardul Unirii nr. 64, Sector 5, București",
        "program": "Luni - Duminică: Non-Stop (24/7)",
        "slogan_part1": "Mașini de închiriat",
        "slogan_part2": "pe termen scurt și lung",
        "desc_niche": "închirieri auto în București și județul Ilfov",
        "services": [
            {"icon": "📅", "name": "Închirieri pe Termen Scurt", "desc": "Soluții flexibile de închiriere auto pentru o zi, un weekend sau concediu, cu livrare rapidă la adresa dorită."},
            {"icon": "🏢", "name": "Închirieri Corporate & Termen Lung", "desc": "Abonamente și leasing operațional avantajos pentru firme, incluzând mentenanță completă și mașină la schimb."},
            {"icon": "🗺️", "name": "Km Nelimitați & GPS inclus", "desc": "Toate închirierile beneficiază de kilometri nelimitați pe teritoriul României și asistență rutieră non-stop."}
        ],
        "image_url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=600&q=80",
        "prefix": "inchirieri_auto_"
    },
    {
        "niche": "instructor_auto",
        "emoji": "🚗",
        "name": "Instructor Auto Daniel Cat. B",
        "phone": "0722 112 211",
        "location": "Șoseaua Berceni nr. 104, Sector 4, București",
        "program": "Luni - Sâmbătă: 07:00 - 21:00 | Duminică: Închis",
        "slogan_part1": "Ședințe de conducere &",
        "slogan_part2": "pregătire examen obținere permis",
        "desc_niche": "instructor auto categoria B, ședințe conducere și perfecționare",
        "services": [
            {"icon": "🚗", "name": "Curs Complet Școala Șoferi B", "desc": "Instruire practică 30 de ore pe mașină modernă, pregătire dosar și asistență la susținerea examenului practic (traseu)."},
            {"icon": "📈", "name": "Ședințe Perfecționare Posesori", "desc": "Ședințe dedicate persoanelor care dețin deja permis dar nu au condus de mult timp: parcări, trafic aglomerat."},
            {"icon": "📚", "name": "Pregătire Teoretică & Chestionare", "desc": "Suport curs legislație rutieră și explicarea detaliată a regulamentului rutier pentru promovarea sălii din prima."}
        ],
        "image_url": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=600&q=80",
        "prefix": "instructor_auto_"
    },
    {
        "niche": "instructor_auto",
        "emoji": "🚦",
        "name": "Școala de Șoferi Start Marius",
        "phone": "0765 990 990",
        "location": "Bulevardul Chișinău nr. 14, Sector 3, București",
        "program": "Luni - Sâmbătă: 08:00 - 20:00 | Duminică: Închis",
        "slogan_part1": "Învață să conduci relaxat",
        "slogan_part2": "cu instructori calmi",
        "desc_niche": "instruire auto, cursuri legislație și perfecționare în conducere",
        "services": [
            {"icon": "🚗", "name": "Instruire Practică Categoria B", "desc": "Pregătire practică pe mașini cu transmisie manuală sau automată, cu trasee similare celor de la examen."},
            {"icon": "🅿️", "name": "Simulări Traseu Examen (Poligon)", "desc": "Simularea exactă a examenului cu instructorul, parcări laterale/perpendiculare, pornirea din rampă și întoarceri."},
            {"icon": "🕒", "name": "Program Flexibil Ședințe", "desc": "Preluare și predare cursant de la metrou sau de la adresa dorită, la ore stabilite în funcție de programul tău."}
        ],
        "image_url": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=600&q=80",
        "prefix": "instructor_auto_"
    },
    {
        "niche": "alpinism_toaletare",
        "emoji": "🧗",
        "name": "Alpinism Utilitar București Gabi",
        "phone": "0764 555 666",
        "location": "Strada Valea Oltului nr. 82, Sector 6, București",
        "program": "Luni - Sâmbătă: 08:00 - 18:00 (Urgențe Non-Stop)",
        "slogan_part1": "Lucrări la înălțime &",
        "slogan_part2": "alpinism utilitar profesionist",
        "desc_niche": "alpinism utilitar, reparații fațade și lucrări la înălțime",
        "services": [
            {"icon": "🏢", "name": "Reparații & Curățare Fațade", "desc": "Tencuieli, vopsitorie, reparații rosturi dilatație, spălare geamuri clădiri de birouri și montaj publicitate."},
            {"icon": "🪵", "name": "Toaletări & Tăieri Arbori", "desc": "Tăieri controlate de crengi uscate sau arbori periculoși poziționați în spații greu accesibile, prin tehnici de alpinism."},
            {"icon": "🧱", "name": "Montaj Jgheaburi & Parazăpezi", "desc": "Montare sau curățare jgheaburi și burlane la case sau blocuri, montaj parazăpezi și eliminare țurțuri iarna."}
        ],
        "image_url": "https://images.unsplash.com/photo-1508962914676-134849a727f0?auto=format&fit=crop&w=600&q=80",
        "prefix": "alpinism_toaletare_"
    },
    {
        "niche": "alpinism_toaletare",
        "emoji": "🌲",
        "name": "Toaletare Arbori & Tăieri Copaci",
        "phone": "0722 333 222",
        "location": "Strada Principală nr. 90, Cernica, Ilfov",
        "program": "Luni - Duminică: 08:00 - 19:00",
        "slogan_part1": "Tăieri arbori periculoși",
        "slogan_part2": "în siguranță maximă",
        "desc_niche": "servicii de toaletare arbori, defrișări și tocări crengi",
        "services": [
            {"icon": "🪓", "name": "Tăiere Arbori Periculoși", "desc": "Tăierea copacilor mari, înclinați sau uscați din curți care pun în pericol case, linii electrice sau garduri."},
            {"icon": "✂️", "name": "Toaletare & Corecție Coroană", "desc": "Tăieri de formare și aerisire pentru copaci ornamentali sau fructiferi, stimulând creșterea sănătoasă."},
            {"icon": "🚜", "name": "Defrișări Terenuri & Tocare", "desc": "Curățarea completă a terenurilor de vegetație sălbatică, arbuști și tocare crengi cu utilaje profesionale."}
        ],
        "image_url": "https://images.unsplash.com/photo-1590486803833-1c5dc8ddd4c8?auto=format&fit=crop&w=600&q=80",
        "prefix": "alpinism_toaletare_"
    }
]

PALETTES = {
    "peisagistica": {
        "primary": "#15803d",
        "rgb": "21, 128, 61",
        "secondary": "#1e293b",
        "bg": "#f0fdf4",
        "tag": "Amenajări Grădini & Peisagistică"
    },
    "hvac_clima": {
        "primary": "#0ea5e9",
        "rgb": "14, 165, 233",
        "secondary": "#0f172a",
        "bg": "#f0f9ff",
        "tag": "Montaj & Service Climatizare"
    },
    "fotografie_evenimente": {
        "primary": "#a855f7",
        "rgb": "168, 85, 247",
        "secondary": "#090514",
        "bg": "#faf5ff",
        "tag": "Servicii Foto-Video Profesionale"
    },
    "curatenie_profesionala": {
        "primary": "#06b6d4",
        "rgb": "6, 182, 212",
        "secondary": "#0f172a",
        "bg": "#f0fdfa",
        "tag": "Servicii Curățenie Premium"
    },
    "catering": {
        "primary": "#ec4899",
        "rgb": "236, 72, 153",
        "secondary": "#310c22",
        "bg": "#fdf2f8",
        "tag": "Servicii Catering Premium"
    },
    "dermatologie": {
        "primary": "#0d9488",
        "rgb": "13, 148, 136",
        "secondary": "#1e1b4b",
        "bg": "#f0fdfa",
        "tag": "Cabinet Dermatologie & Estetică"
    },
    "logopedie": {
        "primary": "#e11d48",
        "rgb": "225, 29, 72",
        "secondary": "#1e293b",
        "bg": "#fff1f2",
        "tag": "Cabinet Logopedie & Terapie"
    },
    "inchirieri_auto": {
        "primary": "#f59e0b",
        "rgb": "245, 158, 11",
        "secondary": "#0f172a",
        "bg": "#fffbeb",
        "tag": "Închirieri Auto Rent-a-Car"
    },
    "instructor_auto": {
        "primary": "#3b82f6",
        "rgb": "59, 130, 246",
        "secondary": "#0f172a",
        "bg": "#eff6ff",
        "tag": "Instructor Auto Autorizat"
    },
    "alpinism_toaletare": {
        "primary": "#16a34a",
        "rgb": "22, 163, 74",
        "secondary": "#111827",
        "bg": "#f0fdf4",
        "tag": "Toaletări & Lucrări la Înălțime"
    }
}

REVIEWS_TEMPLATES = {
    "peisagistica": [
        "Sunt extrem de mulțumită de cum mi-au amenajat grădina! Gazonul rulou arată impecabil și s-a prins extraordinar de bine. Servicii profesionale de nota 10.",
        "Montajul sistemului automat de irigații a decurs foarte rapid și funcționează perfect. Acum grădina mea este verde și fresh tot timpul.",
        "Echipă serioasă și bine dotată. Au curățat curtea de resturi, au toaletat pomii și au nivelat terenul impecabil. Prețul a fost cel stabilit inițial.",
        "Recomand Green Garden Design! Proiectul de amenajare 3D a fost superb și au transpus totul în realitate cu mare precizie și seriozitate."
    ],
    "hvac_clima": [
        "Montajul aerului condiționat a fost realizat rapid și curat. Au strâns tot praful cu aspiratorul în timp ce dădeau gaura. Meseriași cu bun simț.",
        "Igienizarea aparatului AC a scos toate mirosurile neplăcute. Acum aerul este curat și răcește ca nou. Mulțumesc mult Clima Install!",
        "Servicii profesionale. Au detectat o fisură mică pe unde pierdea freon, au sudat conducta și au reîncărcat instalația rapid. Recomand cu drag.",
        "Echipă punctuală și foarte experimentată. Montaj realizat impecabil cu materiale de calitate superioară. Foarte mulțumit."
    ],
    "fotografie_evenimente": [
        "Alex ne-a fotografiat nunta și pozele au ieșit de-a dreptul magice! A capturat toate emoțiile noastre într-un mod natural și discret. Livrare rapidă.",
        "Clipul video de nuntă realizat de ei este o capodoperă cinematică. Montaj de înaltă clasă și filmări cu dronă spectaculoase. Recomand cu drag!",
        "Alina ne-a făcut ședința foto de maternitate și ne-am simțit extrem de relaxați în studio. Portretele au o lumină superbă și sunt foarte expresive.",
        "Fotografii de produs impecabile pentru magazinul nostru online. Fundal curat, culori reale și livrare în timp record. Mulțumim mult!"
    ],
    "curatenie_profesionala": [
        "Curățenia post-constructor după renovarea apartamentului a fost impecabilă. Au curățat toate petele de glet și vopsea și au lăsat totul lună. Recomand!",
        "Simona a făcut o treabă excelentă. Curățenia generală în casă a fost realizată cu produse ecologice foarte sigure pentru fetița mea mică. Mulțumesc!",
        "Abonament de curățenie pentru biroul nostru de nota 10. Echipă serioasă, rapidă și discretă. Raport calitate-preț foarte bun.",
        "Spălarea geamurilor exterioare la apartamentul de la etajul 6 a fost realizată în siguranță deplină și geamurile sunt impecabile. Foarte serioși."
    ],
    "catering": [
        "Mâncarea oferită la aniversarea copilului nostru a fost delicioasă și caldă! Toți invitații au lăudat aperitivele și finger food-ul. Servicii de top.",
        "Candy barul personalizat a fost atracția serii la nuntă! Macarons și cupcakes excepționale ca gust și un design superb potrivit cu tema noastră.",
        "Serviciu de catering corporate foarte serios. Platourile office au sosit la ora stabilită, extrem de proaspete și frumos aranjate. Recomand!",
        "Tortul de nuntă comandat a fost exact cum am visat: textură fină, compoziție cu ciocolată belgiană și ingrediente 100% naturale. Superb."
    ],
    "dermatologie": [
        "Dr. Radu este un medic dermatolog de excepție! Mi-a tratat o acnee severă care nu trecea de ani de zile. Cabinet modern și consultații amănunțite.",
        "Am făcut injectare cu acid hialuronic pentru ridurile nazolabiale și rezultatul este extrem de natural și frumos. Medic foarte talentat și blând.",
        "Îndepărtarea papiloamelor cu laser a fost complet nedureroasă și vindecarea a fost foarte rapidă. Recomand cu încredere Dermacare.",
        "Consultație dermatoscopică amănunțită pentru alunițe. Mi-a explicat detaliat fiecare aspect și m-am simțit în siguranță pe tot parcursul vizitei."
    ],
    "logopedie": [
        "Datorită ședințelor cu doamna Ioana Radu, băiețelul meu a început să pronunțe corect sunetul R după doar două luni de terapie logopedică. O recomand cu drag!",
        "Ședințele logopedice sunt extrem de interactive și bazate pe joc, fetița mea merge mereu cu mare drag la cabinet. Progrese vizibile foarte rapide.",
        "Recomand cu căldură. Evaluare inițială completă și corectă, urmată de ședințe bine structurate. Logoped de excepție, foarte cald și calm.",
        "Stimularea vorbirii a dat roade rapid. Copilul meu are acum un vocabular bogat și comunică cu încredere și claritate. Mulțumim mult!"
    ],
    "inchirieri_auto": [
        "Am închiriat o mașină din Otopeni și livrarea la aeroport a fost la secundă! Fără depozit, asigurare completă și prețuri foarte bune. Recomand!",
        "Flota auto este foarte modernă și mașinile sunt extrem de curate și bine întreținute. Procedură de închiriere simplă, fără costuri ascunse.",
        "Închiriez de la ei de fiecare dată când vin în țară. Asistență clienți de nota 10 și kilometri nelimitați. Cei mai serioși din București.",
        "Am ales opțiunea de închiriere auto fără garanție și totul a decurs fără niciun risc. Livrare și preluare rapidă direct la adresa mea. Excelent."
    ],
    "instructor_auto": [
        "Daniel este un instructor auto incredibil de calm și explică totul pe înțeles. Am promovat examenul de traseu din prima încercare! Îl recomand din suflet.",
        "Ședințele de perfecționare auto m-au ajutat să scap de frica de a conduce în traficul intens din București. Parcarea laterală nu mai este o problemă.",
        "Instruire practică excelentă. Mașina este nouă și ușor de condus, iar instructorul are o răbdare de fier. Îți mulțumesc mult pentru tot, Daniel!",
        "Pregătire riguroasă pe traseele de examen. Știe exact ce se cere la proba practică și explică toate micile capcane. Nota 10 cu felicitări."
    ],
    "alpinism_toaletare": [
        "Toaletarea arborilor înalți din curtea noastră a fost realizată cu maxim profesionalism și siguranță pentru firele electrice. Au strâns și curățat tot curtea în urmă.",
        "Am colaborat pentru reparații tencuieli și rosturi de dilatație la fațada blocului nostru. Alpiniști rapizi, serioși și lucrare bine executată.",
        "Tăierea copacului uscat și înclinat peste gardul vecinului s-a făcut impecabil, bucată cu bucată, fără nicio pagubă. Profesioniști adevărați.",
        "Montajul jgheaburilor și parazăpezilor la casa noastră a fost executat de alpiniști utilitari foarte rapizi. Preț corect și servicii excelente."
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
    
    niche_templates = REVIEWS_TEMPLATES.get(niche, REVIEWS_TEMPLATES["peisagistica"])
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
        num = 441 + idx
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
        html_content = html_content.replace("__DESC__", f"Servicii profesionale de {item['desc_niche']} în {item['location']}. Calitate garantată, prețuri accesibile și personal calificat.")
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
