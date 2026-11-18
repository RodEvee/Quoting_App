# config.py

PLANTS = [
    # Tampa District
    {"plant_number": "4062", "district": "Tampa", "name": "56TH ST", "address": "5503 E Diana St, Tampa, FL 33610"},
    {"plant_number": "4058", "district": "Tampa", "name": "78TH ST", "address": "6725 78th St, Riverview, FL 33569"},
    {"plant_number": "1036", "district": "Tampa", "name": "BERTH 150", "address": "3711 Causeway Blvd, Tampa, FL 33619"},
    {"plant_number": "4061", "district": "Tampa", "name": "BIG BEND", "address": "6002 Big Bend Rd, Gibsonton, FL 33534"},
    {"plant_number": "1148", "district": "Tampa", "name": "BROOKSVILLE", "address": "10206 Cobb Rd, Brooksville, FL 34601"},
    {"plant_number": "1033", "district": "Tampa", "name": "EHREN CUTOFF", "address": "11121 Ehren Cutoff Rd, Land O Lakes, FL 34639"},
    {"plant_number": "4048", "district": "Tampa", "name": "LARGO", "address": "2195 Lake Ave SE, Largo, FL 33771"},
    {"plant_number": "1173", "district": "Tampa", "name": "LECANTO", "address": "2975 South Lecanto Hwy (491), Lecanto, FL 34461"},
    {"plant_number": "1037", "district": "Tampa", "name": "ODESSA", "address": "2430 Marathon Rd, Odessa, FL 33556"},
    {"plant_number": "4049", "district": "Tampa", "name": "ST PETE", "address": "601 24th Street South, Saint Petersburg, FL 33733"},
    {"plant_number": "4059", "district": "Tampa", "name": "WATERS", "address": "9117 Florida Mining Blvd, Tampa, FL 33634"},
    {"plant_number": "1142", "district": "Tampa", "name": "ZEPHYRHILLS", "address": "3946 Copeland Dr, Zephyrhills, FL 33542"},
    # Ocala / Gainesville District
    {"plant_number": "1136", "district": "Ocala/Gainesville", "name": "LEESBURG", "address": "2711 C.R. 33, Okahumpka, FL 34746"},
    {"plant_number": "1124", "district": "Ocala/Gainesville", "name": "WILDWOOD", "address": "4270 County Rd 124, Wildwood, FL 34785"},
    {"plant_number": "1155", "district": "Ocala/Gainesville", "name": "OCALA WEST", "address": "2355 SW 60th Ave, Ocala, FL 34474"},
    {"plant_number": "4010", "district": "Ocala/Gainesville", "name": "OCALA", "address": "619 SW 17th Street, Ocala, FL 34471"},
    {"plant_number": "1139", "district": "Ocala/Gainesville", "name": "GAINESVILLE", "address": "820 NW 53rd Ave, Gainesville, FL 32609"},
    # Polk District
    {"plant_number": "4042", "district": "Polk", "name": "AUBURNDALE", "address": "326 Recker Hwy, Auburndale, FL 33823"},
    {"plant_number": "1145", "district": "Polk", "name": "LAKELAND", "address": "3770 Main Ave, Lakeland, FL 33801"},
    {"plant_number": "1106", "district": "Polk", "name": "LAKE WALES", "address": "534 Story Road, Lake Wales, FL 33853"},
    {"plant_number": "1144", "district": "Polk", "name": "PLANT CITY", "address": "2680 US Hwy 92 East, Plant City, FL 33566"},
]

MIXES = [
    {"name": "2500 PSI REGULAR", "price": 183.00},
    {"name": "3000 PSI REGULAR", "price": 185.00},
    {"name": "3000 PSI PEAROCK PUMPMIX", "price": 197.00},
    {"name": "3500 PSI REGULAR", "price": 188.00},
    {"name": "3500 PSI PEAROCK PUMPMIX", "price": 200.00},
    {"name": "4000 PSI REGULAR", "price": 191.00},
    {"name": "4000 PSI PEAROCK PUMPMIX", "price": 203.00},
]

ADDITIVES = [
    {"name": "1% SUMMERSET", "price": 4.00},
    {"name": "2% SUMMERSET", "price": 8.00},
    {"name": "1% WINTERSET", "price": 4.00},
    {"name": "2% WINTERSET", "price": 8.00},
]

FIBERS = [
    {"item_no": "1589831", "name": "RESIDENTIAL FIBER", "price": 13.00},
    {"item_no": "1589832", "name": "COMMERCIAL FIBER", "price": 17.00},
]

TRUCK_FEES = [
    {"item_no": "1253207", "name": "FREIGHT CHARGE / PER LOAD", "price": 200.00},
    {"item_no": "1247818", "name": "FUEL SURCHARGE / PER LOAD", "price": 100.00},
    {"item_no": "1202749", "name": "ENVIRONMENTAL FEE / PER LOAD", "price": 25.00},
    {"item_no": "1586055", "name": "CONCRETE HANDLING FEE / PER LOAD", "price": 10.00},
]

COUNTY_TAX_RATES = {
    "Osceola (7.50%)": 0.075,
    "Hillsborough (7.50%)": 0.075,
    "Pinellas (7.00%)": 0.070,
    "Polk (7.00%)": 0.070,
    "Pasco (7.00%)": 0.070,
    "Hernando (6.50%)": 0.065,
    "Marion / Ocala (7.00%)": 0.070,
    "Alachua / Gainesville (7.50%)": 0.075,
    "Lake / Sumter (7.00%)": 0.070,
    "Orange (6.50%)": 0.065,
}