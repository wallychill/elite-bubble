import sys
import os
import json
import math
from datetime import date
import urllib.request
from pathlib import Path

def main():
    recent = []
    n_recent = 0
    d = open('edsm/bodies7days.json', 'r')
    with d:
        body = json.load(d)
        print (body)

if __name__ == '__main__':
    main()
    
