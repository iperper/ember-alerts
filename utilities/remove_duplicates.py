'''
@author Isaac Perper

Remove duplicates from the dataset based on id (so only works if each point has
unique ID number)
'''

import os
import csv
import argparse

parser = argparse.ArgumentParser(description="Get IDs of datapoints already called")
parser.add_argument("--file", type=str, help="Name of csv file with training data")
args = parser.parse_args()

f = open('{}_noduplicates.csv'.format(args.file[:-4]), 'w')
writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

used_ids = set()
with open(args.file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if row[4] not in used_ids:
            writer.writerow(row)
            used_ids.add(row[4])

f.close()



