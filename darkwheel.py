import sys
import json
import math
from operator import itemgetter

#
# darkwheel
#
# Search for Dark Wheel candidate systems, and collect data on potential characteristics of future candidate systems
#
# The Dark Wheel allegedly orbits the eighth moon of a gas giant planet
#
# Planet types:
#   23      Class III gas giant
#   30      High metal content world
#   31      Icy body
#   33      Rocky body
#   34      Rocky ice world
#   32      Metal-rich body

  
def main():
	# Table of regions used to parse system data into sub-regions
	#   Name = Region Name
	#	minX, maxX = Distance range from Sol (<= minX, <maxX)
	#	minY, maxY = Distance range from Sol (<= minY, <maxY)
	#	minZ, maxZ = Distance range from Sol (<= minZ, <maxZ)
    regions = []
    regions.append ({'name' : 'Core Systems',
                     'minX' : -200, 'maxX' : 200,
                     'minY' : -200, 'maxY' : 200,
                     'minZ' : -200, 'maxZ' : 200})
    regions.append ({'name' : 'Pleiades',
                     'minX' : 50,   'maxX' : 250,
                     'minY' : -75,  'maxY' : 125,
                     'minZ' : -185, 'maxZ' : 15})

    # Import bodies database
    systems = []
    try:
        f = open('edsm/systemsWithCoordinates7days.json', 'r')
    except:
        print ('Error opening file')
        exit()
            
    systems = json.load(f)
    f.close()
    
    for r in regions:
        #fname = r['name'] + ".jsonl"
        #f = open(fname, "w")

        print ('{:<30s}'.format(r['name']))
        # Filter systems in the region
        region_systems = []
        for s in systems:
            x = s['coords']['x']
            y = s['coords']['y']
            z = s['coords']['z']
            xCheck = (x >= r['minX']) and (x < r['maxX'])
            yCheck = (y >= r['minY']) and (y < r['maxY'])
            zCheck = (z >= r['minZ']) and (z < r['maxZ'])
            if (xCheck and yCheck and zCheck):
                print ('  ' + '{:<30s}'.format(s['name']) + '{:>8.2f}'.format(x) + '{:>8.2f}'.format(y) + '{:>8.2f}'.format(z))
                # Get bodies from EDSM API
                

if __name__ == '__main__':
    main()
    
