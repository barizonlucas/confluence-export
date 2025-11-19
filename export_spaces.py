from atlassian import Confluence
import os
import requests

# ========= CONFIGURAÇÕES MANUAIS =========
CONF_OLD_URL = "https://entelgy.atlassian.net/wiki"
CONF_OLD_USER = ""
CONF_OLD_TOKEN = ""
SPACES_FILE = "spaces.txt"
EXPORT_DIR = "exports"
# =========================================


def export_space(confluence, space_key: str):
    print(f"=== Exportando space: {space_key} ===")

    # dispara o export e obtém a URL do arquivo gerado
    export_url = confluence.get_space_export(
        space_key=space_key,
        export_type="xml",
    )
    print(f"URL de export gerada: {export_url}")

    # baixa o arquivo gerado
    resp = requests.get(export_url, auth=(CONF_OLD_USER, CONF_OLD_TOKEN), stream=True)
    resp.raise_for_status()

    os.makedirs(EXPORT_DIR, exist_ok=True)
    file_path = os.path.join(EXPORT_DIR, f"{space_key}.xml.zip")
    with open(file_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print(f">>> Space {space_key} exportado para {file_path}\n")


def main():
    print("Iniciando script de export de spaces...")

    # valida arquivo spaces.txt
    if not os.path.exists(SPACES_FILE):
        print(f"ERRO: Arquivo {SPACES_FILE} não encontrado na pasta atual.")
        print(f"Pasta atual: {os.getcwd()}")
        return

    # inicializa o cliente Confluence
    try:
        confluence = Confluence(
            url=CONF_OLD_URL,
            username=CONF_OLD_USER,
            password=CONF_OLD_TOKEN,
        )
        print("Conexão com Confluence inicializada.")
    except Exception as e:
        print("ERRO ao inicializar Confluence:")
        print(e)
        return

    # lê lista de spaces
    with open(SPACES_FILE, "r", encoding="utf-8") as f:
        space_keys = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not space_keys:
        print(f"ERRO: {SPACES_FILE} está vazio ou só tem comentários.")
        return

    print(f"Spaces a exportar: {space_keys}")

    for space_key in space_keys:
        try:
            export_space(confluence, space_key)
        except Exception as e:
            print(f"ERRO ao exportar space {space_key}:")
            print(e)

    print("✅ Fim do script.")


if __name__ == "__main__":
    main()
