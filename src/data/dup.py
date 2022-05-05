from CGRtools.files import SDFRead, SDFWrite, SMILESRead
import csv
import os
from tqdm import tqdm

def rm_dup(file_in, file_out, file_mis):
    """
    It takes a file with a list of SMILES strings, and removes all duplicates
    
    :param path: the path to the directory where the files are located
    :param file_in: the name of the file you want to remove duplicates from
    :param file_out: the name of the file that will contain the unique molecules
    :param file_mis: the file that will contain the duplicates
    """
    smiles_parser = SMILESRead.create_parser()
    unique_hashes = set()
    with open(file_in, 'r') as inp, \
            open(file_out, 'w', newline='\n') as out, \
            open(file_mis, 'w', newline='\n') as mis:
        lines = csv.reader(inp, delimiter=',')
        data = csv.writer(out, delimiter=',')
        mis = csv.writer(mis, delimiter=',')
        for line in tqdm(lines):
            el = line[0].strip().split(',')
            if el[0] == "smiles":
                data.writerow(line)
                mis.writerow(line)
                continue
            mol = smiles_parser(el[0])
            length_before = len(unique_hashes)
            try:
                unique_hashes.add(hash(mol))
            except TypeError:
                mis.writerow(line)
                continue
            length_after = len(unique_hashes)
            if length_before < length_after:
                data.writerow(line)
            else:
                mis.writerow(line)

def main():
    path = os.path.join(os.getcwd()[:-9], 'data/processed')
    file_in = os.path.join(path, 'valid/pubchem_test.csv')
    file_out = os.path.join(path, 'valid/clean.csv')
    file_mis = os.path.join(path, 'mis/dup.csv')
    rm_dup(file_in, file_out, file_mis)

if __name__ == '__main__':
    main()