import pandas as pd

def house_or_flat(text):
    if 'house' in text:
        return 'house'
    elif 'apartment' in text:
        return 'apartment'
    else:
        return text

def parking_value(data):
    if data == 'None':
        return 0
    try:
        x = int(data)
        if x > 0:
            return 1
        else:
            return 0
    except:
        return data

def parking_col(datas):
    new_data = pd.DataFrame()
    new_data['1'] = datas['Parkings extérieurs'].apply(lambda x: parking_value(x))
    new_data['2'] = datas['Parkings intérieurs'].apply(lambda x: parking_value(x))
    return new_data.max(axis=1)


def cuisine(data):
    fully_equipped = ['Américaine hyper-équipée', 'Équipée', 'Hyper équipée',
                      'Américaine équipée']
    not_equipped = ['Semi-équipée', 'None', 'Américaine semi-équipée', 'Pas équipée',
                    'Américaine non-équipée']
    if data in fully_equipped:
        return 1
    elif data in not_equipped:
        return 0
    else:
        return data


def number_of_rooms(datas):
    number_data = pd.Series()
    number_data = datas['Chambres'].apply(lambda x: int(x) if x != 'None' else 0)
    for value in ['Salles de bains', 'Salles de douche']:
        number_data = number_data.add(datas[value].apply(lambda x: int(x) if x != 'None' else 0))
    for value in ['Cave', 'Bureau', 'Salon', 'Salle à manger', 'Buanderie']:
        number_data = number_data.add(datas[value].apply(lambda x: 1 if x == 'Oui' else 0))
    return number_data


def clean_dataframe(datas):
    new_data = pd.DataFrame()
    new_data['id'] = datas['id']
    new_data['zip_code'] = datas["zip"]
    new_data['price'] = datas['price']
    new_data['transaction_type'] = datas['transactionType']
    new_data['type_prop'] = datas['type'].apply(lambda x: house_or_flat(x))
    new_data['subtype'] = datas['subtype']
    new_data['state'] = datas['État du bâtiment']
    new_data['year'] = datas['Année de construction']
    new_data['surface'] = datas['Surface habitable']
    new_data['surface_land'] = datas['Surface du terrain']
    new_data['facades'] = datas['Nombre de façades']
    new_data['garden'] = datas['Surface du jardin'].apply(lambda x: 0 if x == 'None' else 1)
    new_data['garden_surface'] = datas['Surface du jardin']
    new_data['terrace'] = datas['Surface de la terrasse'].apply(lambda x: 0 if x == 'None' else 1)
    new_data['terrace_surface'] = datas['Surface de la terrasse']
    new_data['number_rooms'] = number_of_rooms(datas)
    new_data['parking'] = parking_col(datas)
    new_data['furnished'] = datas['Meublé'].apply(lambda x: 1 if x == 'Oui' else 0)
    new_data['bathrooms'] = datas['Salles de bains']
    new_data['bedrooms'] = datas["Chambres"]
    new_data['toilets'] = datas['Toilettes']
    new_data['equipped_kitchen'] = datas['Type de cuisine'].apply(lambda x: cuisine(x))
    new_data['open_fire'] = datas['Combien de feux ouverts ?'].apply(lambda x: 0 if 'Non' in x else 1)
    new_data['swimming_pool'] = datas['Piscine'].apply(lambda x: 0 if 'Non' in x else 1)

    return new_data


