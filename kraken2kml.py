import pyproj
import csv
import sys


from lxml import etree
from pykml.parser import Schema
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX

doc = KML.kml(KML.Document())

# Open CSV file and parse line by line
with open(sys.argv[1], newline='') as csvfile:
    lobs = csv.reader(csvfile, delimiter=',')
    p=0
    for row in lobs:
        if p > 0:
            destination = pyproj.Geod(ellps='WGS84').fwd(row[9],row[8],row[1],2000)
            fromLocation = "%s,%s,10 " % (row[9],row[8])
            toLocation = "%s,%s,10 " % (destination[0],destination[1])

            # line of bearing as KML
            line = KML.Placemark(
                KML.LineString(
                    KML.extrude(1),
                    GX.altitudeMode("relativeToGround"),
                    KML.coordinates(
                    fromLocation,
                    toLocation
                    )
                )
            )
            print(etree.tostring(line, pretty_print=True))
            doc.Document.append(line)
        p+=1


kmlfile=sys.argv[1]+".kml"
print("Writing %d lobs to %s.." % (p,kmlfile))
outfile = open(kmlfile, 'w', encoding="utf-8")
outfile.write(etree.tostring(doc, pretty_print=True).decode("utf-8"))

