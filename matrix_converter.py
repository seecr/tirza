#!/usr/bin/env python3

import os
import sys
import csv

tmp_file = '/tmp/tmp.csv'

def order_rows(file_name):
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        with open(tmp_file, 'w') as stripped_csv:
            csv_writer = csv.writer(stripped_csv, delimiter=',')
            ordered_rows = []
            for row in csv_reader:
                ordered_rows[int(row[0])] = row[1:]
            csv_writer.writerows(ordered_rows)

def order_columns(csv_file):
    pass # TODO


def main():
    args = sys.argv[1:]
    assert len(args) >= 1
    arg = args[0]
    if os.path.isfile(arg):
        order_rows(arg)
        order_columns('tirza_matrix_cleaned.csv')
    

if __name__ == '__main__':
    main()

