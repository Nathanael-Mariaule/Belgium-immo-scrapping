def b_soup_immo(html):
    soup = BeautifulSoup(html, 'lxml')
    
    adid = soup.find("meta", {"name": "cXenseParse:rob-immo-property-adid"})
    if adid != None:
        adid = adid.get("content")
    else:
        adid = None
        
    bedrooms = soup.find("meta", {"name": "cXenseParse:rob-immo-property-bedrooms"})
    if bedrooms!= None:
        bedrooms = bedrooms.get("content")
    else:
        bedrooms = None
        
    city = soup.find("meta", {"name": "cXenseParse:rob-immo-property-city"})
    if city != None:
        city = city.get("content")
    else:
        city = None
        
    price = soup.find("meta", {"name": "cXenseParse:rob-immo-property-price"})
    if price != None:
        price = price.get("content")
    else:
        price = None
        
    transaction_type = soup.find("meta", {"name": "cXenseParse:rob-immo-transaction-type"})
    if transaction_type != None:
        transaction_type = transaction_type.get("content")
    else:
        transaction_type = None
    
    type_prop = soup.find("meta", {"name": "cXenseParse:rob-immo-property-type"})
    if type_prop!= None:
        type_prop = type_prop.get("content")
    else:
        type_prop = None
    
    subtype = soup.find("meta", {"name": "cXenseParse:rob-immo-property-subtype"})
    if subtype!= None:
        subtype = subtype.get("content")
    else:
        subtype = None
        
    zipcode = soup.find("meta", {"name": "cXenseParse:rob-immo-property-zipcode"})
    if zipcode != None:
        zipcode = zipcode.get("content")
    else:
        zipcode = None
        
    adresse = soup.find("span", {"class": "address-line"})
    if adresse != None:
        adresse = adresse.text
    else:
        adresse = None
        
    surface = soup.find("div", {"title": "Surface habitable"})
    if surface!= None:
        surface = surface.find("div", {"class":"fs-4"}).text[:-3]
    else:
        surface = None
    
    general = soup.find("div", {"id":"collapse_equipment_details"})
    etat = None
    if general != None:
        for element in general:
            try:
                text = element.text.strip()
                if text == "Etat du bien":
                    etat = element.find_next_sibling().text.strip()
            except AttributeError:
                pass
            
    exterieur = soup.find("div", {"id":"collapse_outdoor_details"}).find_all("div")
    facades, surface_terrain, garden, garden_surface, terrasse, terrasse_surface, piscine = None, None, None, None, None, None, None
    for element in exterieur:
        text = element.text.strip()
        if text == "Nombre de façades":
            facades = element.find_next_sibling().text.strip()
        elif text == "Surface du terrain (m²)":
            surface_terrain = element.find_next_sibling().text.strip()[:-3]
        elif text == "Jardin":
            garden = element.find_next_sibling().text.strip()
            if garden == "Oui":
                garden == 1
            else:
                garden == 0
        elif text == "Surface du jardin":
            garden_surface = element.find_next_sibling().text.strip()[:-3]
        elif text == "Terrasse aménagée":
            terrasse = element.find_next_sibling().text.strip()
            if terrasse == "Oui":
                terrasse == 1
            else:
                terrasse == 0
        elif text == "Surface de la terrasse":
            terrasse_surface = element.find_next_sibling().text.strip()[:-3]
        elif text == "Piscine extérieure":
            piscine = element.find_next_sibling().text.strip()
            if piscine == "Oui":
                piscine == 1
            else:
                piscine == 0

            
    interieur = soup.find("div", {"id":"collapse_indoor_details"}).find_all("div")
    nombre_chambres, garage, surface_habitable, meuble = None, None, None, None
    for element in interieur:
        text = element.text.strip()
        if text == "Nombre de chambres à coucher":
            nombre_chambres = element.find_next_sibling().text.strip()
        elif text == "Surface habitable":
            surface_habitable = element.find_next_sibling().text.strip()[:-3]
        elif text == "Garage":
            garage = element.find_next_sibling().text.strip()
            if garage == "Oui":
                garage == 1
            else:
                garage == 0
        elif text == "Meublé":
            meuble = element.find_next_sibling().text.strip()
            if meuble == "Oui":
                meuble == 1
            else:
                meuble == 0
    
    sanitaires = soup.find("div", {"id":"collapse_kitchenbath_details"})
    salles_de_bain, toilettes, cuisine_equipee = None, None, None
    if sanitaires != None:
        sanitaires = sanitaires.find_all("div")
        for element in sanitaires:
            text = element.text.strip()
            if text == "Nombre de salles de bain":
                salles_de_bain = element.find_next_sibling().text.strip()
            elif text == "Nombre de toilettes":
                toilettes = element.find_next_sibling().text.strip()
            elif text == "Equipement de la cuisine":
                cuisine_equipee = element.find_next_sibling().text.strip()
                if cuisine_equipee == "Oui":
                    cuisine_equipee == 1
                else:
                    cuisine_equipee == 0
    
    equipments = soup.find("div", {"id":"collapse_equipment_details"})
    cheminee = None
    if equipments != None:
        equipments = equipments.find_all("div")
        for element in equipments:
            text = element.text.strip()
            if text == "Feu ouvert":
                cheminee = element.find_next_sibling().text.strip()
                if cheminee == "Oui":
                    cheminee == 1
                else:
                    cheminee == 0
            
    
    return "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(adid, bedrooms, city, price, transaction_type,
     subtype, zipcode, adresse, surface, type_prop, etat,
     facades, surface_terrain, garden, garden_surface, terrasse, terrasse_surface, piscine,
     nombre_chambres, garage, surface_habitable, meuble,
     salles_de_bain, toilettes, cuisine_equipee, cheminee)
    