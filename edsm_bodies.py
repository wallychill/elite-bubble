import sys
import os
import json
import math
from datetime import date
import urllib.request
from pathlib import Path

def main():
    # If file does not exist, download from EDSM
    systems = Path('edsm/systemsWithCoordinates.json')
    if not systems.is_file():
        urllib.request.urlretrieve ("https://edsm.net/dump/systemsWithCoordinates.json", systems)

if __name__ == '__main__':
    main()
    
