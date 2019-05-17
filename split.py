import sys
import json
import math
from operator import itemgetter
    
def main():
    # Import populated systems
    systems = []
    f = open("systems_populated.jsonl", "r")
    for line in f:
        sys = json.loads(line)
        info = {'name' : sys['name'],
		        'id' : sys['id'],
                'allegiance' : sys['allegiance'],
				'x' : sys['x'],
				'y' : sys['y'],
				'z' : sys['z'],
				'population' : sys['population']}
        systems.append(info)
    f.close()

	# Table of regions used to parse system data into sub-regions
	#   Name = Region Name
	#	minX, maxX = Distance range from Sol (<= minX, <maxX)
	#	minY, maxY = Distance range from Sol (<= minY, <maxY)
	#	minZ, maxZ = Distance range from Sol (<= minZ, <maxZ)
    regions = []
    regions.append ({'name' : 'Upper North East',
                     'minX' : 0,    'maxX' : 500,
                     'minY' : 0,    'maxY' : 500,
                     'minZ' : 0,    'maxZ' : 500})
    regions.append ({'name' : 'Upper South East',
                     'minX' : 0,    'maxX' : 500,
                     'minY' : 0,    'maxY' : 500,
                     'minZ' : -500, 'maxZ' : 0})
    regions.append ({'name' : 'Upper South West',
                     'minX' : -500, 'maxX' : 0,
                     'minY' : 0,    'maxY' : 500,
                     'minZ' : -500, 'maxZ' : 0})
    regions.append ({'name' : 'Upper North West',
                     'minX' : -500, 'maxX' : 0,
                     'minY' : 0,    'maxY' : 500,
                     'minZ' : 0,    'maxZ' : 500})
    regions.append ({'name' : 'Lower North East',
                     'minX' : 0,    'maxX' : 500,
                     'minY' : -500, 'maxY' : 0,
                     'minZ' : 0,    'maxZ' : 500})
    regions.append ({'name' : 'Lower South East',
                     'minX' : 0,    'maxX' : 500,
                     'minY' : -500, 'maxY' : 0,
                     'minZ' : -500, 'maxZ' : 0})
    regions.append ({'name' : 'Lower South West',
                     'minX' : -500, 'maxX' : 0,
                     'minY' : -500, 'maxY' : 0,
                     'minZ' : -500, 'maxZ' : 0})
    regions.append ({'name' : 'Lower North West',
                     'minX' : -500, 'maxX' : 0,
                     'minY' : -500, 'maxY' : 0,
                     'minZ' : 0,    'maxZ' : 500})

    # Open summary CSV file
    f_summary = open("summary.csv", "w")
    f_summary.write ("Region, Total, Federation, Imperial, Alliance, Independent, Pilots Federation, Thargoid, Guardian, None\n")
        
    for r in regions:
        fname = r['name'] + ".jsonl"
        f = open(fname, "w")

        # Collect statistics
        stats = {'n' : 0, 'fed' : 0, 'imp' : 0, 'all' : 0, 'ind' : 0, 'pfd' : 0, 'bug' : 0, 'non' : 0, 'grd' : 0}
        
        # Construct list of systems in the region
        region_systems = []
        for s in systems:
            xCheck = (s['x'] >= r['minX']) & (s['x'] < r['maxX'])
            yCheck = (s['y'] >= r['minY']) & (s['y'] < r['maxY'])
            zCheck = (s['z'] >= r['minZ']) & (s['z'] < r['maxZ'])
            if (xCheck & yCheck & zCheck):
                f.write(json.dumps(s) + '\n')
                stats['n'] += 1
                if (s['allegiance'] == "Federation"):
                    stats['fed'] += 1
                elif (s['allegiance'] == "Empire"):
                    stats['imp'] += 1
                elif (s['allegiance'] == "Alliance"):
                    stats['all'] += 1
                elif (s['allegiance'] == "Independent"):
                    stats['ind'] += 1
                elif (s['allegiance'] == "Pilots Federation"):
                    stats['pfd'] += 1
                elif (s['allegiance'] == "Thargoid"):
                    stats['bug'] += 1
                elif (s['allegiance'] == "Guardian"):
                    stats['grd'] += 1
                elif (s['allegiance'] == "None"):
                    stats['non'] += 1
                else:
                    print(s['allegiance'])
        f.close()
                    
        # Print Summary statistics
        f_summary.write (r['name'] + ',')
        f_summary.write (str(stats['n']) + ',')
        f_summary.write (str(stats['fed']) + ',')
        f_summary.write (str(stats['imp']) + ',')
        f_summary.write (str(stats['all']) + ',')
        f_summary.write (str(stats['ind']) + ',')
        f_summary.write (str(stats['pfd']) + ',')
        f_summary.write (str(stats['bug']) + ',')
        f_summary.write (str(stats['grd']) + ',')
        f_summary.write (str(stats['non']) + '\n')
        
    f_summary.close()


if __name__ == '__main__':
    main()
    
