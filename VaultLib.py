import os
import base64
import json
import secrets
import string
import subprocess
import shutil
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken

class Vault:
    def __init__(self, vault_name:str, master_password, out_image, mask_source = None, signature: bytes = b"NEO_SPACE_MARKER", user: str = 'Default', os: str = "Arch Linux", show_logo: bool = False):
        self.db_path = out_image
        self.mask_source = mask_source

        self.vault_name = vault_name
        self.user = user
        self.os = os

        self.salt_size = 16
        self.signature = signature
        
        # Печатаем приветствие в стиле Arch
        if show_logo:
            self._print_logo()
        
        self.salt = self._get_or_create_salt()
        self.key = self._derive_key(master_password)
        self.cipher = Fernet(self.key)

    def _print_logo(self):
        """Просто потому что I use Arch btw"""
        print(f"""
                   -`                    
                  .o+`                   [ {self.vault_name} ]
                 `ooo/                   [ User: {self.user} ]
                `+oooo:                  [ OS: {self.os} ]
               `+oooooo:                 [ Status: Encrypted ]
               -+oooooo+:                
             `/:-:++oooo+:               [ Mask: {self.mask_source} ]
            `/++++/+++++++:              [ Source: {self.db_path} ]
           `/++++++++++++++:
          `/+++ooooooooooooo/`
         ./ooossssqssoooossssw`
        .oossssso-````/ossssss+
       -osssssso.      :ssssssso.
      :osssssss/        ossssoooo.
     /ossssssss/        ossssoooo.
    /osssssoooo/        ossssoooo.
    """)

    def _show_decoy(self):
        if os.path.exists(self.db_path):
            try:
                subprocess.Popen(['xdg-open', self.db_path], 
                                 stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL)
            except Exception: pass

    def _get_or_create_salt(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "rb") as f:
                content = f.read()
                idx = content.find(self.signature)
                if idx != -1:
                    start = idx + len(self.signature)
                    return content[start : start + self.salt_size]
        return os.urandom(self.salt_size)

    def _derive_key(self, password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=200000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def _save_db(self, data):
        if os.path.exists(self.db_path):
            with open(self.db_path, "rb") as f:
                content = f.read()
                idx = content.find(self.signature)
                image_base = content[:idx] if idx != -1 else content
        elif self.mask_source and os.path.exists(self.mask_source):
            with open(self.mask_source, "rb") as f:
                image_base = f.read()
        else:
            image_base = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")

        with open(self.db_path, "wb") as f:
            f.write(image_base)
            f.write(self.signature)
            f.write(self.salt)
            encrypted_data = self.cipher.encrypt(json.dumps(data).encode())
            f.write(encrypted_data)

    def _load_db(self):
        if not os.path.exists(self.db_path): return {}
        try:
            with open(self.db_path, "rb") as f:
                content = f.read()
                idx = content.find(self.signature)
                if idx == -1: return {}
                data_start = idx + len(self.signature) + self.salt_size
                decrypted_json = self.cipher.decrypt(content[data_start:]).decode()
                return json.loads(decrypted_json)
        except Exception: return {}

    def get_services(self) -> list[str] | None:
        """Возвращает список всех сохраненных сервисов"""
        to_ret: list[str] = []

        data = self._load_db()
        if not data:
            print("[!] Секреты не найдены или неверный пароль.")
            return None

        for i, service in enumerate(data.keys(), 1):
            to_ret.append(service)

        return to_ret

    def list_entries(self):
        """Выводит список всех сохраненных сервисов"""
        data = self._load_db()
        if not data:
            print("[!] Секреты не найдены или неверный пароль.")
            return
        
        print("\n" + "─" * 30)
        print(f"{'#':<3} | {'СЕРВИС':<20}")
        print("─" * 30)
        for i, service in enumerate(data.keys(), 1):
            print(f"{i} | {service}")
            # print(f"{i:<3} | {service:<20}")
        print("─" * 30 + "\n")

    def add_entry(self, service, login, length=20):
        """
        Добавить Сервис, Логин, Пароль в хранилище
        """
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        data = self._load_db()
        data[service] = {"login": login, "password": password}
        self._save_db(data)
        print(f"[+] Успешно скрыто в {self.db_path}")
        return password
    
    def remove_entry(self, service: str) -> bool:
        """
        Удаляет сервис из хранилища.
        Возвращает True при успешном удалении, иначе False.
        """
        data = self._load_db()
        
        if not data:
            print(f"[!] Ошибка доступа или база пуста при попытке удаления {service}")
            return False
            
        if service in data:
            del data[service]
            self._save_db(data)
            print(f"[-] Сервис '{service}' успешно удален из {self.db_path}")
            return True
        else:
            print(f"[?] Сервис '{service}' не найден в базе.")
            return False

    def get_entry(self, service):
        data = self._load_db()
        if not data: return [1, "Доступ запрещен или база пуста"]
        if service not in data: return [0, "Не найдено"]
        return [2, data[service]]

if __name__ == '__main__':
    vault = Vault(vault_name="NeoVault", signature=b"NEO_SPACE_MARKER", master_password="Aleksey_Secure_2026", user='Alex', out_image="cat.png", mask_source="mask_cat.jpg")

    # Показать список:
    vault.list_entries()

    services = vault.get_services()

    if services:
        for service in services:
            # Прочитать:
            res = vault.get_entry(service)
            if res[0] == 2:
                print(f"[S] Сервис: {service} | Логин: {res[1]['login']} | Пасс: {res[1]['password']}")
            elif res[0] == 1:
                print('[!] Неверный мастер-пароль')