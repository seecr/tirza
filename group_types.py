#!/usr/bin/env python

import numpy as np
import csv
    
group_mapping = {}
type_uri_mapping = {}
types = []

def read_type_mapping():
    global group_mapping, type_uri_mapping
    with open('tirza_uri_type.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            group_mapping[int(row[0])-1] = row[1]
    #print group_mapping
    global types
    types = sorted(set(group_mapping.values()))
    type_uri_mapping = {}
    for media_type in types:
        for (i, mtype) in group_mapping.items():
            if media_type == mtype:
                if mtype in type_uri_mapping:
                    type_uri_mapping[mtype].add(i)
                else:
                    type_uri_mapping[mtype] = set([i])
    print type_uri_mapping
    return group_mapping

def read_sim_matrix():
    with open('tirza_cov.csv', 'r') as csv_file:
        sim_matrix = np.loadtxt(csv_file, delimiter=',')
        #print sim_matrix
        return sim_matrix

def calculate_svg(cov_matrix):
    (u, s, v) = np.linalg.svd(cov_matrix)
    #print s
    return (u, s, v)

def calcluate_similarity(cov_matrix, mtype1, mtype2):
    global types, type_uri_mapping
    len_m1 = len(type_uri_mapping[mtype1])
    len_m2 = len(type_uri_mapping[mtype2])
    result = 0.0
    count = 0
    for uri_m1 in type_uri_mapping[mtype1]:
        for uri_m2 in type_uri_mapping[mtype2]:
            entry = cov_matrix[uri_m1, uri_m2]
            if entry >= 0.3:
                count += 1
            result += entry
    #result = result / len_m1
    print "Relation from %s to %s: %f (%i->%i) %i" % (mtype1, mtype2, result,\
            len_m1, len_m2, count)
    return (result, count)

def calculate_groups(cov_matrix, mapping=group_mapping):
    global types
    len_types = len(types)
    sim_type_matrix = np.zeros(shape=(len_types, len_types))
    count_edges_matrix = np.zeros(shape=(len_types, len_types))
    for (i, mtype) in enumerate(types):
        for (j, omtype) in enumerate(types):
            if mtype != omtype:
                (sim, count) = calcluate_similarity(cov_matrix, mtype, omtype)
                sim_type_matrix[i, j] = sim
                count_edges_matrix[i, j] = count
    print (sim_type_matrix, count_edges_matrix)
    return (sim_type_matrix, count_edges_matrix)

def output_csv():
    pass # TODO

def main():
    read_type_mapping()
    cov_matrix = read_sim_matrix()
    calculate_svg(cov_matrix)
    calculate_groups(cov_matrix)

if __name__ == '__main__':
    main()
