
import sys
import json
import math
from jinja2 import Environment, FileSystemLoader
from operator import itemgetter

# Set HTML output style : print / screen
style = "print"

# Set target system name and radius in ly
target_name = "Gateway"
radius = 15

#
# Return bitmap of economy types for the station.  Default value 0 is None
#
# Bit     Economy
#  1    Extraction
#  2    Refinery
#  3    Industrial
#  4    Agriculture
#  5    Terraforming
#  6    High Tech
#  7    Service
#  8    Tourism
#  9    Military
#
def station_economy (s):
    economy = 0
    for e in s:
        if "Extraction" in e:
            economy |= 0x0001
            break
        if "Refinery" in e:
            economy |= 0x0002
            break
        if "Industrial" in e:
            economy |= 0x0004
            break
        if "Agriculture" in e:
            economy |= 0x0008
            break
        if "Terraforming" in e:
            economy |= 0x0010
            break
        if "High Tech" in e:
            economy |= 0x0020
            break
        if "Service" in e:
            economy |= 0x0040
            break
        if "Tourism" in e:
            economy |= 0x0080
            break
        if "Military" in e:
            economy |= 0x0100
            break
    return economy

#
# Return filename of station icon
#
# e.g. coriolis_refinery.png
#
def station_icon (type, economy):
    # Decode station type
    #      1 = Civilian Outpost
    #      2 = Commercial Outpost
    #      3 = Coriolis Starport
    #      4 = Industrial Outpost
    #      5 = Military Outpost
    #      6 = Mining Outpost
    #      7 = Ocellus Starport
    #      8 = Orbis Starport
    #      9 = Scientific Outpost
    if (type == 1) | (type == 2) | (type == 4) | (type == 5) | (type == 6) | (type == 9):
        fname = "outpost_"
    elif (type == 3):
        fname = "coriolis_"
    elif (type == 7):
        fname = "ocellus_"
    elif (type == 8):
        fname = "orbis_"
    else:
        fname = "outpost_"

    # Append economy type
    if economy & 0x0001: fname += "extraction"
    if economy & 0x0002: fname += "refinery"
    if economy & 0x0004: fname += "industrial"
    if economy & 0x0008: fname += "agriculture"
    if economy & 0x0010: fname += "terraforming"
    if economy & 0x0020: fname += "high_tech"
    if economy & 0x0040: fname += "service"
    if economy & 0x0080: fname += "tourism"
    if economy & 0x0100: fname += "military"

    # Append .png
    fname += ".png"
    return fname

# Format population value into diplay-friendly string
def format_population (s):
    pop = float(s)
    if pop >= 1e9:   rc = "%5.1d B" % (pop/1e9)
    elif pop >= 1e6: rc = "%5.1d M" % (pop/1e6)
    elif pop >= 1e3: rc = "%5.1d K" % (pop/1e3)
    else:            rc = "%5.1d" % pop
    return rc

    
def main():
    # Import populated systems
    systems = []
    f = open("C:\Elite\systems_populated.jsonl", "r")
    for line in f:
        sys = json.loads(line)
        info = {'name' : sys['name'], 'id' : sys['id'], 'x' : sys['x'], 'y' : sys['y'], 'z' : sys['z'], 'population' : sys['population']}
        systems.append(info)
    f.close()

    # Import stations
    stations = []
    f = open("stations.jsonl", "r")
    for line in f:
        sta = json.loads(line)
        info = {}
        info['name'] = sta.get('name', "")
        name_split = info['name'].split()
        info['short_name'] = name_split[0].upper()
        info['type'] = sta.get('type_id', 0)
        info['system_id'] = sta.get('system_id', 0)
        info['distance'] = sta.get('distance_to_star', 0)
        info['economy'] = station_economy (sta['economies'])
        info['icon'] = station_icon(info['type'], info['economy'])
        info['superpower'] = sta['allegiance_id']
        # Clamp distance to 1M ls and log scale between 0 ls [0.0] and 1M ls [1.0]
        try:
            distance = float(info['distance'])
            if (distance >= 1e6): distance = 1e6
            log_distance = math.log10(distance)
        except TypeError:
            log_distance = 0.0
        info['log_distance'] = log_distance
        stations.append(info)
    f.close()

    # Get target system data
    target = {}
    for s in systems:
        if (s['name'] == target_name):
            target['name'] = target_name
            target['x'] = s['x']
            target['y'] = s['y']
            target['z'] = s['z']
            # Format population value into diplay-friendly string
            target['population'] = format_population (s['population'])
            # Extract list of stations in the target system
            sys_stations = []
            for sta in stations:
                if (sta['system_id'] == s['id']): sys_stations.append (sta)
            sys_stations.sort (key=itemgetter('distance'))
            target['stations'] = sys_stations
            break

    # Construct list of systems in the bubble, omitting target system
    bubble_systems = []
    for s in systems:
        dx = s['x'] - target['x']
        dy = s['y'] - target['y']
        dz = s['z'] - target['z']
        d = math.sqrt(dx*dx + dy*dy + dz*dz)
        if (d <= radius) & (s['name'] != target_name):
            system = {}
            system['name'] = s['name']
            system['distance'] = d
            system['population'] = format_population(s['population'])
            # Extract list of stations in this system
            sys_stations = []
            for sta in stations:
                if (sta['system_id'] == s['id']): sys_stations.append (sta)
            sys_stations.sort (key=itemgetter('distance'))
            system['stations'] = sys_stations
            bubble_systems.append (system)
    bubble_systems.sort (key=itemgetter('distance'))
                         
    # Generate html output page
    env = Environment(loader=FileSystemLoader('.\\templates'))
    template = env.get_template('bubble_template.html')
    filename = target_name + '.html'
    f = open(filename, "w")
    f.write (template.render({'target' : target, 'systems' : bubble_systems, 'style' : style}))
    f.close()


if __name__ == '__main__':
    main()
    
