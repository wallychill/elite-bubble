import sys
import os
import json
import math

#
# Scan bodies.jsonl for landable planets with rare materials and volcanism
#
mats_jumponium = ({'element':"Polonium",  'symbol':"Po", 'share':0},
                  {'element':"Yttrium",   'symbol':"Yt", 'share':0},
                  {'element':"Niobium",   'symbol':"Nb", 'share':0},
                  {'element':"Cadmium",   'symbol':"Cd", 'share':0},
                  {'element':"Arsenic",   'symbol':"As", 'share':0},
                  {'element':"Vanadium",  'symbol':"V",  'share':0},
                  {'element':"Germanium", 'symbol':"Ge", 'share':0})

def main():
    s = '{:^40s}'.format("Planet") + '{:3s}'.format("Vol") + '{:^8s}'.format("ls")
    for mj in mats_jumponium:
        s += '{:^6s}'.format(mj['symbol'])
    print(s)

    # Open bodies database
    f = open("bodies.jsonl", "r")
    for line in f:
        body = json.loads(line)
        if (body['is_landable']):
            if (body['volcanism_type_id'] != 1):
                # print ('{:>3d}'.format(body['type_id']) + ' ' + '{:<20s}'.format(body['type_name']))
                if ((body['type_id'] == 30) or (body['type_id'] == 32)):
                    # Clear array of jumponium materials
                    for mj in mats_jumponium:
                        mj['share'] = 0

                    # Search through materials found on this body for any match in the set of jumponium elements
                    mats = body['materials']
                    match = False
                    for m in mats:
                        for mj in mats_jumponium:
                            if (m['material_name'] == mj['element']):
                                mj['share'] = m['share']
                                match = True
                        
                    if (match):
                        name = body['name']
                        volcanism = body['volcanism_type_id']
                        distance = body['distance_to_arrival']
                        system_id = body['system_id']
                        s = '{:40s}'.format(name) + '{:>3d}'.format(volcanism) + '{:>7d}'.format(distance)
                        for mj in mats_jumponium:
                            if (mj['share'] == 0):
                                s += '      '
                            else:
                                s += '{:>6.2f}'.format(mj['share'])
                        print(s)
        
    f.close()

if __name__ == '__main__':
    main()
    
