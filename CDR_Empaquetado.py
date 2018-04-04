import zipfile
import sys
import hashlib
import glob

file_list=glob.glob('*.csv')
# print(file_list)

for file in file_list:
    param=file.split('.')
    zfile = zipfile.ZipFile(param[0] + '.zip', mode='w')
    zfile.write(file, compress_type=zipfile.ZIP_DEFLATED)
    zfile.close()

zip_list= glob.glob('*.zip')
# print(zip_list)

for zip in zip_list:

    sha_256 = hashlib.sha256()
    param = zip.split('.')

    with open(zip,"rb") as f:
        # Read and update hash string value in blocks of 4K
        bytes = f.read()  # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest()
        # print(readable_hash)
    f.close()

    sha256_file = open(param[0] + '.sha256', 'w+')
    sha256_file.write(readable_hash)
    sha256_file.close()