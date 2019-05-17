import sys
import os
import json
import math
from datetime import date
import urllib.request

def main():
    # Save latest bodies_recentl.json from EDDB in local cache
    year = date.today().year
    month = date.today().month
    day = date.today().day
    datecode = '{:04d}'.format(year) + '{:02d}'.format(month) + '{:02d}'.format(day)
    daily = "bodies/bodies_recently_" + datecode + '.jsonl'
    urllib.request.urlretrieve ("http://eddb.io/archive/v6/bodies_recently.jsonl", daily)

    # Read daily update into memory
    recent = []
    n_recent = 0
    d = open(daily, "r")
    for line_daily in d:
        recent.append(json.loads(line_daily))
        n_recent += 1
    print ("Num records in daily update : " + '{:>5d}'.format(n_recent))
    
    # Open master bodies database
    n_old = 0
    n_updated = 0
    n_added = 0
    n_new = 0
    old = open("bodies.jsonl", "r")
    new = open("bodies_new.jsonl", "w");
    for line in old:
        record = json.loads(line)
        n_old += 1
        found = False
        
        # Scan daily update for a matching body id, with more recent update
        for update in recent:
#            print ("Compare " + '{:d}'.format(record['id']) + " vs " '{:d}'.format(update['id']))
            if (record['id'] == update['id']):
#                print ("    Compare " + '{:d}'.format(record['updated_at']) + " vs " '{:d}'.format(update['updated_at']))
                # Record matches, check if this is a newer update
                if (record['updated_at'] < update['updated_at']):
                    # Write the updated record instead of the original record
                    found = True
                    n_updated += 1
                    n_new += 1
                    new.write(json.dumps(update) + '\n')
                # Delete the record so it doesn't get appended later
                recent.remove(update)
                break
        if (not found):
            # No update found, write original record
            n_new += 1
            new.write(json.dumps(record) + '\n')
    # Append any remaining daily records
    for update in recent:
        n_new += 1
        n_added += 1
        new.write(json.dumps(update) + '\n')
        
    old.close()
    new.close()
    
    print ("Num records in old database : " + '{:>5d}'.format(n_old))
    print ("Num records in new database : " + '{:>5d}'.format(n_new))
    print ("Num records updated         : " + '{:>5d}'.format(n_updated))
    print ("Num records added           : " + '{:>5d}'.format(n_added))

    # Replace previous bodies database with new version
    os.remove("bodies_old.jsonl")
    os.rename("bodies.jsonl", "bodies_old.jsonl")
    os.rename("bodies_new.jsonl", "bodies.jsonl")

if __name__ == '__main__':
    main()
    
