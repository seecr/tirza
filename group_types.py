#!/usr/bin/env python

import numpy as np
import csv

def read_type_mapping():
    group_mapping = {}
    with open('tirza_uri_type.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            group_mapping[row[0]] = row[1]
    print group_mapping
    return group_mapping

def read_sim_matrix():
    pass # TODO

def calculate_groups():
    pass # TODO

def calcluate_similarity():
    pass # TODO

def output_csv():
    pass # TODO

def main():
    read_type_mapping()

if __name__ == '__main__':
    main()
