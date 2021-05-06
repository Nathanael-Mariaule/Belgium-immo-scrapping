# Challenge-collecting-data

_Authors: Nathanaël Mariaule, Han Le, Jérémy Lipszyc_**

##1/ The project

In the context of Becode's AI training, we were asked to build a database containing various information on houses for sale.
This program scans two websites (ImmoVlan and ImmoWeb) for houses for sale and retrieves the data on the single page of each house.
The retrieved data is stored in two files in csv format named "data_immoweb.csv" and "data_immovlan.csv".

##2/ The files

###data_immoweb.csv and data_immovlan.csv:
Contain separate data from immoweb and immovlan

###data.csv
Contains the data collected in a single file of data_immoweb.csv and data_immovlan.csv

###post_codes.csv: [source](https://public.opendatasoft.com/explore/dataset/liste-des-codes-postaux-belges-fr/table/?flg=fr)
Used to get the postcodes and names of areas.

###immovlan_scrapping.py
Browse the ImmoVlan site and retrieve the html code of the unique pages for each house for sale.

###immovlan_page_scrapping.py
Parse the html code of a page and retrieve the desired data (see next point for more details).

###immoweb_scrapping.py
Browse the ImmoWeb site and retrieve the html code of the unique pages for each house for sale.

###immoweb_page_scrapping.py
arse the html code of a page and retrieve the desired data (see next point for more details).


##3/ Attributes in data.csv
They are 26 columns in data.csv:

*adid*: Id on the website
*bedrooms*: Number of bedrooms
*Locality*: Name of the area
*price*: Price
*transaction_type*: Type of sale (Exclusion of life sales)
*type_prop*: Type of the property (house, appartment)
*subtype*: Subtype of the property (villa, bungalow)
*zipcode*: Zipcode
*adress*: Adress of the house
*surface*: Surface of the land
*state*: State of the building (New, to be renovated, ...)
*facades*: Number of facades
*surface_land*: Surface area of the plot of land
*garden*: Garden (1 for yes, 0 for no)
*garden_surface*: Surface area of the garden
*terrace*: Terrace (1 for yes, 0 for no) 
*terrace_surface*: Surface area of the terrace
*swimming_pool*: Swimming pool (1 for yes, 0 for no) 
*number_rooms*: Number of rooms
*garage*: Garage (1 for yes, 0 for no)
*surface_living*: Surface area of the building
*furnished*: Furnished (1 for yes, 0 for no)
*bathrooms*: Number of bathrooms
*toilets*: Number of toilets
*equipped_kitchen*: Fully equipped kitchen (1 for yes, 0 for no)
*open_fire*: Open fire (1 for yes, 0 for no)
