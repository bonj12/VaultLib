import VaultLib as vl

vault = vl.Vault(vault_name="NeoVault",
                 signature=b"NEO_SPACE_MARKER",
                 master_password="Aleksey_Secure_2026",
                 user='Alex',
                 out_image="cat.png",
                 mask_source="mask_cat.jpg",
                 show_logo=True)

# Показать список:
vault.list_entries()

services = vault.get_services()

# vault._show_decoy()

if services:
    for service in services:
        # Прочитать:
        res = vault.get_entry(service)
        if res[0] == 2:
            print(f"[S] Сервис: {service} | Логин: {res[1]['login']} | Пасс: {res[1]['password']}")
        elif res[0] == 1:
            print('[!] Неверный мастер-пароль')