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

def delete_dup():
    # main_dir = os.path.join(os.getcwd(), '../../')
    # os.chdir(main_dir)
    # main_dir = os.getcwd()

    main_dir = os.getcwd()
    path = main_dir

    try:
        isExist = os.path.exists(path + '/data/processed')
        if not isExist:
            os.mkdir(path + '/data/processed')
        print('ok')
    except OSError as error: 
        print(error)

    file_in = os.path.join(main_dir, 'data/interim/valid/pubchem_test.csv')
    file_out = os.path.join(main_dir, 'data/processed/clean.csv')
    file_mis = os.path.join(main_dir, 'data/interim/mis/dup.csv')
    rm_dup(file_in, file_out, file_mis)

