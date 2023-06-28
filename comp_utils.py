import gzip
import shutil
def compress(file_in, file_out):
    with open(file_in, "rb") as fin, gzip.open(file_out, "wb") as fout:
        shutil.copyfileobj(fin, fout)

def decompress(file_in, file_out):
    with gzip.open(file_in, "rb") as fin, open(file_out, "wb") as fout:
        shutil.copyfileobj(fin, fout)