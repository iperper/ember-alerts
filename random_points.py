import numpy as np
import argparse
import csv


box_corners= [[-124.43052823234245,41.77671368132927],[-116.21275479484245,32.66397383901734]]

box_edge = [[-124.92673044628157,39.3212354168924], [-118.99411325878157,32.34713863318287]]

edge_slope = -(box_edge[0][1] - box_edge[1][1])/(box_edge[0][0]
        - box_edge[0][1])

years = ['2017','2018','2019']

def random_date_generator(start_date, range_in_day, length):
    days_to_add = np.arange(0, range_in_day)
    random_dates = np.datetime64(start_date) + np.random.choice(days_to_add, (length, 1))
    return random_dates

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create random coordinates in box')
    parser.add_argument('--N', type=int, default=100, help='Number of coordinates to generate')
    parser.add_argument('--filename', type=str, default='non_fire.csv', help="File name of output to store coordinates")

    args = parser.parse_args()

    print(args.N)

    ## The height of the box from the top left corner
    width = box_corners[1][0] - box_corners[0][0]
    height = box_corners[1][1] - box_corners[0][1]

    print("Using coords {}".format(box_corners))
    print("Width: {}, Height: {}".format(width, height))
    print("Box Slope: {}, Box {}".format(edge_slope, box_edge))

    # Take random coordinates in the box and combine
    rand_lat = np.random.rand(args.N*len(years), 1)*width + box_corners[0][0]
    rand_long = np.random.rand(args.N*len(years), 1)*height + box_corners[0][1]

    rand_coords = np.hstack((rand_lat, rand_long))

    rand_dates_list = []

    for year in years:
        date_start = np.datetime64('{}-06-01'.format(year))
        date_end = np.datetime64('{}-09-01'.format(year))
        days_diff = (date_end - date_start).astype(int)
        
        rand_dates_list.append(random_date_generator(date_start, days_diff, args.N))

    rand_dates = np.vstack(rand_dates_list)
    
    output = []
    for d, c in zip(rand_dates, rand_coords):
        lon, lat = c[0], c[1]
        if (lat - box_edge[0][1]) > edge_slope*(lon - box_edge[0][0]):
            ## Date , Label, lon, lat
            output.append([str(d[0]).replace('-','/'), 0, lat, lon])

    

    with open(args.filename, 'w') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for data in output:
            writer.writerow(data)

