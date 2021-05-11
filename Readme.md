# Challenge-collecting-data

_Authors: Nathanaël Mariaule, Han Le, Jérémy Lipszyc_

## 1/ The project

In the context of Becode's AI training, we were asked to build a database containing various information on houses for sale.
This program scans two websites (ImmoVlan and ImmoWeb) for houses for sale and retrieves the data on the single page of each house.
The retrieved data is stored in data.csv .

## 2/ The files

### data_immoweb.csv and data_immovlan.csv:
Contain separate data from immoweb and immovlan

### data.csv
Contains the data collected in a single file of data_immoweb.csv and data_immovlan.csv

### post_codes.csv: [source](https://public.opendatasoft.com/explore/dataset/liste-des-codes-postaux-belges-fr/table/?flg=fr)
Used to get the postcodes and names of areas.

### immovlan_scrapping.py
Browse the ImmoVlan site and retrieve the html code of the unique pages for each house for sale.

### immovlan_page_scrapping.py
Parse the html code of a page and retrieve the desired data (see next point for more details).

### immoweb_scrapping.py
Browse the ImmoWeb site and retrieve the html code of the unique pages for each house for sale.

### immoweb_threading.py
Multi-threading version of immoweb_scrapping.py

### immoweb_page_scrapping.py
Parse the html code of a page and retrieve the desired data (see next point for more details).

### data_cleaner.py
Clean the datas obtained with immoweb_scrapping.py using pandas


## 3/ Attributes in data.csv
They are 26 columns in data.csv:

1. *id*: Id on the website.
2. *bedrooms*: Number of bedrooms.
4. *price*: Price.
5. *transaction_type*: Type of sale (Exclusion of life sales).
6. *type_prop*: Type of the property (house, appartment).
7. *subtype*: Subtype of the property (villa, bungalow).
8. *zipcode*: Zipcode.
9. *adress*: Adress of the house.
10. *surface_land*: Surface of the land.
11. *state*: State of the building (New, to be renovated, ...).
    *year*: Year of the construction
12. *facades*: Number of facades.
13. *surface*: Surface building area.
14. *garden*: Garden (1 for yes, 0 for no).
15. *garden_surface*: Surface area of the garden.
16. *terrace*: Terrace (1 for yes, 0 for no).
17. *terrace_surface*: Surface area of the terrace.
18. *swimming_pool*: Swimming pool (1 for yes, 0 for no).
19. *number_rooms*: Number of rooms.
20. *parking*: Garage or Parking place (1 for yes, 0 for no).
21. *surface_living*: Surface area of the building.
22. *furnished*: Furnished (1 for yes, 0 for no).
23. *bathrooms*: Number of bathrooms.
24. *toilets*: Number of toilets.
25. *equipped_kitchen*: Fully equipped kitchen (1 for yes, 0 for no).
26. *open_fire*: Open fire (1 for yes, 0 for no).
