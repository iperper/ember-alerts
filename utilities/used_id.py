'''
@author Isaac Perper

Creates csv file with ids of points already called on API, such that darksky
doesn't use API calls unnecessarily
'''

import os
import csv
import argparse

parser =argparse.ArgumentParser(description="Get IDs of datapoints already called")
parser.add_argument("--file", type=str, help="Name of csv file with training data")
args = parser.parse_args()

f = open('used_ids.csv', 'w')
writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)

firstline = True
used_ids = set()
with open(args.file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if firstline:
            firstline = False
            continue
        if row[4] not in used_ids:
            writer.writerow([row[4]])
            used_ids.add(row[4])

f.close()



