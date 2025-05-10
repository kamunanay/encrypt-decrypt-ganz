
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import os

def encrypt_file(file_path, password):
    with open(file_path, 'rb') as f:
        data = f.read()

    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    file_out = file_path + ".enc"
    with open(file_out, 'wb') as f:
        for x in (salt, cipher.nonce, tag, ciphertext):
            f.write(x)

    print(f"\n[✓] File terenkripsi disimpan sebagai: {file_out}")

def decrypt_file(file_path, password):
    with open(file_path, 'rb') as f:
        salt = f.read(16)
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()

    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_EAX, nonce)

    try:
        data = cipher.decrypt_and_verify(ciphertext, tag)
        out_path = file_path.replace(".enc", ".decrypted")
        with open(out_path, 'wb') as f:
            f.write(data)
        print(f"\n[✓] File berhasil didekripsi sebagai: {out_path}")
    except ValueError:
        print("\n[!] Password salah atau file rusak!")

def tampilkan_banner():
    os.system("clear")
    print("="*50)
    print("         Encrypt & Decrypt Tools By Ganzmods")
    print("="*50)
  
def main():
    tampilkan_banner()
    while True:
        print("\n[1] Enkripsi File")
        print("[2] Dekripsi File")
        print("[3] Keluar")
        pilihan = input("Pilih menu (1/2/3): ")

        if pilihan == "1":
            file = input("Masukkan nama file yang ingin dienkripsi: ")
            pw = input("Masukkan password rahasia: ")
            encrypt_file(file, pw)
        elif pilihan == "2":
            file = input("Masukkan file .enc yang ingin didekripsi: ")
            pw = input("Masukkan password: ")
            decrypt_file(file, pw)
        elif pilihan == "3":
            print("\n[✓] Terima kasih sudah pakai tools ini, sayang!")
            break
        else:
            print("[!] Pilihan tidak valid!")

if __name__ == "__main__":
    main()
