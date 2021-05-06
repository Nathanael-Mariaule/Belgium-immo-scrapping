from bs4 import BeautifulSoup
import json as js

def find_brackets(text):
    """
        Function that takes for entry a text and return the position of the first brackets {}
        :param text: the text
        :return index1, index2: the indexes of the first { and  corresponding } in the text
    """
    index1, index2 = -1, -1

    for i, c in enumerate(text):
        if c == "{":
            index1 = i
            break

    for i in range(len(text) - 1, 0, -1):
        if text[i] == "}":
            index2 = i
            break

    return index1, index2

def scrap_page(html):
    """"
        The function takes for input a html sale page from immoweb and return a csv line with various informations
        regarding the sale
        :param hmtl: the html page as string
        :return csv_line: string that contains the informations on csv format
    """
    soup = BeautifulSoup(html, features="html.parser")
    variables = [None for i in range(24)]
    #first set of informations to be collected
    arguments = ["Surface habitable", 'Surface du terrain', 'Chambres', 'Meublé', 'Type de cuisine',
                 'Surface du jardin', 'Terrasse', 'Surface de la terrasse', 'Nombre de façades',
                 'État du bâtiment', 'Combien de feux ouverts ?', 'Piscine', 'Salles de bains', 'Toilettes', 'Dressing',
                 'Cave', 'Bureau', "Salon", 'Parkings intérieurs',
                 'Parkings extérieurs', 'Salle à manger', 'Salles de douche', 'Buanderie', 'Année de construction']
    #extract the info from the page
    rows = soup.find_all('tr', {'class': 'classified-table__row'})
    for row in rows:
        for i in range(len(arguments)):
            try:
                if arguments[i] in row.findChild('th').string:
                    variables[i] = row.findChild('td', {'class': 'classified-table__data'})\
                                    .children.__next__().string.strip()
            except:
                continue

    #extract a json file from the page
    json = soup.find_all("script")
    for j in json:
        if j.string != None:
            if "window.dataLayer" in j.string.split():
                json = j
                break
    start, end = find_brackets(json.string)
    json_clean = (json.string)[start:end + 1]
    data = js.loads(json_clean)
    adid, transaction_type, type_prop, subtype, zipcode, price = None, None, None, None, None, None

    #infos to be extracted from the json
    variables2 = [adid, transaction_type, type_prop, subtype, zipcode, price]
    mot_cle = ["id", "transactionType", "type", "subtype", "zip", 'price']

    for i in range(len(variables2)):
        try:
            variables2[i] = data["classified"][mot_cle[i]]
        except:
            variables2[i] = None
    etat = None
    try:
        etat = data["classified"]["building"]["condition"]
    except:
        etat = None
    #write all infos as a csv line
    csv_line = ""
    for var in variables:
        if var:
            csv_line += var+','
        else:
            csv_line += 'None,'
    for var in variables2:
        if var:
            csv_line += var + ','
        else:
            csv_line += 'None,'
    if etat:
        csv_line += etat + '\n'
    else:
        csv_line += 'None\n'
    return csv_line








