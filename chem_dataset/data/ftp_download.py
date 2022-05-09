import os
import ftplib
from tqdm import tqdm

def ftp_download(path,ftp_addr, ftp_path):
    """
    > This function downloads all files from a given FTP address and path to a given local path
    
    :param path: the path to the directory where you want to download the files
    :param ftp_addr: the address of the ftp server
    :param ftp_path: the path to the directory on the ftp server that you want to download from
    """
    ftp = ftplib.FTP(ftp_addr)
    ftp.login()
    ftp.cwd(ftp_path)
    filenames = ftp.nlst()
    filenames.sort()
    curr_files = os.listdir(path)
    for filename in tqdm(filenames):
        try:
            if filename not in curr_files and filename[-3:] != 'md5':
                out = path + filename
                with open(out, 'wb') as f:
                    ftp.retrbinary('RETR ' + filename, f.write)
        except ftplib.error_perm:
            pass
    ftp.quit()

def load_data():
    path = os.getcwd()

    try:
        isExist = os.path.exists(path + '/data')
        isExist_2 = os.path.exists(path + '/data/raw')
        if not isExist:
            os.mkdir(path + '/data')
        if not isExist_2:
            os.mkdir(path + '/data/raw')
        print('ok')
    except OSError as error: 
        print(error)

    path = os.path.join(path, 'data/raw/')
    ftp_addr = 'ftp.ncbi.nlm.nih.gov'
    ftp_path = 'pubchem/Compound/CURRENT-Full/SDF/'
    ftp_download(path,ftp_addr, ftp_path)

