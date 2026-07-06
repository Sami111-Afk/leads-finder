# -*- coding: utf-8 -*-
import os
import re
import random
import json
import subprocess

LEADS = [
    # 1. Chirurgie Plastică
    {
        "niche": "chirurgie_plastica", "emoji": "🩺", "name": "Clinica Chirurgie Estetică Dr. Adrian Radu",
        "phone": "0723 111 888", "location": "Calea Dorobanți nr. 120, Sector 1, București",
        "program": "Luni - Vineri: 09:00 - 19:00 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Chirurgie estetică premium &", "slogan_part2": "tratamente estetice avansate",
        "desc_niche": "chirurgie plastică, estetică facială și remodelare corporală",
        "services": [
            {"icon": "🩺", "name": "Chirurgie Plastică & Reconstructivă", "desc": "Consultații și intervenții de blefaroplastie (corecție pleoape), otoplastie (corecție urechi) și lifting facial."},
            {"icon": "💉", "name": "Estetică Facială / Injectări", "desc": "Tratamente de injectare cu toxină botulinică pentru riduri și acid hialuronic pentru mărire buze sau volumizare pomeți."},
            {"icon": "🌟", "name": "Remodelare Corporală", "desc": "Consultații pre-operatorii pentru proceduri de lipoaspirație, augmentare mamară (implante silicon) sau abdominoplastie."}
        ],
        "image_url": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=600&q=80", "prefix": "estetica_"
    },
    {
        "niche": "chirurgie_plastica", "emoji": "🩺", "name": "Cabinet Chirurgie Plastică Dr. Elena Marin",
        "phone": "0744 222 999", "location": "Calea Moșilor nr. 256, Sector 2, București",
        "program": "Luni - Vineri: 09:30 - 18:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Frumusețe naturală cu", "slogan_part2": "tehnici chirurgicale moderne",
        "desc_niche": "chirurgie plastică-estetică, microchirurgie și injectări faciale",
        "services": [
            {"icon": "💉", "name": "Injectări Acid Hialuronic & Botox", "desc": "Estomparea ridurilor de expresie, remodelare mandibulă și hidratare profundă buze cu produse de top."},
            {"icon": "🩹", "name": "Chirurgie Dermatologică / Nevi", "desc": "Excizii chirurgicale cu examen histopatologic pentru alunițe, chisturi sebacee sau papiloame cu cicatrici minime."},
            {"icon": "✨", "name": "Terapia Vampir (PRP)", "desc": "Tratament de regenerare a pielii folosind plasma proprie a pacientului pentru riduri fine și elasticitate."}
        ],
        "image_url": "https://images.unsplash.com/photo-1579684389782-64d84b5e901d?auto=format&fit=crop&w=600&q=80", "prefix": "estetica_"
    },
    {
        "niche": "chirurgie_plastica", "emoji": "🩺", "name": "Estetic Clinic Dr. Mihai Popescu",
        "phone": "0722 333 555", "location": "Bulevardul Primăverii nr. 14, Sector 1, București",
        "program": "Luni - Vineri: 09:00 - 19:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Consultații chirurgie plastică",
        "slogan_part2": "tratamente faciale personalizate",
        "desc_niche": "cabinet medical de chirurgie estetică și tratamente rejuvenare",
        "services": [
            {"icon": "🩺", "name": "Lifting Facial Nechirurgical", "desc": "Tratamente de lifting cu fire resorbabile (PDO) pentru conturul feței și rejuvenare instantă."},
            {"icon": "🔬", "name": "Corecție Cearcăne & Acid", "desc": "Injectare de acid hialuronic special pentru zona delicată a cearcănelor, redând un aspect odihnit."},
            {"icon": "🩹", "name": "Tratament Cicatrici & Arsuri", "desc": "Proceduri medicale de corectare a cicatricilor post-acneice, post-operatorii sau post-arsură."}
        ],
        "image_url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=600&q=80", "prefix": "estetica_"
    },
    {
        "niche": "chirurgie_plastica", "emoji": "🩺", "name": "Consult Chirurgie Plastică Sector 3",
        "phone": "0761 444 999", "location": "Calea Dudești nr. 182, Sector 3, București",
        "program": "Luni - Vineri: 08:30 - 20:00 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Consultații estetică &", "slogan_part2": "intervenții chirurgicale mici",
        "desc_niche": "chirurgie plastică de cabinet, injectări estetice și pansamente",
        "services": [
            {"icon": "🩺", "name": "Consult & Recomandare chirurgicală", "desc": "Evaluări amănunțite pentru intervenții mari și stabilirea planului operator personalizat."},
            {"icon": "💉", "name": "Tratament Hiperhidroză (Botox)", "desc": "Injectare toxină botulinică în axilă, palme sau tălpi pentru combaterea transpirației excesive."},
            {"icon": "🩹", "name": "Tratament Unghie Încarnată Chirurgical", "desc": "Intervenție chirurgicală clasică (rezecție pană) cu anestezie locală pentru vindecarea definitivă."}
        ],
        "image_url": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=600&q=80", "prefix": "estetica_"
    },

    # 2. Servicii Întreținere Piscine
    {
        "niche": "intretinere_piscine", "emoji": "🏊", "name": "Smart Pool Service București",
        "phone": "0722 888 777", "location": "Bulevardul Pipera nr. 42, Voluntari, Ilfov",
        "program": "Luni - Sâmbătă: 08:00 - 19:00 | Duminică: Urgențe",
        "slogan_part1": "Întreținere piscine &", "slogan_part2": "tratamente chimice profesionale",
        "desc_niche": "întreținere piscine rezidențiale, curățare și echipamente piscine",
        "services": [
            {"icon": "🧼", "name": "Curățare Piscine Săptămânală", "desc": "Aspirare fund piscină, curățare linie apă, spălare filtre nisip și golire coșuri skimmer/pompă."},
            {"icon": "🧪", "name": "Tratare & Echilibrare Apă", "desc": "Analiză chimică a apei (pH, clor, alcalinitate) și dozarea precisă a chimicalelor pentru o apă cristal."},
            {"icon": "❄️", "name": "Pregătire Iernare / Primăvară", "desc": "Montare prelată iarnă, flotoare anti-îngheț, golire conducte și punere în funcțiune primăvara."}
        ],
        "image_url": "https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?auto=format&fit=crop&w=600&q=80", "prefix": "piscine_"
    },
    {
        "niche": "intretinere_piscine", "emoji": "🏊", "name": "Întreținere Piscine Rapid Andrei",
        "phone": "0764 111 999", "location": "Strada Principală nr. 92, Snagov, Ilfov",
        "program": "Luni - Duminică: 08:00 - 20:00",
        "slogan_part1": "Curățare piscine Snagov &",
        "slogan_part2": "reparații pompe și filtre",
        "desc_niche": "întreținere piscine, schimb nisip filtru și reparații pompe",
        "services": [
            {"icon": "🔧", "name": "Schimb Nisip / Sticlă Filtru", "desc": "Înlocuirea periodică a mediului filtrant (nisip cuarțos sau sticlă activă) pentru o filtrare optimă a apei."},
            {"icon": "🛠️", "name": "Reparații Pompe & Clorinatoare", "desc": "Remediere defecțiuni pompe filtrare, înlocuire garnituri, reparare sisteme de sare (electroliză)."},
            {"icon": "✨", "name": "Tratament Șoc anti-alge", "desc": "Tratamente rapide pentru eliminarea apei verzi din piscină, utilizând algicide și clor șoc."}
        ],
        "image_url": "https://images.unsplash.com/photo-1560185007-c5ca9d2c014d?auto=format&fit=crop&w=600&q=80", "prefix": "piscine_"
    },
    {
        "niche": "intretinere_piscine", "emoji": "🏊", "name": "Curățare Piscine Ilfov Marius",
        "phone": "0733 222 888", "location": "Strada Primăverii nr. 104, Corbeanca, Ilfov",
        "program": "Luni - Sâmbătă: 08:00 - 18:00 | Duminică: Închis",
        "slogan_part1": "Piscine curate &",
        "slogan_part2": "sisteme automatizate dozare",
        "desc_niche": "mentenanță piscine, montaj dozatoare automate și accesorii",
        "services": [
            {"icon": "🤖", "name": "Montaj Dozatoare Automate", "desc": "Instalare sisteme automate de măsurare și dozare a clorului și pH-ului pentru efort minim."},
            {"icon": "🌊", "name": "Detectare Pierderi Apă", "desc": "Identificarea fisurilor în conducte sau în linerul piscinei și reparații profesionale localizate."},
            {"icon": "💡", "name": "Montaj Proiectoare LED", "desc": "Înlocuire proiectoare halogene vechi cu sisteme moderne LED RGB cu control prin telecomandă."}
        ],
        "image_url": "https://images.unsplash.com/photo-1572331130797-3d05d27e8c04?auto=format&fit=crop&w=600&q=80", "prefix": "piscine_"
    },
    {
        "niche": "intretinere_piscine", "emoji": "🏊", "name": "Atelier Piscine & Chimicale Alex",
        "phone": "0765 333 999", "location": "Calea Bucureștilor nr. 82, Otopeni, Ilfov",
        "program": "Luni - Vineri: 09:00 - 18:00 | Sâmbătă: 09:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Echipamente piscine premium &",
        "slogan_part2": "livrare substanțe chimice",
        "desc_niche": "vânzare și montaj echipamente piscine și livrare chimicale la domiciliu",
        "services": [
            {"icon": "🚚", "name": "Livrare Substanțe Piscine", "desc": "Livrăm la domiciliu clor tablete multi-funcție, pH minus, antialge, floculant și sare specială."},
            {"icon": "🌊", "name": "Montaj Pompe Căldură", "desc": "Instalare pompe de căldură aer-apă pentru încălzirea apei și prelungirea sezonului de înot."},
            {"icon": "🛡️", "name": "Înlocuire Liner Piscine", "desc": "Demontare liner uzat și montaj liner nou armat termosudat de 1.5mm într-o varietate de culori."}
        ],
        "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=600&q=80", "prefix": "piscine_"
    },

    # 3. Centru Radiologie Dentară
    {
        "niche": "radiologie_dentara", "emoji": "🦴", "name": "Radiologie Dentară Dristor Mihai",
        "phone": "0722 121 555", "location": "Bulevardul Camil Ressu nr. 10, Sector 3, București",
        "program": "Luni - Vineri: 08:00 - 20:30 | Sâmbătă: 09:00 - 15:00 | Duminică: Închis",
        "slogan_part1": "Radiografii dentare 3D &",
        "slogan_part2": "tomografii computerizate CBCT",
        "desc_niche": "radiologie dentară digitală, radiografii panoramice și CBCT",
        "services": [
            {"icon": "🦷", "name": "Tomografii CBCT (3D)", "desc": "Tomografii dentare volumetrice 3D de înaltă rezoluție, esențiale pentru planificarea implantelor dentare."},
            {"icon": "🦴", "name": "Radiografii Panoramice (2D)", "desc": "Ortopantomograme (OPG) digitale cu doze minime de radiații, oferite pacienților pe loc pe CD, e-mail sau film."},
            {"icon": "📸", "name": "Radiografii Retroalveolare", "desc": "Radiografii intraorale mici de mare precizie pentru vizualizarea canalelor radiculare în timpul tratamentelor de canal."}
        ],
        "image_url": "https://images.unsplash.com/photo-1598256989800-fe5f95da9787?auto=format&fit=crop&w=600&q=80", "prefix": "radiologie_"
    },
    {
        "niche": "radiologie_dentara", "emoji": "🦴", "name": "Centru Radiografii Dentare 3D Sector 6",
        "phone": "0765 232 666", "location": "Bulevardul Iuliu Maniu nr. 45, Sector 6, București",
        "program": "Luni - Vineri: 08:30 - 20:00 | Sâmbătă: 09:00 - 16:00 | Duminică: Închis",
        "slogan_part1": "Radiologie dentară digitală",
        "slogan_part2": "doze minime radiații Sector 6",
        "desc_niche": "radiografii dentare ultra-rapide și tomografii maxilo-faciale",
        "services": [
            {"icon": "🦴", "name": "CBCT Maxilar / Mandibulă", "desc": "Scanare 3D de arcade individuale sau ambele maxilare cu aparatură de ultimă generație Sirona."},
            {"icon": "🦷", "name": "Radiografii Bite-Wing", "desc": "Radiografii interproximale speciale utilizate pentru depistarea cariilor ascunse între dinți în fază incipientă."},
            {"icon": "📡", "name": "Trimitere Digitală la Medic", "desc": "Trimitem rezultatele radiografiei instant pe e-mailul medicului dumneavoastră stomatolog pentru eficiență."}
        ],
        "image_url": "https://images.unsplash.com/photo-1445527815219-ecbfec67492e?auto=format&fit=crop&w=600&q=80", "prefix": "radiologie_"
    },
    {
        "niche": "radiologie_dentara", "emoji": "🦴", "name": "Art Dental X-Ray Sector 2",
        "phone": "0733 454 777", "location": "Strada Agricultori nr. 45, Sector 2, București",
        "program": "Luni - Vineri: 08:00 - 20:00 | Sâmbătă: 09:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Dosare ortodontice complete &",
        "slogan_part2": "teleradiografii de profil",
        "desc_niche": "radiologie ortodontică, teleradiografii și fotografii de diagnostic",
        "services": [
            {"icon": "📐", "name": "Teleradiografii de Profil (Cefalometrice)", "desc": "Radiografii craniene laterale esențiale pentru medicii ortodonți în vederea planificării aparatelor dentare."},
            {"icon": "📋", "name": "Dosar Ortodontic Complet", "desc": "Pachet complet: radiografie panoramică, teleradiografie, fotografii intraorale/extraorale și modele de studiu."},
            {"icon": "🦷", "name": "Radiografii Sinusuri Maxilare", "desc": "Investigație imagistică utilă înaintea intervențiilor de sinus lift sau pentru diagnosticarea sinuzitelor de origine dentară."}
        ],
        "image_url": "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?auto=format&fit=crop&w=600&q=80", "prefix": "radiologie_"
    },
    {
        "niche": "radiologie_dentara", "emoji": "🦴", "name": "Dental Imaging Premium Sector 4",
        "phone": "0765 565 888", "location": "Șoseaua Olteniței nr. 104, Sector 4, București",
        "program": "Luni - Vineri: 08:30 - 19:30 | Sâmbătă: 09:00 - 15:00 | Duminică: Închis",
        "slogan_part1": "Investigații radiologice dentare",
        "slogan_part2": "fără programare prealabilă",
        "desc_niche": "radiografii dentare pe loc, tomografii digitale și retroalveolare",
        "services": [
            {"icon": "🦷", "name": "Radiografie Panoramică pe Loc", "desc": "Efectuare radiografie în mai puțin de 5 minute, fără a fi nevoie de o programare în prealabil."},
            {"icon": "🦴", "name": "CBCT Articulație ATM", "desc": "Tomografii speciale pentru articulația temporo-mandibulară în caz de dureri, zgomote sau blocaje ale maxilarului."},
            {"icon": "🛡️", "name": "Protecție Guler & Șorț Plumb", "desc": "Garantăm siguranță maximă prin utilizarea echipamentelor speciale de protecție din plumb conform normelor CNCAN."}
        ],
        "image_url": "https://images.unsplash.com/photo-1606811971618-4486d14f3f99?auto=format&fit=crop&w=600&q=80", "prefix": "radiologie_"
    },

    # 4. Organizare Petreceri Copii
    {
        "niche": "petreceri_copii", "emoji": "🎈", "name": "Kids Party București Simona",
        "phone": "0722 444 111", "location": "Strada Viitorului nr. 22, Sector 2, București",
        "program": "Luni - Duminică: 09:00 - 21:00 (Petreceri la cerere)",
        "slogan_part1": "Petreceri copii de neuitat &",
        "slogan_part2": "animatori pictură pe față",
        "desc_niche": "organizare petreceri copii, animatori, baloane și spectacole",
        "services": [
            {"icon": "🦸", "name": "Animatori Profesioniști", "desc": "Supereroi, prințese Disney, clovni sau pirați care implică copiii în jocuri interactive, dansuri și concursuri."},
            {"icon": "🎨", "name": "Pictură pe Față & Baloane", "desc": "Pictură profesională pe față cu vopsele ecologice non-toxice pe bază de apă și modelaj de baloane (săbii, căței, flori)."},
            {"icon": "🎉", "name": "Mascote Disney Uriașe", "desc": "Apariție specială a mascotelor îndrăgite (Mickey, Minnie, Chase) pentru tort, fotografii de neuitat și dans."}
        ],
        "image_url": "https://images.unsplash.com/photo-1530103862676-de8c9debad1d?auto=format&fit=crop&w=600&q=80", "prefix": "petreceri_"
    },
    {
        "niche": "petreceri_copii", "emoji": "🎈", "name": "Atelierul de Animație Copii Alex",
        "phone": "0765 888 222", "location": "Calea Dorobanți nr. 56, Sector 1, București",
        "program": "Luni - Sâmbătă: 09:00 - 20:00 | Duminică: Petreceri",
        "slogan_part1": "Show-uri de magie &",
        "slogan_part2": "petreceri tematice copii",
        "desc_niche": "animație petreceri, spectacole de magie și ateliere creative",
        "services": [
            {"icon": "🧙", "name": "Spectacole Magie Copii", "desc": "Show-uri de magie interactive și amuzante realizate de magicieni profesioniști, cu trucuri vizuale și mult umor."},
            {"icon": "🧪", "name": "Ateliere Științifice/Creative", "desc": "Ateliere inedite de preparat slime, experimente cu gheață carbonică sau ateliere de pictură pe tricouri."},
            {"icon": "🫧", "name": "Show Baloane Uriașe Săpun", "desc": "Spectacol vizual uimitor cu baloane uriașe de săpun în care copiii pot fi introduși în interiorul unui balon gigant."}
        ],
        "image_url": "https://images.unsplash.com/photo-1513151233558-d860c5398176?auto=format&fit=crop&w=600&q=80", "prefix": "petreceri_"
    },
    {
        "niche": "petreceri_copii", "emoji": "🎈", "name": "Locul de Joacă Magic Sector 3",
        "phone": "0731 222 333", "location": "Strada Baba Novac nr. 12, Sector 3, București",
        "program": "Luni - Duminică: 10:00 - 21:00",
        "slogan_part1": "Închiriere loc de joacă",
        "slogan_part2": "pentru petreceri aniversare private",
        "desc_niche": "închiriere spațiu joacă copii, aniversări și evenimente copii",
        "services": [
            {"icon": "🏰", "name": "Închiriere Spațiu Exclusiv", "desc": "Închirierea integrală a locului de joacă pentru 3 ore, doar pentru invitații tăi, fără clienți externi în spațiu."},
            {"icon": "☕", "name": "Zonă Cafea & Relaxare Părinți", "desc": "Zonă confortabilă special amenajată pentru părinți cu acces la bar, Wi-Fi și vizibilitate completă asupra copiilor."},
            {"icon": "🍕", "name": "Pachete Pizza & Catering", "desc": "Asigurăm meniu cald (pizza copii, nuggets, cartofi prăjiți), suc natural, apă și tort aniversar la cerere."}
        ],
        "image_url": "https://images.unsplash.com/photo-1566737236500-c8ac43014a67?auto=format&fit=crop&w=600&q=80", "prefix": "petreceri_"
    },
    {
        "niche": "petreceri_copii", "emoji": "🎈", "name": "Petreceri Copii & Animatori Sector 6",
        "phone": "0764 777 444", "location": "Strada Apusului nr. 18, Sector 6, București",
        "program": "Luni - Duminică: 09:00 - 20:30",
        "slogan_part1": "Petreceri la cheie acasă",
        "slogan_part2": "sau la restaurant Sector 6",
        "desc_niche": "animatori petreceri, decor baloane și sonorizare petrecere",
        "services": [
            {"icon": "🏡", "name": "Petreceri la Domiciliu / Curte", "desc": "Venim cu toată logistica (sistem sunet, accesorii jocuri) acasă la tine, în grădină sau la restaurant."},
            {"icon": "🎈", "name": "Arcade & Panouri Baloane", "desc": "Decor decorativ cu baloane colorate, panou foto personalizat cu numele sărbătoritului și cifre uriașe LED."},
            {"icon": "🍿", "name": "Mașini Vată Zahăr / Popcorn", "desc": "Închiriere mașini profesionale de vată de zahăr pe băț sau popcorn cald preparat nelimitat pe durata petrecerii."}
        ],
        "image_url": "https://images.unsplash.com/photo-1547082299-de196ea013d6?auto=format&fit=crop&w=600&q=80", "prefix": "petreceri_"
    },

    # 5. Închirieri ATV & Agrement
    {
        "niche": "atv_agrement", "emoji": "🏍️", "name": "ATV Rent Snagov Mihai",
        "phone": "0722 990 440", "location": "Strada Principală nr. 240, Snagov, Ilfov",
        "program": "Luni - Duminică: 08:30 - 20:30",
        "slogan_part1": "Închirieri ATV-uri Snagov &",
        "slogan_part2": "trasee ghidate prin pădure",
        "desc_niche": "închirieri ATV, adventure tours și agrement Snagov",
        "services": [
            {"icon": "🏍️", "name": "Închirieri ATV Cfmoto 4x4", "desc": "Flotă de ATV-uri moderne Cfmoto de 450cc-600cc, automate, ideale pentru două persoane în siguranță."},
            {"icon": "🗺️", "name": "Trasee Ghidate Pădure", "desc": "Tururi organizate cu ghid prin pădurile din zona Snagov pe drumuri forestiere, ideale pentru începători și avansați."},
            {"icon": "🪖", "name": "Echipament Protecție inclus", "desc": "Oferim obligatoriu căști de protecție curate cu cagulă de unică folosință, ochelari off-road și instructaj complet."}
        ],
        "image_url": "https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=600&q=80", "prefix": "atv_"
    },
    {
        "niche": "atv_agrement", "emoji": "🏍️", "name": "Închirieri ATV Cernica Alex",
        "phone": "0764 888 666", "location": "Strada Principală nr. 48, Cernica, Ilfov",
        "program": "Luni - Duminică: 09:00 - 21:00",
        "slogan_part1": "Închiriere ATV Cernica",
        "slogan_part2": "adrenalină și distracție off-road",
        "desc_niche": "închirieri ATV, trasee off-road și team building-uri",
        "services": [
            {"icon": "🏍️", "name": "Închiriere ATV 1-3 Ore", "desc": "Închiriere ATV-uri puternice cu tarife pe oră avantajoase pentru explorarea drumurilor neasfaltate din zona Cernica."},
            {"icon": "🤝", "name": "Team Building & Grupuri", "desc": "Organizare evenimente corporate inedite de tip ATV adventure cu pauză de grătar în aer liber pentru echipe."},
            {"icon": "🛡️", "name": "Instruirea și Asistență Tehnică", "desc": "Garantăm asistență pe traseu în caz de blocare sau defecțiuni tehnice rapide din partea echipei noastre."}
        ],
        "image_url": "https://images.unsplash.com/photo-1508962914676-134849a727f0?auto=format&fit=crop&w=600&q=80", "prefix": "atv_"
    },
    {
        "niche": "atv_agrement", "emoji": "🌊", "name": "Jet Ski Rent Snagov Gabi",
        "phone": "0733 111 555", "location": "Strada Zorelelor nr. 12, Snagov, Ilfov",
        "program": "Luni - Duminică: 09:00 - 20:00 (În sezonul cald)",
        "slogan_part1": "Închirieri skijet Snagov &",
        "slogan_part2": "agrement nautic pe lac",
        "desc_niche": "închirieri jet ski (skijet), bărci și agrement pe lacul Snagov",
        "services": [
            {"icon": "🌊", "name": "Închirieri Skijet Sea-Doo", "desc": "Închiriere skijet-uri de ultimă generație Sea-Doo Spark/GTI, rapide și stabile pe suprafața apei."},
            {"icon": "🛟", "name": "Veste Salvare & Siguranță", "desc": "Fiecare închiriere include vestă de salvare omologată și instructaj complet privind regulile de navigație pe lac."},
            {"icon": "🚤", "name": "Plimbări cu Barca la Apus", "desc": "Închiriere barcă cu motor cu șofer pentru plimbări relaxante de grup pe lacul Snagov la apus."}
        ],
        "image_url": "https://images.unsplash.com/photo-1569263979104-865ab7cd8d13?auto=format&fit=crop&w=600&q=80", "prefix": "skijet_"
    },
    {
        "niche": "atv_agrement", "emoji": "🏍️", "name": "Adventure Rent Ilfov",
        "phone": "0765 222 666", "location": "Strada Florilor nr. 82, Bragadiru, Ilfov",
        "program": "Luni - Duminică: 08:00 - 21:00",
        "slogan_part1": "Închirieri ATV-uri & Buggy",
        "slogan_part2": "adventure park Ilfov",
        "desc_niche": "închirieri ATV, UTV (Buggy) și plimbări agrement off-road",
        "services": [
            {"icon": "🏎️", "name": "Închiriere UTV / Buggy", "desc": "Vehicule utilitare off-road (Buggy) cu centuri în 4 puncte și structură roll-cage, ideale pentru maxim de siguranță."},
            {"icon": "🏍️", "name": "Abonamente & Cadouri", "desc": "Vouchere cadou pentru plimbări cu ATV-ul pe care le poți oferi prietenilor pasionați de aventură și natură."},
            {"icon": "🌲", "name": "Trasee Pădure Bragadiru", "desc": "Plimbări liniștite prin zonele verzi și lizierele de pădure din Bragadiru și împrejurimi."}
        ],
        "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=600&q=80", "prefix": "atv_"
    },

    # 6. Curățătorie Chimică Haine
    {
        "niche": "curatatorie_chimica", "emoji": "👔", "name": "Clean Express Curățătorie Haine",
        "phone": "0723 555 333", "location": "Strada Viitorului nr. 102, Sector 2, București",
        "program": "Luni - Vineri: 08:30 - 20:00 | Sâmbătă: 09:00 - 15:00 | Duminică: Închis",
        "slogan_part1": "Curățare chimică ecologică &",
        "slogan_part2": "călcare profesională rapidă",
        "desc_niche": "curățătorie haine, curățare chimică costume și rochii de seară",
        "services": [
            {"icon": "👔", "name": "Curățare Costume & Cămăși", "desc": "Curățare chimică și călcare la dungă pentru costume bărbătești, sacouri, pantaloni și cămăși de birou."},
            {"icon": "👗", "name": "Curățare Rochii de Seară/Mireasă", "desc": "Curățare ecologică atentă pentru materiale sensibile (dantelă, mătase, mărgele) garantând protecția țesăturii."},
            {"icon": "🧥", "name": "Curățare Geci Puf & Paltoane", "desc": "Spălare specială geci cu puf de gâscă (re-expandare puf în uscător) și curățare paltoane din lână."}
        ],
        "image_url": "https://images.unsplash.com/photo-1545173168-9f18d8219979?auto=format&fit=crop&w=600&q=80", "prefix": "curatatorie_"
    },
    {
        "niche": "curatatorie_chimica", "emoji": "👔", "name": "Curățătorie Chimică Rapidă Andrei",
        "phone": "0744 666 444", "location": "Bulevardul Camil Ressu nr. 18, Sector 3, București",
        "program": "Luni - Sâmbătă: 08:00 - 21:00 | Duminică: Închis",
        "slogan_part1": "Curățătorie rapidă haine",
        "slogan_part2": "livrare la ușa ta București",
        "desc_niche": "curățătorie chimică haine, lenjerii pat și colectare domiciliu",
        "services": [
            {"icon": "🚚", "name": "Colectare & Livrare Domiciliu", "desc": "Preluăm hainele murdare de acasă și ți le aducem înapoi curățate, călcate pe umeraș în maxim 48 de ore."},
            {"icon": "🛏️", "name": "Spălare Lenjerii & Pături", "desc": "Spălare lenjerii de pat, pături groase, pilote din puf sau cuverturi de mari dimensiuni cu balsam parfumat."},
            {"icon": "⚡", "name": "Serviciu Express 24 Ore", "desc": "Ai un eveniment neprevăzut? Curățăm și călcăm costumul sau rochia ta în regim de urgență în doar 24 de ore."}
        ],
        "image_url": "https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?auto=format&fit=crop&w=600&q=80", "prefix": "curatatorie_"
    },
    {
        "niche": "curatatorie_chimica", "emoji": "👔", "name": "Eco Clean Curățătorie Sector 1",
        "phone": "0722 888 666", "location": "Calea Griviței nr. 142, Sector 1, București",
        "program": "Luni - Vineri: 09:00 - 19:30 | Sâmbătă: 09:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Curățătorie ecologică haine &",
        "slogan_part2": "curățare piele naturală cojoace",
        "desc_niche": "curățătorie ecologică wet-cleaning și curățare haine piele",
        "services": [
            {"icon": "🌿", "name": "Wet-Cleaning Ecologic", "desc": "Tehnologie modernă de curățare cu apă și detergenți biodegradabili, fără solvenți toxici (percloretilenă)."},
            {"icon": "🧥", "name": "Curățare Haine Piele & Cojoace", "desc": "Tratamente speciale de curățare, recondiționare culoare și hidratare pentru geci din piele naturală și cojoace."},
            {"icon": "🧺", "name": "Spălare Haine la Kilogram", "desc": "Serviciu economic pentru spălarea și uscarea hainelor de zi cu zi la sac (haine de bumbac, prosoape, tricouri)."}
        ],
        "image_url": "https://images.unsplash.com/photo-1489087895462-d52c5cddf7b9?auto=format&fit=crop&w=600&q=80", "prefix": "curatatorie_"
    },
    {
        "niche": "curatatorie_chimica", "emoji": "👔", "name": "Curățare Haine Ecologică Sector 4",
        "phone": "0761 222 111", "location": "Șoseaua Olteniței nr. 56, Sector 4, București",
        "program": "Luni - Vineri: 09:00 - 19:00 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Curățătorie haine la prețuri",
        "slogan_part2": "accesibile în Sectorul 4",
        "desc_niche": "spălătorie și curățătorie haine, călcare perdele și draperii",
        "services": [
            {"icon": "🧶", "name": "Curățare Perdele & Draperii", "desc": "Spălare și călcare profesională perdele fine și draperii grele de mari dimensiuni, cu eliminarea prafului."},
            {"icon": "👔", "name": "Călcat Profesional pe Umeraș", "desc": "Serviciu exclusiv de călcare haine (aduse deja spălate) cu prese de abur profesionale pentru un aspect impecabil."},
            {"icon": "🩹", "name": "Mici Retușuri Croitorie", "desc": "Scurtat pantaloni, înlocuit fermoare defecte sau nasturi lipsă în timp ce hainele sunt la curățat."}
        ],
        "image_url": "https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?auto=format&fit=crop&w=600&q=80", "prefix": "curatatorie_"
    },

    # 7. Cabinet Pediatrie Privată
    {
        "niche": "pediatrie_privata", "emoji": "👶", "name": "Cabinet Pediatrie Dr. Maria Popa",
        "phone": "0723 999 777", "location": "Strada Horei nr. 14, Sector 2, București",
        "program": "Luni - Vineri: 09:00 - 19:30 | Sâmbătă: 09:00 - 13:00 | Duminică: Închis",
        "slogan_part1": "Consultații pediatrie &",
        "slogan_part2": "monitorizare completă nou-născuți",
        "desc_niche": "pediatrie generală, ecografii sugari și sfaturi nutriție copii",
        "services": [
            {"icon": "👶", "name": "Consultații Pediatrie Generală", "desc": "Diagnosticare și tratament afecțiuni respiratorii, digestive, infecțioase sau alergice la copii de la 0 la 18 ani."},
            {"icon": "🍼", "name": "Monitorizare Sugari / Neonatologie", "desc": "Evaluarea creșterii și dezvoltării bebelușului, sfaturi alăptare, diversificare și scheme naționale de vaccinare."},
            {"icon": "🌡️", "name": "Consultații în regim de Urgență", "desc": "Programare rapidă în aceeași zi pentru episoade acute de febră, vărsături, erupții cutanate sau tuse severă."}
        ],
        "image_url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=600&q=80", "prefix": "pediatrie_"
    },
    {
        "niche": "pediatrie_privata", "emoji": "👶", "name": "Clinica Pediatrie Dr. Elena Georgescu",
        "phone": "0744 888 999", "location": "Calea Dorobanți nr. 82, Sector 1, București",
        "program": "Luni - Vineri: 09:00 - 19:00 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Sănătatea copilului tău",
        "slogan_part2": "cu medici pediatri cu experiență",
        "desc_niche": "pediatrie privată, ecografii pediatrice și sfaturi preventive",
        "services": [
            {"icon": "📟", "name": "Ecografie Șold Sugari", "desc": "Ecografie de screening pentru depistarea precoce a displaziei de șold la bebeluși de 4-12 săptămâni, non-invazivă."},
            {"icon": "🥗", "name": "Diverisificare & Nutriție Copii", "desc": "Consiliere nutrițională personalizată în etapele de diversificare sau pentru combaterea obezității infantile."},
            {"icon": "📝", "name": "Avize Medicale & Adeverințe", "desc": "Eliberare avize epidemiologice pentru intrarea în colectivitate (creșă, grădiniță, școală) și fișe de aptitudini."}
        ],
        "image_url": "https://images.unsplash.com/photo-1579684389782-64d84b5e901d?auto=format&fit=crop&w=600&q=80", "prefix": "pediatrie_"
    },
    {
        "niche": "pediatrie_privata", "emoji": "👶", "name": "Consult Pediatric Dr. Radu",
        "phone": "0722 666 888", "location": "Calea Dudești nr. 102, Sector 3, București",
        "program": "Luni - Vineri: 08:30 - 20:00 | Sâmbătă: 09:00 - 13:00 | Duminică: Închis",
        "slogan_part1": "Consultații copii rapide &",
        "slogan_part2": "ecografii abdominale pediatrice",
        "desc_niche": "cabinet medical de pediatrie, ecografie abdominală și monitorizare",
        "services": [
            {"icon": "📟", "name": "Ecografie Abdominală Copii", "desc": "Investigație ecografică completă a organelor abdominale la sugari și copii mari, complet nedureroasă."},
            {"icon": "🩺", "name": "Tratament Colici & Reflux", "desc": "Ghidaj medical pentru ameliorarea colicilor, refluxului gastro-esofagian și tulburărilor de tranzit la bebeluși."},
            {"icon": "🌡️", "name": "Tratamente Aerosoli & Inhalatoare", "desc": "Prescriere scheme tratament prin nebulizare pentru laringite, bronșiolite sau crize de astm pediatric."}
        ],
        "image_url": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=600&q=80", "prefix": "pediatrie_"
    },
    {
        "niche": "pediatrie_privata", "emoji": "👶", "name": "Pediatrie & Neonatologie Sector 4",
        "phone": "0761 333 999", "location": "Șoseaua Olteniței nr. 35, Sector 4, București",
        "program": "Luni - Vineri: 09:00 - 18:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Îngrijire dedicată sugari &",
        "slogan_part2": "consultații pediatrie Sector 4",
        "desc_niche": "cabinet pediatrie-neonatologie și suport alăptare",
        "services": [
            {"icon": "🍼", "name": "Consiliere Alăptare & Lactație", "desc": "Suport oferit proaspetelor mămici de către neonatolog pentru inițierea și menținerea alăptării corecte."},
            {"icon": "👶", "name": "Evaluare Neuro-Motorie Sugari", "desc": "Verificarea reflexelor neonatale și a etapelor de dezvoltare motorie (stat în șezut, mers de-a bușilea)."},
            {"icon": "🌡️", "name": "Diagnostic Boli Sezoniere", "desc": "Depistare rapidă gripă, VRS, COVID sau streptococ prin teste rapide de cabinet pe loc."}
        ],
        "image_url": "https://images.unsplash.com/photo-1530026405186-ed1ea0ac7a63?auto=format&fit=crop&w=600&q=80", "prefix": "pediatrie_"
    },

    # 8. Service Centrale Termice
    {
        "niche": "service_centrale", "emoji": "🔥", "name": "Centrale Termice Service Rapid",
        "phone": "0722 123 789", "location": "Strada Baba Novac nr. 12, Sector 3, București",
        "program": "Luni - Sâmbătă: 08:00 - 20:00 | Duminică: Urgențe Frig",
        "slogan_part1": "Reparații centrale termice &",
        "slogan_part2": "autorizări ISCIR rapide",
        "desc_niche": "service centrale termice gaz, verificări periodice și autorizări ISCIR",
        "services": [
            {"icon": "🔥", "name": "Reparații Centrale Gaz", "desc": "Diagnosticare și înlocuire piese defecte (pompe circulație, plăci electronice, schimbătoare căldură, senzori) pentru toate mărcile."},
            {"icon": "📜", "name": "Verificări Periodice VTP ISCIR", "desc": "Efectuarea verificării tehnice periodice obligatorii la 2 ani, eliberarea documentelor oficiale ISCIR pe loc."},
            {"icon": "💦", "name": "Spălare Chimică Schimbătoare", "desc": "Curățare cu acizi speciali a depunerilor de calcar din schimbătorul secundar sau principal pentru redarea randamentului."}
        ],
        "image_url": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=600&q=80", "prefix": "centrale_"
    },
    {
        "niche": "service_centrale", "emoji": "🔥", "name": "Reparații Centrale Termice Militari",
        "phone": "0765 987 321", "location": "Bulevardul Iuliu Maniu nr. 82, Sector 6, București",
        "program": "Luni - Duminică: 08:00 - 21:00 (Intervenții rapide)",
        "slogan_part1": "Service centrale pe gaz",
        "slogan_part2": "piese schimb originale în stoc",
        "desc_niche": "reparații centrale gaz, mentenanță cazane și spălări chimice",
        "services": [
            {"icon": "🔥", "name": "Intervenții Centrale Urgențe", "desc": "Repunere în funcțiune rapidă în caz de erori pe ecran, pierderi presiune apă, zgomote anormale sau lipsă apă caldă."},
            {"icon": "⚙️", "name": "Piese Originale în Stoc", "desc": "Deținem pe dubele de intervenție majoritatea pieselor uzuale (vane cu 3 căi, fluxostate, vase expansiune) pentru reparație pe loc."},
            {"icon": "💦", "name": "Curățare Filtre & Aerisire", "desc": "Verificarea filtrelor magnetice anti-magnetită, curățare filtre Y și aerisirea instalației de calorifere."}
        ],
        "image_url": "https://images.unsplash.com/photo-1581094288338-2314dddb7eed?auto=format&fit=crop&w=600&q=80", "prefix": "centrale_"
    },
    {
        "niche": "service_centrale", "emoji": "🔥", "name": "Atelier Centrale & Căldură Marius",
        "phone": "0733 112 444", "location": "Strada Agricultori nr. 78, Sector 2, București",
        "program": "Luni - Sâmbătă: 08:30 - 18:30 | Duminică: Închis",
        "slogan_part1": "Montaj centrale termice &",
        "slogan_part2": "verificări ISCIR Sector 2",
        "desc_niche": "montaj și service centrale termice, instalații termice",
        "services": [
            {"icon": "🔧", "name": "Montaj Centrale Termice", "desc": "Instalare și punere în funcțiune centrale murale pe gaz, realizare legături apă, gaz și evacuare coaxială."},
            {"icon": "📜", "name": "Autorizare Funcționare (AF ISCIR)", "desc": "Prima punere în funcțiune cu eliberare raport de analiză gaze arse și autorizație de funcționare ISCIR."},
            {"icon": "🌡️", "name": "Montaj Termostate Ambient", "desc": "Instalare termostate wireless smart sau cu fir (Honeywell, Computherm) pentru economisirea consumului de gaz."}
        ],
        "image_url": "https://images.unsplash.com/photo-1508514177221-188b1cf16e9d?auto=format&fit=crop&w=600&q=80", "prefix": "centrale_"
    },
    {
        "niche": "service_centrale", "emoji": "🔥", "name": "Service Centrale Gaz Sector 4",
        "phone": "0765 444 555", "location": "Șoseaua Olteniței nr. 102, Sector 4, București",
        "program": "Luni - Sâmbătă: 08:00 - 19:00 | Duminică: Închis",
        "slogan_part1": "Revizii anuale centrale gaz",
        "slogan_part2": "mentenanță preventivă Sector 4",
        "desc_niche": "revizii tehnice centrale gaz, spălare chimică și ISCIR",
        "services": [
            {"icon": "📋", "name": "Revizie Tehnică Anuală", "desc": "Curățare arzător, electrozi aprindere, verificare presiune aer în vasul de expansiune și analiză noxe."},
            {"icon": "💦", "name": "Curățare Chimică Instalație", "desc": "Curățare profesională a întregii instalații de încălzire (calorifere sau pardoseală) pentru eliminarea nămolului și ruginii."},
            {"icon": "🔥", "name": "Reparații Centrale Condensare", "desc": "Diagnosticare și curățare sifon condens, verificare schimbător aluminiu/inox la centralele noi în condensare."}
        ],
        "image_url": "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=600&q=80", "prefix": "centrale_"
    },

    # 9. Cabinet Urologie & Consult
    {
        "niche": "urologie_consult", "emoji": "🩺", "name": "Cabinet Urologie Dr. Adrian Popescu",
        "phone": "0723 112 333", "location": "Strada Viitorului nr. 104, Sector 2, București",
        "program": "Luni - Vineri: 09:00 - 19:00 | Sâmbătă: 09:00 - 13:00 | Duminică: Închis",
        "slogan_part1": "Consultații urologie &",
        "slogan_part2": "ecografii aparat urinar Doppler",
        "desc_niche": "urologie clinică, ecografie reno-vezico-prostatică și tratamente",
        "services": [
            {"icon": "🩺", "name": "Consultații Urologie", "desc": "Diagnosticare și tratament afecțiuni prostată (adenom de prostată, prostatită), infecții urinare repetate, disfuncții erectile."},
            {"icon": "📟", "name": "Ecografie Reno-Vezico-Prostatică", "desc": "Vizualizarea rinichilor, vezicii urinare și prostatei (transrectală sau transabdominală) de înaltă rezoluție."},
            {"icon": "🔬", "name": "Tratament Litiază Renală (Pietre)", "desc": "Diagnosticarea pietrelor la rinichi, recomandare tratamente de dizolvare sau trimiteri proceduri de spargere (ESWL)."}
        ],
        "image_url": "https://images.unsplash.com/photo-1579684389782-64d84b5e901d?auto=format&fit=crop&w=600&q=80", "prefix": "urologie_"
    },
    {
        "niche": "urologie_consult", "emoji": "🩺", "name": "Clinica Urologică Dr. Elena Rădulescu",
        "phone": "0744 223 444", "location": "Calea Dorobanți nr. 56, Sector 1, București",
        "program": "Luni - Vineri: 09:00 - 19:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Sănătate uro-genitală &",
        "slogan_part2": "screening cancer de prostată",
        "desc_niche": "urologie generală, ecografii transrectale și diagnostic precoce",
        "services": [
            {"icon": "🔍", "name": "Screening Cancer Prostată", "desc": "Palpare clinică, ecografie prostatică dedicată și recomandare testări PSA / Free PSA pentru prevenție."},
            {"icon": "🔬", "name": "Urologie Pediatrică / Fimoze", "desc": "Consultații urologice pentru copii mici, tratamente fimoze, sinechie prepuțială sau uretre malformate."},
            {"icon": "🩺", "name": "Diagnostic Incontinență Urinară", "desc": "Evaluarea pierderilor involuntare de urină la femei sau bărbați, tratament medicamentos și exerciții recuperatorii."}
        ],
        "image_url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=600&q=80", "prefix": "urologie_"
    },
    {
        "niche": "urologie_consult", "emoji": "🩺", "name": "Consult Urologic Sector 3 Mihai",
        "phone": "0722 334 555", "location": "Calea Dudești nr. 120, Sector 3, București",
        "program": "Luni - Vineri: 08:30 - 20:00 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Ecografie urologică rapidă &",
        "slogan_part2": "tratamente cistite infecții urinare",
        "desc_niche": "urologie clinică, ecografie abdominală și probe de laborator",
        "services": [
            {"icon": "📟", "name": "Ecografie Scrotală / Testiculară", "desc": "Investigație ecografică Doppler a testiculelor pentru depistarea varicocelului, chisturilor sau tumorilor."},
            {"icon": "🩺", "name": "Tratament Cistite Acute/Cronice", "desc": "Scheme terapeutice moderne pentru infecțiile urinare la femei, uroculturi ghidate de antibiogramă."},
            {"icon": "💊", "name": "Disfuncție Erectilă / Andrologie", "desc": "Evaluare hormonală și vasculară, consiliere și tratamente moderne pentru disfuncții erectile sau ejaculare precoce."}
        ],
        "image_url": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=600&q=80", "prefix": "urologie_"
    },
    {
        "niche": "urologie_consult", "emoji": "🩺", "name": "Urologie Medicală Sector 4",
        "phone": "0761 445 666", "location": "Șoseaua Olteniței nr. 82, Sector 4, București",
        "program": "Luni - Vineri: 09:00 - 18:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Consultații urologie &",
        "slogan_part2": "rețete compensate în Sectorul 4",
        "desc_niche": "cabinet urologie, ecografii aparat urinar și referate medicale",
        "services": [
            {"icon": "🩺", "name": "Control Urologic de Rutină", "desc": "Controlul anual recomandat tuturor bărbaților de peste 50 de ani pentru prevenirea adenomului de prostată."},
            {"icon": "📝", "name": "Referate comisie de expertiză", "desc": "Eliberare referate medicale urologice pentru dosare de pensie, comisie handicap sau asigurări private."},
            {"icon": "💊", "name": "Montare & Schimbare Sonde", "desc": "Servicii de montare, spălare sau schimbare a sondelor urinare (cateterism uretro-vezical) la cabinet sau la domiciliu."}
        ],
        "image_url": "https://images.unsplash.com/photo-1530026405186-ed1ea0ac7a63?auto=format&fit=crop&w=600&q=80", "prefix": "urologie_"
    },

    # 10. Sisteme Irigații & Gazon
    {
        "niche": "irigatii_gazon", "emoji": "🌱", "name": "Amenajări Gazon & Irigații București",
        "phone": "0722 990 550", "location": "Bulevardul Theodor Pallady nr. 48, Sector 3, București",
        "program": "Luni - Sâmbătă: 08:00 - 18:00 | Duminică: Închis",
        "slogan_part1": "Montaj sisteme irigații Hunter &",
        "slogan_part2": "rulouri gazon premium",
        "desc_niche": "amenajări grădini, montaj gazon rulou și sisteme de irigații automate",
        "services": [
            {"icon": "💦", "name": "Sisteme Irigații Automate", "desc": "Proiectare și montaj sisteme de irigație Hunter sau Rain Bird cu aspersoare telescopice, picurătoare și senzori de ploaie."},
            {"icon": "🌱", "name": "Montaj Gazon Rulou", "desc": "Pregătirea solului, frezare, nivelare, aplicare îngrășământ și montaj rulouri gazon din import pentru un gazon instant superb."},
            {"icon": "✂️", "name": "Însămânțare Gazon & Tundere", "desc": "Pregătirea solului, însămânțare gazon cu semințe premium rezistente la secetă și prima tundere/tăvălugire."}
        ],
        "image_url": "https://images.unsplash.com/photo-1558904541-efa8c3a30fc9?auto=format&fit=crop&w=600&q=80", "prefix": "gazon_"
    },
    {
        "niche": "irigatii_gazon", "emoji": "🌱", "name": "Sisteme Irigații Automate Otopeni",
        "phone": "0764 888 777", "location": "Strada Florilor nr. 12, Otopeni, Ilfov",
        "program": "Luni - Sâmbătă: 08:00 - 19:00 | Duminică: Închis",
        "slogan_part1": "Instalare sisteme irigații",
        "slogan_part2": "mentenanță gazon și curți Ilfov",
        "desc_niche": "sisteme de irigații inteligente, gazon și întreținere grădini",
        "services": [
            {"icon": "🤖", "name": "Irigații Smart Wifi", "desc": "Instalare programatoare de irigație conectate la Wifi (Landroid, Hydrawise) controlabile direct de pe telefonul mobil."},
            {"icon": "🔧", "name": "Pregătire Iarnă (Suflare Aer)", "desc": "Pregătirea sistemului de irigație pentru iarnă prin suflarea conductelor cu compresor de aer pentru a preveni înghețul."},
            {"icon": "🌿", "name": "Aerare & Scarificare Gazon", "desc": "Îndepărtarea uscăturilor din gazon (scarificare) și găurirea solului (aerare) pentru pătrunderea oxigenului și apei."}
        ],
        "image_url": "https://images.unsplash.com/photo-1592417817098-8f3d6eb19675?auto=format&fit=crop&w=600&q=80", "prefix": "gazon_"
    },
    {
        "niche": "irigatii_gazon", "emoji": "🌱", "name": "Montaj Rulouri Gazon Mihai",
        "phone": "0733 111 777", "location": "Strada Dezrobirii nr. 82, Sector 6, București",
        "program": "Luni - Sâmbătă: 08:00 - 18:00 | Duminică: Închis",
        "slogan_part1": "Amenajare curți cu rulouri",
        "slogan_part2": "gazon și irigații Sector 6",
        "desc_niche": "amenajare gazon, sisteme picurare și decopertare curte",
        "services": [
            {"icon": "🚜", "name": "Decopertare & Pregătire Sol", "desc": "Decopertarea pământului vechi sau buruienilor, adăugare pământ vegetal fertil, nivelare și tăvălugire profesională."},
            {"icon": "💦", "name": "Sisteme Picurare Gard Viu", "desc": "Montaj linii de picurare mascate pentru tuia, gard viu sau straturi de flori, cu consum minim de apă."},
            {"icon": "🩹", "name": "Reparații Aspersoare Spulberate", "desc": "Înlocuirea duzelor sparte de mașina de tuns gazonul, reglaj unghi stropire și înlocuire electrovalve."}
        ],
        "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=600&q=80", "prefix": "gazon_"
    },
    {
        "niche": "irigatii_gazon", "emoji": "🌱", "name": "Gazon & Irigații Premium Alex",
        "phone": "0765 222 777", "location": "Bulevardul Pipera nr. 120, Voluntari, Ilfov",
        "program": "Luni - Sâmbătă: 08:30 - 18:30 | Duminică: Închis",
        "slogan_part1": "Gazon perfect & sisteme",
        "slogan_part2": "irigații automate premium Pipera",
        "desc_niche": "amenajare gazon premium, sisteme inteligente de irigații și fertilizare",
        "services": [
            {"icon": "🌱", "name": "Gazon Rulou Sport/Umbră", "desc": "Montaj rulouri gazon rezistente la trafic intens (tip Sport) sau adaptate zonelor împădurite cu umbră (tip Umbră)."},
            {"icon": "💦", "name": "Mentenanță Sisteme Irigații", "desc": "Curățare filtre, reglaj aspersoare pentru acoperire 100% și verificări periodice ale senzorului de ploaie."},
            {"icon": "🧪", "name": "Tratamente Fertilizar & Epurare", "desc": "Aplicare îngrășăminte solide profesionale cu eliberare lentă și tratamente antifungice preventive."}
        ],
        "image_url": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&w=600&q=80", "prefix": "gazon_"
    }
]

PALETTES = {
    "chirurgie_plastica": {
        "primary": "#be185d", "rgb": "190, 24, 93", "secondary": "#1e1b4b", "bg": "#fdf2f8", "tag": "Clinică Chirurgie Plastică"
    },
    "intretinere_piscine": {
        "primary": "#06b6d4", "rgb": "6, 182, 212", "secondary": "#0f172a", "bg": "#ecfeff", "tag": "Servicii Întreținere Piscine"
    },
    "radiologie_dentara": {
        "primary": "#0ea5e9", "rgb": "14, 165, 233", "secondary": "#1e293b", "bg": "#f0f9ff", "tag": "Centru Radiologie Dentară"
    },
    "petreceri_copii": {
        "primary": "#f43f5e", "rgb": "244, 63, 94", "secondary": "#310d20", "bg": "#fff1f2", "tag": "Organizare Petreceri Copii"
    },
    "atv_agrement": {
        "primary": "#ea580c", "rgb": "234, 88, 12", "secondary": "#111827", "bg": "#fff7ed", "tag": "Închirieri ATV & Agrement"
    },
    "curatatorie_chimica": {
        "primary": "#0d9488", "rgb": "13, 148, 136", "secondary": "#0f172a", "bg": "#f0fdfa", "tag": "Curățătorie Chimică Haine"
    },
    "pediatrie_privata": {
        "primary": "#10b981", "rgb": "16, 185, 129", "secondary": "#064e3b", "bg": "#ecfdf5", "tag": "Cabinet Pediatrie Privată"
    },
    "service_centrale": {
        "primary": "#eab308", "rgb": "234, 179, 8", "secondary": "#1e293b", "bg": "#fefce8", "tag": "Service Centrale Termice"
    },
    "urologie_consult": {
        "primary": "#3b82f6", "rgb": "59, 130, 246", "secondary": "#1e1b4b", "bg": "#eff6ff", "tag": "Cabinet Urologie & Consult"
    },
    "irigatii_gazon": {
        "primary": "#16a34a", "rgb": "22, 163, 74", "secondary": "#14532d", "bg": "#f0fdf4", "tag": "Sisteme Irigații & Gazon"
    }
}

REVIEWS_TEMPLATES = {
    "chirurgie_plastica": [
        "Am ales clinica pentru o procedură de injectare buze cu acid hialuronic și rezultatul este extrem de natural! Domnul Dr. Radu lucrează impecabil. Recomand!",
        "Cabinet foarte cochet, curățenie exemplară și o atmosferă primitoare. Tratamentul cu Botox pentru riduri a dat roade în doar 5 zile. Minunat!",
        "Otoplastia efectuată de doamna Dr. Marin mi-a redat încrederea în mine. O echipă de profesioniști și o urmărire post-operatorie perfectă.",
        "Consultație chirurgie estetică detaliată. Mi-au fost explicate toate opțiunile, riscurile și pașii necesari pentru augmentare. Medic de încredere."
    ],
    "intretinere_piscine": [
        "De când colaborăm cu Smart Pool, apa piscinei noastre din Pipera este impecabilă. Sunt foarte serioși, punctuali și folosesc substanțe bune. Recomand!",
        "Curățarea săptămânală a piscinei este realizată foarte bine. Ne-au rezolvat rapid și o defecțiune la pompa de filtrare în plin sezon. Mulțumim!",
        "Servicii excelente de pregătire a piscinei pentru iarnă. Au venit cu toate materialele necesare, au golit conductele și au pus prelata în siguranță.",
        "Livrare rapidă de clor și sare direct la curtea noastră din Otopeni. Prețuri avantajoase și sfaturi bune pentru dozarea lor. Foarte mulțumit."
    ],
    "radiologie_dentara": [
        "Am realizat o tomografie 3D CBCT în acest centru din Dristor. Totul a fost gata în mai puțin de 10 minute și trimis instant pe mailul stomatologului. Recomand!",
        "Aparatură modernă Sirona și personal foarte amabil. Radiografia panoramică digitală s-a făcut cu doze foarte mici de radiații. Mulțumesc!",
        "Am primit dosarul ortodontic complet realizat impecabil (fotografii, teleradiografii și modele printate 3D). Servicii de radiologie de înaltă clasă.",
        "Nu este nevoie de programare prealabilă pentru radiografii retroalveolare sau panoramice. Se intră rapid, iar personalul este deosebit de atent."
    ],
    "petreceri_copii": [
        "Animatorii Simona au creat o petrecere de neuitat pentru ziua băiețelului nostru! Copiii au fost fascinați de supereroul preferat și jocurile propuse. Mulțumesc!",
        "Spectacolul de magie cu baloane uriașe de săpun a fost minunat! Toți copiii au participat activ și s-au distrat de minune. Servicii de nota 10 cu felicitări.",
        "Locul de joacă a fost închiriat exclusiv pentru noi. Spațiu curat, cafea bună pentru părinți și mâncare delicioasă pentru copii. Un eveniment foarte reușit.",
        "Venirea animatorilor la noi în curte, în Sectorul 6, a decurs impecabil. Au montat sistemul de sunet, au adus popcorn cald și au pictat toți copiii pe față."
    ],
    "atv_agrement": [
        "Plimbarea cu ATV-ulCFMOTO prin pădurea Snagov a fost o aventură de neuitat! Ghidul a fost foarte atent și ne-a dus pe trasee superbe. Recomand cu drag!",
        "ATV-uri puternice și bine întreținute, echipament de protecție complet inclus și o organizare ireproșabilă pentru team building-ul nostru. Foarte mulțumit!",
        "Închirierea de skijet la Snagov a fost senzațională. Apusul de pe lac și viteza pe apă au oferit o relaxare totală. Vom reveni cu mare plăcere.",
        "Adventure Rent din Bragadiru oferă cele mai distractive circuite off-road cu Buggy-uri. Siguranță deplină și adrenalină la maxim. Super experiență!"
    ],
    "curatatorie_chimica": [
        "Costumele mele bărbătești au fost curățate chimic și călcate la dungă perfect. Cămașa arată ca nouă și mirosul este discret și plăcut. Recomand!",
        "Rochia mea de mireasă fină din mătase a fost curățată ecologic impecabil, fără nicio deteriorare a dantelei. Servicii de wet-cleaning premium.",
        "Colectarea hainelor de la domiciliu ne-a salvat mult timp. Le-au luat murdare de acasă și le-au adus curate pe umeraș în 2 zile. Profesioniști!",
        "Curățătorie chimică excelentă în Sectorul 4. Prețuri foarte bune pe kilogram, perdelele au fost călcate impecabil și aduse la timp. Mulțumesc mult."
    ],
    "pediatrie_privata": [
        "Doamna Dr. Maria Popa este un pediatru extraordinar de calm și competent. Mi-a urmat bebelușul de la naștere și am primit mereu cele mai bune sfaturi.",
        "Consultația de urgență pentru febră a decurs rapid, fără timp de așteptare. Testele rapide de cabinet au identificat streptococul pe loc. Mulțumesc!",
        "Cabinet primitor, curățenie exemplară și ecografia de șold a fost realizată cu multă atenție și blândețe pentru cel mic. Recomand cu încredere!",
        "Sfaturi excelente primite din partea neonatologului pentru diversificare și suport alăptare. O clinică de pediatrie unde copiii merg fără frică."
    ],
    "service_centrale": [
        "Centrala noastră a intrat în eroare în plină iarnă. Echipa a sosit în 2 ore, a înlocuit pompa de circulație pe loc și a rezolvat problema. Serviciu rapid!",
        "Autorizarea ISCIR eliberată rapid și curățarea chimică a schimbătorului de caldură au redat randamentul centralei noastre. Preț corect și servicii bune.",
        "Montajul centralei noi pe gaz s-a realizat curat, conexiunile sunt etanșe și termostatul Wifi merge perfect. Experiență excelentă cu Marius!",
        "Revizia anuală a centralei în condensare a fost făcută profesionist. Analiza gazelor arse a fost făcută cu aparat special și totul este sigur. Recomand."
    ],
    "urologie_consult": [
        "Domnul Dr. Adrian Popescu este un medic urolog de un profesionalism desăvârșit. Mi-a explicat pe înțeles ecografia și tratamentul adenomului de prostată.",
        "Cabinet foarte discret și modern. Diagnosticarea litiazei renale și tratamentul prescris m-au ajutat să elimin pietrele fără operație. Mulțumesc!",
        "Consultație urologie rapidă în Sectorul 3. Ecografia scrotală a identificat rapid problema și schema de tratament a dat roade rapid. Foarte mulțumit.",
        "Recomand urologia din Sectorul 4. Schimbarea sondei urinare la domiciliu pentru bunicul meu a fost făcută cu mare grijă și igienă deplină."
    ],
    "irigatii_gazon": [
        "Sistemul automat de irigații Hunter funcționează perfect și acoperă fiecare colț al curții noastre. Rulourile de gazon montate arată ca un covor verde!",
        "Am ales programatorul irigații Wifi Hydrawise și pot controla stropirea gazonului direct de pe telefon în funcție de prognoza meteo. Foarte smart!",
        "Decopertarea pământului vechi și pregătirea riguroasă a solului au asigurat prinderea perfectă a rulourilor de gazon sport. O echipă de nota 10!",
        "Întreținerea irigațiilor și aerarea gazonului din Pipera au decurs foarte rapid. Duzele sparte au fost înlocuite și reglate corect. Profesioniști."
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
    
    niche_templates = REVIEWS_TEMPLATES.get(niche, REVIEWS_TEMPLATES["irigatii_gazon"])
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
        num = 541 + idx
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
        html_content = html_content.replace("__DESC__", f"Servicii profesionale de {item['desc_niche']} în {item['location']}. Calitate premium, echipamente de ultimă generație și satisfacție garantată.")
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
