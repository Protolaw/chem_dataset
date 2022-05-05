from random import shuffle
from io import StringIO
from itertools import chain, islice
from subprocess import run
from collections import defaultdict
from time import time

from CGRtools.files import SDFRead, SDFWrite, SMILESRead
from CGRtools.exceptions import InvalidAromaticRing
from multiprocessing import Pool

import logging
import pickle
import warnings
import os
import csv
from tqdm import tqdm

# В качестве параметра принимает данные о молекулы
# определяет id
# 1)При наличии ошибок в структуре молекулы, функция возращает число (id молекулы)
# Ошибки: корректность ароматичееского цикла, наличие радикала, корректность валентонсти,
# длина молекулы менее 2 и более 150, при неудачной попытке перевода молекулы в ароматический вид,
# если молекула содержит более 1 соединения
# 2) При отсутствии ошибок:
# заполняет массив метаданными о молекуле по определенным заголовкам
# Заголовки = строка SMILES + значения словаря names_transfrom + список module_headers,
# если данные отсутствуют - определить как 'nan'
# 3) Возвращение массива данных

def standardize_molecule(molecule: MoleculeContainer) -> Optional[MoleculeContainer]:
    """
    It takes a molecule, checks if it's valid, and if it is, it returns a standardized version of the
    molecule
    
    :param molecule: The molecule to standardize
    :type molecule: MoleculeContainer
    :return: A standardized molecule
    """

    if len(molecule) > 150 or len(molecule) < 2:
        return None

    bad_elements = set(range(58, 72))
    bad_elements.update([10, 18, 36, 54])

    bad_element_present = False
    for _, atom in molecule.atoms():
        if atom.atomic_number in bad_elements or atom.atomic_number > 84:
            bad_element_present = True
            break

    if bad_element_present:
        return None

    conn_comp = molecule.connected_components_count
    if conn_comp > 1:
        return None

    if molecule.is_radical:
        return None

    try:
        molecule.kekule()
        molecule.standardize(fix_stereo=False)
        molecule.clean_isotopes()

        if molecule.check_valence():
            return None

        molecule.implicify_hydrogens(fix_stereo=False)
        molecule.remove_hydrogen_bonds(fix_stereo=False)
        molecule.clean_stereo()
        molecule.thiele()
        return molecule
    except InvalidAromaticRing:
        return None

# Данная функция принимает в качестве параметра массив строк (данных о моолекуле),
# параллелит данные для обработки функцией std_molecule
# и возвращает очищенные данные:
# в случае ошибки - число (type int), Pubchem ID
# в случае валидности - данные этой молекулы

def run_std(readed_molecules):
    with Pool(7) as p:
        filtered_molecules = p.map(std_molecule, readed_molecules)
    return filtered_molecules

def standardize_pubchem_batch(molecules: List[MoleculeContainer], pubchem_ids: List[int],
                              std_writer: Any, mistakes_writer: Any, pubchem_meta: List[str]) -> None:
    """
    It takes a batch of molecules, processes them, and writes the results to a file
    
    :param molecules: List of MoleculeContainer objects
    :type molecules: List[MoleculeContainer]
    :param pubchem_ids: a list of PubChem IDs
    :type pubchem_ids: List[int]
    :param std_writer: a csv.writer object that will write the standardized molecules to a file
    :type std_writer: Any
    :param mistakes_writer: a csv.writer object that will write the PubChem IDs of molecules that were
    filtered out
    :type mistakes_writer: Any
    :param pubchem_meta: a list of metadata keys to be extracted from the molecule.meta dictionary
    :type pubchem_meta: List[str]
    """
    filtered_molecules = run_std(molecules)
    for pubchem_id, molecule in zip(pubchem_ids, filtered_molecules):
        if molecule:
            mol_line = [str(molecule)]
            for key in pubchem_meta:
                if key in molecule.meta.keys():
                    mol_line.append(molecule.meta[key])
                else:
                    mol_line.append('nan')
            mol_line.append(molecule.rings_count)
            mol_line.append(molecule.molecular_mass)
            mol_line.append(molecule.bonds_count)
            std_writer.writerow(mol_line)
        else:
            mistakes_writer.writerow([pubchem_id])
    del filtered_molecules

def standardize_sdf_pubchem(name: str, std_writer: Any, mistakes_writer: Any,
                            batch_size: int, pubchem_meta: List[str]) -> None:
    """
    It reads a SDF file, standardizes the molecules in batches, and writes the standardized molecules to
    a new SDF file
    
    :param name: the name of the file to be standardized
    :type name: str
    :param std_writer: a writer to write the standardized molecules to
    :type std_writer: Any
    :param mistakes_writer: a file to write the molecules that couldn't be standardized to
    :type mistakes_writer: Any
    :param batch_size: the number of molecules to standardize at once
    :type batch_size: int
    :param pubchem_meta: a list of strings that will be added to the metadata of the standardized
    molecule
    :type pubchem_meta: List[str]
    """
    readed_molecules, readed_ids = [], []
    with SDFRead(name, indexable=True) as inp:
        inp.reset_index()
        for n, molecule in enumerate(inp):
            readed_molecules.append(molecule)
            readed_ids.append(int(molecule.meta['PUBCHEM_COMPOUND_CID']))
            if len(readed_molecules) == batch_size:
                assert len(readed_ids) == batch_size
                standardize_pubchem_batch(readed_molecules, readed_ids, std_writer, mistakes_writer, pubchem_meta)
                del readed_molecules
                readed_molecules = []
                del readed_ids
                readed_ids = []
        if readed_molecules:
            standardize_pubchem_batch(readed_molecules, readed_ids, std_writer, mistakes_writer, pubchem_meta)
            del readed_molecules
            del readed_ids
        os.remove(name)

def standardize_pubchem(input_files_path: str, output_file: str, mistake_file: str, batch_size: int) -> None:
    """
    It takes a path to a directory with .sdf.gz files,
    unzips them, standardizes them, and writes the results to a .csv file.
    
    :param input_files_path: path to the folder with the downloaded files
    :type input_files_path: str
    :param output_file: the path to the output file
    :type output_file: str
    :param mistake_file: a file to write the pubchem_ids of the molecules that couldn't be standardized
    :type mistake_file: str
    :param batch_size: the number of molecules to be processed at once
    :type batch_size: int
    """
    pubchem_meta = ['PUBCHEM_COMPOUND_CID', 'PUBCHEM_OPENEYE_CAN_SMILES', 'PUBCHEM_IUPAC_OPENEYE_NAME',
                    'PUBCHEM_CACTVS_ROTATABLE_BOND', 'PUBCHEM_XLOGP3_AA', 'PUBCHEM_CACTVS_HBOND_ACCEPTOR',
                    'PUBCHEM_CACTVS_HBOND_DONOR', 'PUBCHEM_HEAVY_ATOM_COUNT']
    pubchem_headers = ['pubchem_id', 'pubchem_smiles', 'iupac_name', 'rot_bonds',
                       'logp', 'h_acc', 'h_don', 'heavy_atoms']
    cgrtools_headers = ['ring_count', 'mol_mass', 'bonds_count']
    files = os.listdir(input_files_path)
    files.sort()
    with open(output_file, 'w', newline='\n') as standardized_out, open(mistake_file, 'w', newline='\n') as mistakes_out:
        std_mols_writer = csv.writer(standardized_out, delimiter=',')
        mistakes_writer = csv.writer(mistakes_out, delimiter=',')
        fields_names = ['smiles'] + pubchem_headers + cgrtools_headers
        std_mols_writer.writerow(fields_names)
        mistakes_writer.writerow(['pubchem_id'])
        for file_name in tqdm(files):
            if file_name[-2:] == 'gz':
                file = input_files_path + file_name
                name = file[:-3]
                run(["gunzip", "-k", file])
                standardize_sdf_pubchem(name, std_mols_writer, mistakes_writer, batch_size, pubchem_meta)


# Функция заходит в рабочее простанство, которое содержит архивы (метаданные базы данных [в формате SDF]),
# далее инициализирует (открывает) 2 csv-файла
# 1 - для валидных даных, 2 - для данных с ошибками
# далее определяет заголовки строк - список
# По 1 файлу обрабатывает отправляя в функцию read_std_pubchem

def main():
    path = os.path.join(os.getcwd()[:-9], 'data/')
    output_file_path = os.path.join(path, 'processed/pubchem_test.csv')
    mistakes_file_path = os.path.join(path, 'processed/pubchem_test_mistakes.csv')
    path = os.path.join(path, 'raw/' )
    batch_size = 10000

    standardize_pubchem(path, output_file_path, mistakes_file_path, batch_size)

if __name__ == '__main__':
    main()