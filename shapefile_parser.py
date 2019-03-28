import shapefile
import csv
import os

cur_dir = os.path.dirname(os.path.realpath(__file__))
shpname = cur_dir + '/ZillowNeighborhoods-NJ/ZillowNeighborhoods-NJ.shp'
def write_data(filename):
    dirname = os.path.dirname(os.path.realpath(__file__)) + f'/{filename}.csv'
    csvfile = open(dirname, 'w', newline='')
    writer = csv.writer(csvfile)
    print(shpname)
    sf = shapefile.Reader(shpname)
    shapes = sf.shapes()
    line = 1
    num = 0
    for shape in shapes:
        for point in shape.points:
            temp = [str(num), str(point[0]), str(point[1]), None]
            writer.writerow(temp)
            line += 1
        num += 1

    csvfile.close()
    print(f'{filename} is {str(line)} points and {str(num)} paths')


def main():
    write_data('/Users/franklin/SSW695/SSW695_DuckHome/ZillowNeighborhoods-NJ/ZillowNeighborhoods-NJ.shp')
if __name__ == '__main__':
    main()