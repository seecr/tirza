#!/usr/bin/env python3

import os
import sys
import csv
#from itertools import izip

tmp_file = '/tmp/tmp.csv'
column_mapping = list()

def order_rows(file_name):
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        with open(tmp_file, 'w') as stripped_csv:
            csv_writer = csv.writer(stripped_csv, delimiter=',')
            ordered_rows = {}
            for row in csv_reader:
                if row[0]:
                    ordered_rows[int(row[0])] = row[1:]
                else:
                    ordered_rows[0] = row[1:]
                    column_mapping = [int(x) for x in row[1:]]
                    print(column_mapping)
            for uri in ordered_rows.keys():
                print(uri)
                values = ordered_rows[uri]
                csv_writer.writerow(values)

def transpose_csv():
    tmp = zip(*csv.reader(open(tmp_file, "r")))
    csv.writer(open(tmp_file, "w")).writerows(tmp)


def order_columns(csv_file):
    pass # TODO


def main():
    args = sys.argv[1:]
    assert len(args) >= 1
    arg = args[0]
    if os.path.isfile(arg):
        order_rows(arg)
        transpose_csv()
        order_columns('tirza_matrix_cleaned.csv')
    

if __name__ == '__main__':
    main()

