# -*- coding: utf-8 -*-
import os
import re
import random
import json
import subprocess

LEADS = [
    {
        "niche": "panouri_fotovoltaice",
        "emoji": "☀️",
        "name": "Smart Solar Solutions București",
        "phone": "0722 990 110",
        "location": "Calea Rahovei nr. 266, Sector 5, București",
        "program": "Luni - Vineri: 08:30 - 18:30 | Sâmbătă: 09:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Sisteme fotovoltaice premium &",
        "slogan_part2": "independență energetică",
        "desc_niche": "proiectare, instalare și avizare sisteme panouri fotovoltaice",
        "services": [
            {"icon": "☀️", "name": "Instalare Panouri Fotovoltaice", "desc": "Montaj sisteme fotovoltaice on-grid, off-grid și hybrid cu panouri monocristaline de înaltă eficiență și invertoare premium (Huawei, Fronius)."},
            {"icon": "🔋", "name": "Sisteme Stocare / Baterii", "desc": "Integrare acumulatori LFP (Litiu Fier Fosfat) pentru stocarea energiei solare și utilizarea ei pe timpul nopții sau în caz de avarie."},
            {"icon": "📝", "name": "Dosar Prosumator & Avize", "desc": "Întocmirea completă a documentației tehnice pentru obținerea statutului de prosumator și conectarea sistemului la rețeaua națională."}
        ],
        "image_url": "https://images.unsplash.com/photo-1508514177221-188b1cf16e9d?auto=format&fit=crop&w=600&q=80",
        "prefix": "panouri_fotovoltaice_"
    },
    {
        "niche": "panouri_fotovoltaice",
        "emoji": "⚡",
        "name": "Eco Volt Systems Otopeni",
        "phone": "0764 888 333",
        "location": "Calea Bucureștilor nr. 89, Otopeni, Ilfov",
        "program": "Luni - Vineri: 08:00 - 18:00 | Sâmbătă: 09:00 - 15:00 | Duminică: Închis",
        "slogan_part1": "Pompe de căldură &",
        "slogan_part2": "panouri solare Ilfov",
        "desc_niche": "energii regenerabile, panouri fotovoltaice și pompe de căldură",
        "services": [
            {"icon": "🔥", "name": "Instalare Pompe de Căldură", "desc": "Montaj pompe de căldură aer-apă sau sol-apă pentru încălzire eficientă și apă caldă menajeră cu consum minim."},
            {"icon": "⚡", "name": "Sisteme Hybrid Smart", "desc": "Configurare sisteme inteligente care combină energia solară cu pompa de căldură pentru maximizarea autoconsumului."},
            {"icon": "🛠️", "name": "Mentenanță & Verificări", "desc": "Curățare profesională panouri, măsurători parametrii invertor, verificări conexiuni electrice și diagnosticări periodice."}
        ],
        "image_url": "https://images.unsplash.com/photo-1509391366360-2e959784a276?auto=format&fit=crop&w=600&q=80",
        "prefix": "panouri_fotovoltaice_"
    },
    {
        "niche": "panouri_fotovoltaice",
        "emoji": "🔌",
        "name": "Solar Energy Install Mihai",
        "phone": "0733 111 222",
        "location": "Strada Dezrobirii nr. 45, Sector 6, București",
        "program": "Luni - Sâmbătă: 08:00 - 19:00 | Duminică: Închis",
        "slogan_part1": "Panouri fotovoltaice la cheie",
        "slogan_part2": "în București & Ilfov",
        "desc_niche": "montaj panouri fotovoltaice și stații de încărcare mașini electrice",
        "services": [
            {"icon": "🏠", "name": "Montaj pe Acoperișuri", "desc": "Instalare structuri de aluminiu specifice pentru țiglă metalică, ceramică, tablă cutată sau terase plane în siguranță."},
            {"icon": "🚗", "name": "Stații Încărcare Auto", "desc": "Montaj stații de încărcare rapide pentru mașini electrice (EV Chargers) conectate direct la sistemul tău solar."},
            {"icon": "🔧", "name": "Cablare & Automatizări", "desc": "Realizare tablouri de curent continuu/alternativ (DC/AC), siguranțe de protecție, descărcătoare și punere în funcțiune."}
        ],
        "image_url": "https://images.unsplash.com/photo-1613665813446-82a78c468a1d?auto=format&fit=crop&w=600&q=80",
        "prefix": "panouri_fotovoltaice_"
    },
    {
        "niche": "panouri_fotovoltaice",
        "emoji": "🔋",
        "name": "Green Power Systems Alex",
        "phone": "0765 222 333",
        "location": "Bulevardul Metalurgiei nr. 82, Sector 4, București",
        "program": "Luni - Sâmbătă: 08:30 - 18:30 | Duminică: Închis",
        "slogan_part1": "Facturi zero cu energie",
        "slogan_part2": "verde din soare",
        "desc_niche": "instalații panouri fotovoltaice, invertoare și stocare energie",
        "services": [
            {"icon": "☀️", "name": "Sisteme Fotovoltaice 5kW - 30kW", "desc": "Proiectare și dimensionare personalizată a sistemului în funcție de consumul mediu lunar al casei tale."},
            {"icon": "📡", "name": "Monitorizare Online Smart", "desc": "Configurare aplicații mobile pentru monitorizarea în timp real a producției solare și a consumului locuinței."},
            {"icon": "🛡️", "name": "Garanție & Suport Tehnic", "desc": "Oferim garanție completă pentru montaj, service rapid în caz de erori ale invertorului și suport tehnic dedicat."}
        ],
        "image_url": "https://images.unsplash.com/photo-1548613053-22087dd8edb8?auto=format&fit=crop&w=600&q=80",
        "prefix": "panouri_fotovoltaice_"
    },
    {
        "niche": "ginecologie",
        "emoji": "🩺",
        "name": "Cabinet Ginecologie Dr. Maria Ionescu",
        "phone": "0723 444 888",
        "location": "Bulevardul Carol I nr. 45, Sector 2, București",
        "program": "Luni - Vineri: 09:00 - 19:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Consultații ginecologice &",
        "slogan_part2": "ecografii 3D/4D de specialitate",
        "desc_niche": "consultații obstetrică-ginecologie, ecografii de sarcină și analize de prevenție",
        "services": [
            {"icon": "🩺", "name": "Consultații Ginecologie", "desc": "Examinări clinice de rutină, diagnosticare și tratament afecțiuni ginecologice, recomandări contracepție și tratamente menopauză."},
            {"icon": "🤰", "name": "Monitorizare Sarcină (Obstetrică)", "desc": "Urmărirea evoluției sarcinii trimestru cu trimestru, ecografii morfologice, monitorizare bătăi inimă făt și sfaturi prenatale."},
            {"icon": "🔬", "name": "Test Babeș-Papanicolau & HPV", "desc": "Recoltare analize de prevenție cancer de col uterin, genotipare HPV și interpretare rezultate cu scheme tratament."}
        ],
        "image_url": "https://images.unsplash.com/photo-1579684389782-64d84b5e901d?auto=format&fit=crop&w=600&q=80",
        "prefix": "ginecologie_"
    },
    {
        "niche": "ginecologie",
        "emoji": "⚕️",
        "name": "Clinica Ginecologie Dr. Elena Marin",
        "phone": "0744 555 999",
        "location": "Strada Paris nr. 12, Sector 1, București",
        "program": "Luni - Vineri: 09:00 - 19:00 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Sănătatea femeii pe primul",
        "slogan_part2": "loc cu medici dedicați",
        "desc_niche": "ginecologie clinică, senologie și planning familial",
        "services": [
            {"icon": "🤰", "name": "Ecografie Transvaginală & Pelvină", "desc": "Investigații ecografice de înaltă rezoluție pentru vizualizarea uterului, ovarelor și depistarea chisturilor sau fibroamelor."},
            {"icon": "🎀", "name": "Ecografie Mamară & Senologie", "desc": "Examinări ecografice mamare și palpare clinică pentru depistarea precoce a nodulilor mamari și recomandări preventive."},
            {"icon": "💊", "name": "Planning Familial & Sterilet", "desc": "Consiliere planning familial, prescriere contraceptive potrivite și montare/extragere dispozitive intrauterine (sterilet)."}
        ],
        "image_url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=600&q=80",
        "prefix": "ginecologie_"
    },
    {
        "niche": "ginecologie",
        "emoji": "🏥",
        "name": "Cabinet Obstetrică Ginecologie Dr. Rădulescu",
        "phone": "0722 777 444",
        "location": "Calea Dudești nr. 104, Sector 3, București",
        "program": "Luni - Vineri: 08:30 - 20:00 | Sâmbătă: 09:00 - 13:00 | Duminică: Închis",
        "slogan_part1": "Consultații ginecologie &",
        "slogan_part2": "monitorizare completă sarcină",
        "desc_niche": "cabinet de ginecologie, ecografii ginecologice și monitorizări prenatale",
        "services": [
            {"icon": "🔬", "name": "Analize Ginecologice & Secreții", "desc": "Recoltare culturi col, secreții vaginale, teste pentru infecții cu transmitere sexuală și interpretare analize microbiologie."},
            {"icon": "👶", "name": "Ecografie de Sarcină 3D/4D", "desc": "Vizualizarea în timp real a fătului în format 3D/4D, înregistrări video și fotografii pentru viitorii părinți."},
            {"icon": "🩺", "name": "Tratament Tulburări Menstruale", "desc": "Diagnosticarea dezechilibrelor hormonale, chisturi ovariene, dismenoree, menopauză prematură și tratamente personalizate."}
        ],
        "image_url": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=600&q=80",
        "prefix": "ginecologie_"
    },
    {
        "niche": "ginecologie",
        "emoji": "🩺",
        "name": "Consult Ginecologic Dr. Popescu",
        "phone": "0761 112 233",
        "location": "Șoseaua Olteniței nr. 14, Sector 4, București",
        "program": "Luni - Vineri: 09:00 - 18:30 | Sâmbătă - Duminică: Închis",
        "slogan_part1": "Consultații ginecologie &",
        "slogan_part2": "ecografii rapide sector 4",
        "desc_niche": "cabinet medical de ginecologie, ecografii de rutină și prevenție medicală",
        "services": [
            {"icon": "🩺", "name": "Control Ginecologic de Rutină", "desc": "Examinare clinică anuală recomandată pentru menținerea stării de sănătate a aparatului genital feminin."},
            {"icon": "🔬", "name": "Diagnosticare Răni pe Col", "desc": "Colposcopie, depistarea leziunilor precanceroase de pe col și stabilirea planului terapeutic minim-invaziv."},
            {"icon": "💖", "name": "Consiliere Preconcepțională", "desc": "Evaluări medicale amănunțite și analize recomandate cuplurilor care își doresc o sarcină în viitorul apropiat."}
        ],
        "image_url": "https://images.unsplash.com/photo-1530026405186-ed1ea0ac7a63?auto=format&fit=crop&w=600&q=80",
        "prefix": "ginecologie_"
    },
    {
        "niche": "cazare_pensiuni",
        "emoji": "🏡",
        "name": "Pensiunea Green Oasis Cernica",
        "phone": "0722 888 999",
        "location": "Strada Principală nr. 42, Cernica, Ilfov",
        "program": "Luni - Duminică: Recepție Non-Stop (24/7)",
        "slogan_part1": "Cazare în natură lângă lacul",
        "slogan_part2": "Cernica în oază de liniște",
        "desc_niche": "servicii de cazare, pensiune turistică și organizări mici evenimente în natură",
        "services": [
            {"icon": "🛌", "name": "Camere Duble & Apartamente", "desc": "Cazare în camere spațioase dotate cu baie proprie, aer condiționat, balcon cu vedere spre pădure sau lac și Wi-Fi gratuit."},
            {"icon": "🌳", "name": "Grădină Generoasă & Foișoare", "desc": "Acces liber în curtea imensă cu spații verzi amenajate, foișoare pentru grătar, zonă de relaxare și loc de joacă copii."},
            {"icon": "🍳", "name": "Mic Dejun Inclus & Restaurant", "desc": "Mic dejun tradițional proaspăt inclus în prețul cazării și posibilitatea de a comanda prânzul sau cina la cerere."}
        ],
        "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=600&q=80",
        "prefix": "cazare_pensiuni_"
    },
    {
        "niche": "cazare_pensiuni",
        "emoji": "🪵",
        "name": "Cabana Rustică Snagov",
        "phone": "0745 222 111",
        "location": "Strada Zorelelor nr. 15, Snagov, Ilfov",
        "program": "Luni - Duminică: Recepție 08:00 - 22:00",
        "slogan_part1": "Cabana din bușteni Snagov",
        "slogan_part2": "pentru weekenduri relaxante",
        "desc_niche": "cazare rustică din lemn, închiriere integrală cabană și relaxare în Snagov",
        "services": [
            {"icon": "🪵", "name": "Închiriere Integrală Cabană", "desc": "Cabană din bușteni de lemn masiv cu 5 dormitoare duble, living generos cu șemineu cu lemne și bucătărie complet utilată."},
            {"icon": "🪵", "name": "Ciubăr Exterior Încălzit", "desc": "Relaxare în ciubăr mare din lemn cu apă sărată încălzită la 38-40 de grade, disponibil pe tot parcursul anului."},
            {"icon": "🛶", "name": "Acces Lac & Plimbări Kayak", "desc": "Acces direct la pontonul privat de pe malul lacului Snagov și plimbări gratuite cu kayak-ul pentru oaspeții noștri."}
        ],
        "image_url": "https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=600&q=80",
        "prefix": "cazare_pensiuni_"
    },
    {
        "niche": "cazare_pensiuni",
        "emoji": "⛺",
        "name": "Glamping Premium Ilfov",
        "phone": "0763 444 555",
        "location": "Strada Florilor nr. 82, Bragadiru, Ilfov",
        "program": "Luni - Duminică: Recepție 09:00 - 21:00",
        "slogan_part1": "Experiență de camping luxos",
        "slogan_part2": "glamping premium lângă pădure",
        "desc_niche": "cazare in corturi glamping de lux încălzite, cu terase și jacuzzi exterior",
        "services": [
            {"icon": "⛺", "name": "Corturi Glamping de Lux", "desc": "Corturi spațioase de tip dome geo-desic cu pat king-size, încălzire electrică pentru nopți răcoroase și podea din lemn."},
            {"icon": "🛀", "name": "Jacuzzi Exterior Privat", "desc": "Fiecare cort beneficiază de un jacuzzi exterior privat pe terasă pentru momente unice de relaxare sub stele."},
            {"icon": "🔥", "name": "Zonă de Foc de Tabără", "desc": "Zonă special amenajată în centrul complexului pentru foc de tabără, socializare și preparat bezele coapte seara."}
        ],
        "image_url": "https://images.unsplash.com/photo-1470246973918-29a93221c455?auto=format&fit=crop&w=600&q=80",
        "prefix": "cazare_pensiuni_"
    },
    {
        "niche": "cazare_pensiuni",
        "emoji": "🏡",
        "name": "Pensiunea Eden Corbeanca",
        "phone": "0731 555 666",
        "location": "Strada Primăverii nr. 122, Corbeanca, Ilfov",
        "program": "Luni - Duminică: Recepție Non-Stop (24/7)",
        "slogan_part1": "Cazare elegantă în camere",
        "slogan_part2": "premium liniște în Corbeanca",
        "desc_niche": "cazare pensiune turistică, piscină exterioară și grădină amenajată",
        "services": [
            {"icon": "🏊", "name": "Piscină Exterioară în Sezon", "desc": "Acces gratuit la piscina noastră exterioară cu șezlonguri, umbrele și bar în curte pe timpul verii."},
            {"icon": "🛌", "name": "Camere Standard & Deluxe", "desc": "Opțiuni de cazare în camere duble standard sau camere deluxe cu cadă cu hidromasaj și balcoane mari."},
            {"icon": "🚗", "name": "Parcare Privată Supravegheată", "desc": "Parcare gratuită securizată în interiorul curții noastre, supravegheată video 24/7 pentru siguranța mașinii tale."}
        ],
        "image_url": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=600&q=80",
        "prefix": "cazare_pensiuni_"
    },
    {
        "niche": "sali_box_fitness",
        "emoji": "🥊",
        "name": "Sală Box Kickbox Sector 6 Alex",
        "phone": "0764 990 011",
        "location": "Aleea Callatis nr. 10, Sector 6, București",
        "program": "Luni - Vineri: 07:00 - 22:00 | Sâmbătă: 09:00 - 15:00 | Duminică: Închis",
        "slogan_part1": "Antrenamente de box &",
        "slogan_part2": "kickbox pentru toate nivelurile",
        "desc_niche": "club sportiv specializat în box, kickboxing și antrenamente de autoapărare",
        "services": [
            {"icon": "🥊", "name": "Antrenamente Box Adulți & Copii", "desc": "Inițiere și perfecționare în box: tehnici de lovire, deplasare în ring, eschive, antrenamente la sac și sparring controlat."},
            {"icon": "💥", "name": "Ședințe Kickbox & K1", "desc": "Antrenamente dinamice care combină loviturile de brațe și picioare, ideale pentru autoapărare și tonifiere rapidă."},
            {"icon": "🔥", "name": "Pregătire Fizică / Condiționare", "desc": "Circuite intense de cardio și forță pentru creșterea rezistenței, flexibilității, coordonării și pierderea în greutate."}
        ],
        "image_url": "https://images.unsplash.com/photo-1599058917212-d750089bc07e?auto=format&fit=crop&w=600&q=80",
        "prefix": "sali_box_fitness_"
    },
    {
        "niche": "sali_box_fitness",
        "emoji": "🥊",
        "name": "Boxing Club Dristor Mihai",
        "phone": "0722 444 333",
        "location": "Bulevardul Camil Ressu nr. 12, Sector 3, București",
        "program": "Luni - Vineri: 08:00 - 21:30 | Sâmbătă: 10:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Învață arta boxului cu",
        "slogan_part2": "antrenori cu experiență",
        "desc_niche": "sală de box clasic, antrenamente de grup și ședințe private",
        "services": [
            {"icon": "🥊", "name": "Grupe Box Începători / Avansați", "desc": "Antrenamente de grup structurate pentru învățarea corectă a elementelor de bază din box sau perfecționare tehnică."},
            {"icon": "🤝", "name": "Antrenamente Private 1-la-1", "desc": "Ședințe individuale cu antrenor dedicat pentru corectare rapidă a posturii, tehnicii și pregătire fizică personalizată."},
            {"icon": "🏋️", "name": "Zona Fitness & Sacii de Box", "desc": "Acces liber la zona de saci de box, gantere, funii de antrenament și aparate cardio în afara orelor de grup."}
        ],
        "image_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=600&q=80",
        "prefix": "sali_box_fitness_"
    },
    {
        "niche": "sali_box_fitness",
        "emoji": "🥊",
        "name": "Fight Club Titan",
        "phone": "0733 555 777",
        "location": "Strada Liviu Rebreanu nr. 18, Sector 3, București",
        "program": "Luni - Vineri: 07:30 - 22:00 | Sâmbătă: 09:00 - 16:00 | Duminică: Închis",
        "slogan_part1": "Fight Club &",
        "slogan_part2": "programe fitness intense",
        "desc_niche": "club de lupte, arte marțiale, kickbox și antrenamente funcționale",
        "services": [
            {"icon": "🥋", "name": "Kickbox & Autoapărare", "desc": "Cursuri axate pe tehnici practice de autoapărare și combat sport în deplină siguranță pentru cursanți."},
            {"icon": "🥊", "name": "Kickboxing / Fitbox Femei", "desc": "Antrenamente dinamice la sacii de box combinate cu exerciții funcționale destinate doamnelor, axate pe tonifiere."},
            {"icon": "🤸", "name": "Box Copii & Auto-Disciplină", "desc": "Cursuri speciale pentru copii: dezvoltare motorie, coordonare, creșterea încrederii în sine și auto-disciplină."}
        ],
        "image_url": "https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?auto=format&fit=crop&w=600&q=80",
        "prefix": "sali_box_fitness_"
    },
    {
        "niche": "sali_box_fitness",
        "emoji": "🏋️",
        "name": "Personal Trainer Gabriel Rusu",
        "phone": "0761 222 888",
        "location": "Strada Horei nr. 10, Sector 2, București",
        "program": "Luni - Vineri: 06:00 - 21:00 | Sâmbătă: 08:00 - 14:00 | Duminică: Închis",
        "slogan_part1": "Antrenor personal &",
        "slogan_part2": "planuri nutriționale personalizate",
        "desc_niche": "servicii de personal training, slăbire, tonifiere și nutriție",
        "services": [
            {"icon": "🏋️", "name": "Personal Training 1-la-1", "desc": "Antrenamente programate după obiectivele tale (slăbire, hipertrofie, rezistență), monitorizate de antrenor atestat."},
            {"icon": "🥗", "name": "Plan Nutrițional Personalizat", "desc": "Calcul macronutrienți, planuri alimentare ușor de urmat fără înfometare, adaptate stilului tău de viață."},
            {"icon": "📉", "name": "Monitorizare Progres & Măsurători", "desc": "Măsurători corporale periodice, monitorizare evoluție greutate și ajustarea programului de exerciții."},
        ],
        "image_url": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?auto=format&fit=crop&w=600&q=80",
        "prefix": "sali_box_fitness_"
    },
    {
        "niche": "pergole_foisoare",
        "emoji": "🪵",
        "name": "Atelier Pergole Lemn București",
        "phone": "0783 111 222",
        "location": "Strada Zeicani nr. 8, Sector 5, București",
        "program": "Luni - Sâmbătă: 08:00 - 18:00 | Duminică: Închis",
        "slogan_part1": "Pergole din lemn &",
        "slogan_part2": "terase din lemn la comandă",
        "desc_niche": "atelier de dulgherie specializat în pergole auto, terase și copertine din lemn",
        "services": [
            {"icon": "🪵", "name": "Pergole & Copertine Lemn", "desc": "Executăm pergole din lemn lamelar încleiat (stratificat) sau lemn masiv tratat pentru protecție mașină sau umbrire terase."},
            {"icon": "🏡", "name": "Amenajări Terase Lemn", "desc": "Construcții de podele exterioare din lemn (decking din pin termotratat sau compozit WPC) și balustrade rustice."},
            {"icon": "🛡️", "name": "Tratamente Lemn & Lăcuiri", "desc": "Șlefuire profesională, tratamente ignifuge, antifungice, împotriva dăunătorilor și finisaje cu lacuri rezistente la razele UV."}
        ],
        "image_url": "https://images.unsplash.com/photo-1560185007-cde436f6a4d0?auto=format&fit=crop&w=600&q=80",
        "prefix": "pergole_foisoare_"
    },
    {
        "niche": "pergole_foisoare",
        "emoji": "🏡",
        "name": "Foișoare Terase Custom Marius",
        "phone": "0765 444 888",
        "location": "Strada Primăverii nr. 48, Bragadiru, Ilfov",
        "program": "Luni - Sâmbătă: 08:00 - 19:00 | Duminică: Închis",
        "slogan_part1": "Foișoare de grădină &",
        "slogan_part2": "terase din lemn stratificat",
        "desc_niche": "execuție foișoare lemn, pergole bioclimatice sau rustice și terase",
        "services": [
            {"icon": "🏡", "name": "Foișoare de Grădină Custom", "desc": "Realizare foișoare hexagonale, pătrate sau dreptunghiulare din lemn stratificat, echipate cu acoperiș din șindrilă bituminoasă."},
            {"icon": "📐", "name": "Proiectare & Măsurători Gratuite", "desc": "Ne deplasăm la adresa ta în București/Ilfov pentru stabilirea cotelor exacte, tipului de structură și calcul de deviz gratuit."},
            {"icon": "🚪", "name": "Închideri Terase / Sticlă", "desc": "Montaj sisteme de închidere terase cu folie transparentă sau sticlă glisantă pentru utilizarea spațiului în sezonul rece."}
        ],
        "image_url": "https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=600&q=80",
        "prefix": "pergole_foisoare_"
    },
    {
        "niche": "pergole_foisoare",
        "emoji": "🪵",
        "name": "Amenajări Terase Lemn Alex",
        "phone": "0722 333 444",
        "location": "Strada Agricultori nr. 78, Sector 2, București",
        "program": "Luni - Sâmbătă: 08:30 - 18:30 | Duminică: Închis",
        "slogan_part1": "Construcții terase &",
        "slogan_part2": "placări exterioare cu lemn",
        "desc_niche": "amenajări terase, deck, pergole auto și placări decorative din lemn",
        "services": [
            {"icon": "🪵", "name": "Placări Decking Exterioare", "desc": "Montaj pardoseală caldă pentru balcoane, terase de apartament sau împrejurimi piscine din lemn exotic sau WPC rezistent."},
            {"icon": "🚗", "name": "Carporturi & Pergole Auto", "desc": "Copertine rezistente din grinzi masive de lemn cu acoperiș din policarbonat compact pentru protecția autoturismelor."},
            {"icon": "🎨", "name": "Restaurări Pergole & Întreținere", "desc": "Curățare mecanică sau chimică a lemnului înnegrit din cauza vremii și aplicare uleiuri speciale de protecție (teak oil)."}
        ],
        "image_url": "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?auto=format&fit=crop&w=600&q=80",
        "prefix": "pergole_foisoare_"
    },
    {
        "niche": "pergole_foisoare",
        "emoji": "🌲",
        "name": "Construcții Rustice Snagov",
        "phone": "0745 999 000",
        "location": "Strada Principală nr. 222, Snagov, Ilfov",
        "program": "Luni - Sâmbătă: 08:00 - 18:00 | Duminică: Închis",
        "slogan_part1": "Amenajări curți rustice &",
        "slogan_part2": "foișoare terase Snagov",
        "desc_niche": "construcții foișoare, case de vacanță din lemn și amenajări rustice",
        "services": [
            {"icon": "🏡", "name": "Foișoare & Bucătării de Vară", "desc": "Foișoare mari rustice dotate cu spații pentru bucătării de vară exterioare, gratare zidite din cărămidă și cuptoare."},
            {"icon": "🌲", "name": "Căsuțe Grădină & Depozitare", "desc": "Căsuțe din lemn pentru depozitarea uneltelor de grădinărit, lemne de foc sau biciclete, tratate împotriva intemperiilor."},
            {"icon": "🛹", "name": "Ponton & Terase pe Malul Apei", "desc": "Proiectare și montaj structuri grele din lemn tratat pentru pontoane pe malul apei sau terase suspendate."}
        ],
        "image_url": "https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=600&q=80",
        "prefix": "pergole_foisoare_"
    }
]

PALETTES = {
    "panouri_fotovoltaice": {
        "primary": "#eab308",
        "rgb": "234, 179, 8",
        "secondary": "#0f172a",
        "bg": "#fafdfb",
        "tag": "Sisteme Panouri Fotovoltaice"
    },
    "ginecologie": {
        "primary": "#ec4899",
        "rgb": "236, 72, 153",
        "secondary": "#1e1b4b",
        "bg": "#fff1f2",
        "tag": "Cabinet Ginecologie & Obstetrică"
    },
    "cazare_pensiuni": {
        "primary": "#d97706",
        "rgb": "217, 119, 6",
        "secondary": "#1e293b",
        "bg": "#faf7f5",
        "tag": "Cazare & Pensiune Premium"
    },
    "sali_box_fitness": {
        "primary": "#dc2626",
        "rgb": "220, 38, 38",
        "secondary": "#0b0f19",
        "bg": "#f9fafb",
        "tag": "Sală Box & Personal Training"
    },
    "pergole_foisoare": {
        "primary": "#854d0e",
        "rgb": "133, 77, 14",
        "secondary": "#27272a",
        "bg": "#fafaf9",
        "tag": "Construcții Pergole & Foișoare"
    }
}

REVIEWS_TEMPLATES = {
    "panouri_fotovoltaice": [
        "Echipa Smart Solar a instalat sistemul meu de 6kW într-o singură zi. Dosarul de prosumator a fost aprobat rapid. Producția de energie este excelentă!",
        "Am ales o pompă de căldură împreună cu sistemul fotovoltaic. Consumul de curent a scăzut considerabil și totul este complet automatizat. Recomand!",
        "Montaj curat și profesional. Materiale calitative, cabluri bine mascate în tuburi de protecție și explicații detaliate pentru aplicația de monitorizare.",
        "Colaborare de nota 10. Ne-au ajutat cu dimensionarea corectă a sistemului și totul funcționează perfect de peste 6 luni. Recomand cu drag!"
    ],
    "ginecologie": [
        "Doamna Dr. Maria Ionescu este un medic de o caldura si un profesionalism desavarsit. Mi-a urmarit toata sarcina si m-am simtit excelent. Multumesc din suflet!",
        "Cabinet foarte curat, dotat cu echipamente moderne. Ecografia 4D a fost realizată cu multă atenție, oferindu-ne fotografii minunate cu bebelușul nostru.",
        "Recomand clinica cu toata increderea. Atmosferă primitoare, personal amabil și consultații detaliate fără nicio grabă. Servicii medicale premium.",
        "Testările preventive și ecografia au fost explicate pe înțeles. Am primit tratamentul potrivit și sfaturi excelente de planning familial."
    ],
    "cazare_pensiuni": [
        "Am petrecut un weekend minunat la Green Oasis Cernica. Camere curate, liniște deplină, aer curat și o grădină imensă unde copiii s-au jucat liberi. Recomand!",
        "Cabana din bușteni Snagov este incredibilă! Ciubărul cu apă caldă sub cerul înstelat și plimbările cu kayak-ul pe lac au fost pur și simplu de neuitat.",
        "Experiența de glamping a fost la superlativ! Cortul este foarte confortabil și călduros, iar jacuzzi-ul privat de pe terasă oferă o relaxare totală.",
        "Pensiune primitoare în Corbeanca. Piscină curată, parcare securizată, mic dejun bogat și proaspăt. Gazde primitoare și servicii de înaltă clasă."
    ],
    "sali_box_fitness": [
        "Antrenamentele de box de aici sunt excelente! Antrenorul Alex are un stil grozav de predare și explică fiecare tehnică în detaliu. Atmosferă plină de energie.",
        "Am ales ședințele de personal training cu Gabriel și după 3 luni am slăbit 8 kg și mi-am îmbunătățit considerabil rezistența fizică. Cel mai bun antrenor!",
        "Fight Club Titan are cele mai bune circuite de kickbox și cardio. Antrenamente intense dar foarte sigure pentru începători. Merg cu mare plăcere.",
        "Club curat, saci de box noi, sală bine ventilată și antrenori foarte experimentați care știu cum să te motiveze să îți depășești limitele."
    ],
    "pergole_foisoare": [
        "Atelierul ne-a construit o pergolă auto superbă din lemn stratificat. Finisaje perfecte și rezistență excelentă în timp la ploi și zăpadă. Recomand!",
        "Foișorul din grădină a depășit așteptările noastre! Lucrare executată curat, montat rapid și lemnul a fost tratat cu lacuri premium. Profesioniști.",
        "Placarea terasei cu deck din WPC a fost executată de o echipă rapidă și atentă la detalii. Acum terasa arată modern și este foarte ușor de curățat.",
        "Bucătăria de vară din lemn masiv și foișorul construite la Snagov sunt ideale pentru weekenduri în familie. Lucrare rezistentă și aspect rustic superb."
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
    
    niche_templates = REVIEWS_TEMPLATES.get(niche, REVIEWS_TEMPLATES["pergole_foisoare"])
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
        num = 461 + idx
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
        html_content = html_content.replace("__DESC__", f"Servicii de {item['desc_niche']} în {item['location']}. Standarde înalte de calitate, garanție deplină și experiență recunoscută.")
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
