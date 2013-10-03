import json
import xmltodict

fileStr = open('ZIPtoStats.kml', 'r').read() 
doc = xmltodict.parse(fileStr)
ZIPtoCensus = {}
for zip_code in doc["kml"]["Document"]["Placemark"]:
    ZIPtoCensus[zip_code["name"][-5:]] = zip_code["description"]
    #print json.dumps(ZIPtoCensus[zip_code["name"][-5:]], sort_keys=True, indent=2)

fileStr = open('ZIP_boundaries_NY.kml', 'r').read()
doc = xmltodict.parse(fileStr)
ZIP_CODES = []
for zip_code in doc["kml"]["Folder"]["Document"]["Placemark"]:
    new_zip = {}
    new_zip["id"] = '%s' % zip_code['name']
    new_zip["type"] = "Feature"
    coordinates = [(float(coor.split(',')[0]), float(coor.split(',')[1])) for coor in zip_code["MultiGeometry"]["LinearRing"]["coordinates"].split()]
    new_zip["geometry"] = {"type": "Polygon", "coordinates": [coordinates]}

    new_zip["properties"] = {
        "name": 'ZIP Code %s' % zip_code['name']
    }
    try:
        new_zip["properties"].update(ZIPtoCensus[zip_code['name']])
    except (KeyError):
        continue
    
    ZIP_CODES.append(new_zip)
    #print json.dumps(new_zip, sort_keys=True, indent=2)

#print json.dumps(ZIP_CODES, sort_keys=True, indent=2)
print json.dumps(ZIP_CODES)
