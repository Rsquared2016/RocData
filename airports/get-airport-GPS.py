db = open('GlobalAirportDatabase.txt', 'r')
airports = open('major-US-airports.txt', 'r')
out = open('airport-to-GPS.txt', 'w')

airport2gps = {}

numLines = 0
for line in airports:
        numLines += 1
	# skip header
        if numLines == 1:
		continue
	columns = line.split('\t')
        name = columns[3]
        code = columns[4].upper()
        airport2gps[code] = [0, 0]
airports.close()
print airport2gps.keys()

for line in db:
	columns = line.split(':')
        code = columns[1]
        if code in airport2gps.keys():
                lat = int(columns[5]) + int(columns[6])/60.0 + int(columns[7])/3600.0
                lon = -1*(int(columns[9]) + int(columns[10])/60.0 + int(columns[11])/3600.0)
                airport2gps[code][0] = lat
                airport2gps[code][1] = lon
db.close()

for (airport, latLon) in airport2gps.items():
        out.write('%s\t%f\t%f\n' % (airport, latLon[0], latLon[1]))
out.close()


	
