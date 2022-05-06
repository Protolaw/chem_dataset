import csv
import os
from math import floor

def analyze(file, head_list):
    """
    It takes a file and a list of headers, and returns a list of dictionaries, where each dictionary
    contains the counts of each value in the corresponding column
    
    :param file: the name of the file you want to analyze
    :param head_list: a list of the headers you want to analyze
    :return: A list of dictionaries. Each dictionary contains the unique values of a column and the
    number of times they appear in the column.
    """
    list_dict = [{} for _ in range(len(head_list))]
    with open(file, 'r') as inp:
        lines = csv.reader(inp, delimiter='\n')
        for line in lines:
            clmn = list()
            for header in head_list:
                clmn.append(list(line)[0].split(',').index(header))
            break
    with open(file, 'r') as inp:
        lines = csv.reader(inp, delimiter=',')
        for line in lines:
            for i in clmn:
                el = line[i].strip()
                j = clmn.index(i)
                if el not in list_dict[j]:
                    list_dict[j][el] = 1
                else:
                    list_dict[j][el] += 1
    return list_dict


def write_to_scv(path, head_list, x):
    """
    This function takes in a path, a list of headers, and a list of dictionaries or a dictionary. It
    then writes the data to a csv file
    
    :param path: the path to the folder where you want to save the csv files
    :param head_list: a list of the headers for the data you want to write to csv
    :param x: the data to be written to the csv file
    """
    for head in head_list:
        stat_file = head + '.csv'
        with open(os.path.join(path, stat_file), 'w', newline='\n') as out:
            data = csv.writer(out, delimiter=',')
            if type(x) == list:
                for i in list(x[head_list.index(head)].items()):
                    if i[0] == head:
                        data.writerow([i[0], 'molecules'])
                        continue
                    data.writerow(i)
            if type(x) == dict:
                for i in list(x.items()):
                    if i[0] == head:
                        data.writerow([i[0], 'molecules'])
                        continue
                    data.writerow(i)


def mol_mass_stat(file, int_range, flag, limit):
    dict_mol_mass = {}
    header = 'mol_mass'
    with open(file, 'r') as inp:
        lines = csv.reader(inp, delimiter='\n')
        for line in lines:
            clmn = list(line)[0].split(',').index(header)
            break
    with open(file, 'r') as inp:
        lines = csv.reader(inp, delimiter=',')
        if flag == 0:
            for line in lines:
                if line[clmn] == header:
                    dict_mol_mass[header] = 'molecules'
                else:
                    l = floor(float(line[clmn]) / int_range) * int_range
                    if l not in dict_mol_mass.keys():
                        dict_mol_mass[l] = 1
                    else:
                        dict_mol_mass[l] += 1
        elif flag == 1:
            for line in lines:
                if line[clmn] == header:
                    dict_mol_mass[header] = 'molecules'
                else:
                    # limit for heavy_atoms
                    if int(line[8]) <= limit:
                        buff = floor(float(line[clmn]) / int_range) * int_range
                        if buff not in dict_mol_mass.keys():
                            dict_mol_mass[buff] = 1
                        else:
                            dict_mol_mass[buff] += 1

    return dict_mol_mass


def main():

    main_dir = os.path.join(os.getcwd(), '../../')
    os.chdir(main_dir)
    main_dir = os.getcwd()
    path_to_data = os.path.join(main_dir, 'data/processed/valid/')
    file = 'clean.csv'
    head_list = ['rot_bonds', 'h_acc', 'h_don', 'heavy_atoms', 'ring_count', 'bonds_count']
    path_to_stat = os.path.join(main_dir, "reports/figures/table")
    file = os.path.join(path_to_data, file)
    # interval range( every 50 ) if flag == 1 , limit is related to restriction of heavy_atoms quantity
    int_range = 50
    flag = 1
    limit = 100

    data = analyze(file, head_list)
    write_to_scv(path_to_stat, head_list, data)
    head_list = ['mol_mass']
    data = mol_mass_stat(file, int_range, flag, limit)
    write_to_scv(path_to_stat, head_list, data)

if __name__ == '__main__':
    main()
