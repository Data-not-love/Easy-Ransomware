import RansomEncrypted
from RansomEncrypted import files,file,key
import os


def decrypting ():
    for decrypt_file in os.scandir():
        if decrypt_file.name.endswith('.encrypted'):
            print(decrypt_file.name)

