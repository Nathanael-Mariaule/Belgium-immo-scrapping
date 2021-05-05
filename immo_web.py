def b_soup_immo_web(html):
    soup = BeautifulSoup(html,'lxml')
    json = soup.find_all("script")
    for j in json:
        print(j.string)
        if j.string != None:
            if "window.dataLayer" in j.string.split():
                json = j
                break
    start, end = find_brackets(j.string)
    json_clean = (j.string)[start:end+1]
    data = js.loads(json_clean)
    print(data)
    adid, transaction_type, type_prop, subtype, zipcode, price = None, None, None, None, None, None
    
    variables= [adid, transaction_type, type_prop, subtype, zipcode, price]
    mot_cle = ["id", "transactionType", "type", "subtype", "zip", "price"]
    
    for i in range(len(variables)):
        print(data["classified"][mot_cle[i]])
        try:
            variables[i] = data["classified"][mot_cle[i]]
        except:
            print("Exception")
            variables[i] = None
    
    try:
        etat = data["classified"]["building"]["condition"]
    except:
        etat = None
    
    
    
    """headers = soup.find_all("th", {"class":"classified-table__header"})
    
    adid, bedrooms, city, price, transaction_type, subtype, zipcode, adresse, surface, type_prop,
    etat, facades, surface_terrain, garden, garden_surface, terrasse, terrasse_surface, piscine,
    nombre_chambres, garage, surface_habitable, meuble, salles_de_bain, toilettes, cuisine_equipee, cheminee = None *27
    
    for header in headers:
        text = header.string.strip()
        print(text)
        if text == "Surface habitable":
            surface_habitable = header.find_next_sibling().text.strip()[0:4].strip()
        elif text == "Nombre de façades":
            facades = header.find_next_sibling().text.strip()
        elif text == "État du bâtiment":
            etat = header.find_next_sibling().text.strip()
        elif text == "Quartier ou lieu-dit":
            = header.find_next_sibling().text.strip()"""
        

def find_brackets(text):
    index1, index2 = -1, -1
    
    for i, c in enumerate(text):
          if c == "{":
            index1 = i
            break
    
    for i in range(len(text)-1, 0, -1):
        if text[i] == "}":
            index2 = i
            break
    
    return index1, index2

"""        
adid, bedrooms, city, price, transaction_type, subtype, zipcode, adresse, surface, type_prop,
etat, facades, surface_terrain, garden, garden_surface, terrasse, terrasse_surface, piscine,
nombre_chambres, garage, surface_habitable, meuble, salles_de_bain, toilettes, cuisine_equipee, cheminee"""
b_soup_immo_web(html)