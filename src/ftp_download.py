import os
import ftplib
from tqdm import tqdm

def ftp_download(path,ftp_addr, ftp_path):
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

def main():
    path = os.getcwd()
    path = os.path.join(path[:-3], 'data/raw/')
    ftp_addr = 'ftp.ncbi.nlm.nih.gov'
    ftp_path = 'pubchem/Compound/CURRENT-Full/SDF/'
    ftp_download(path,ftp_addr, ftp_path)

if __name__ == '__main__':
    main()
