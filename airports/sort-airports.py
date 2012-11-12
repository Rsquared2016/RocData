input = open('airport-to-GPS-edited.txt', 'r')
airports = open('major-US-airports.txt', 'r')
out = open('airport-to-GPS-sorted-by-passenger-count.txt', 'w')

a2name = {}
a2count = {}
a2rank = {}
a2gps = {}

for line in input:
	columns = line.split('\t')
        code = columns[0]
        lat = float(columns[1])
        lon = float(columns[2])
        a2gps[code] = [lat, lon]
input.close()

numLines = 0
for line in airports:
        numLines += 1
	# skip header
        if numLines == 1:
		continue
	columns = line.strip().split('\t')
        code = columns[4].upper()
        name = columns[3]
        rank = columns[1]
        count = columns[-1]
        out.write('%s\t%f\t%f\t%s\t%s\n' % (code, a2gps[code][0], a2gps[code][1], name, count))
        a2name[code] = name
        a2rank[code] = rank
        a2count[code] = count
airports.close()
out.close()
