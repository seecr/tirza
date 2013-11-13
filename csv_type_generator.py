#!/usr/bin/env python3

import os
import sys
import csv
import re

def strip_csv_fields(file_name):
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        with open('tirza_uri_type.csv', 'w') as stripped_csv:
            csv_writer = csv.writer(stripped_csv, delimiter=',')
            for row in csv_reader:
                match = re.search(r'Description(\d+)', row[0])
                uri_no = match.group(1)
                #print(uri_no)
                match = re.search(r'(resource|ontology)/(\w+)_?', row[1])
                if match:
                    type_name = match.group(2)
                    if type_name.endswith('_'):
                        type_name = type_name[0:-1]
                    #print(type_name)
                else:
                    type_name = ''
                stripped_row = [uri_no, type_name]
                csv_writer.writerow(stripped_row)

def main():
    args = sys.argv[1:]
    assert len(args) >= 1
    arg = args[0]
    if os.path.isfile(arg):
        strip_csv_fields(arg)
    

if __name__ == '__main__':
    main()

