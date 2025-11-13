import os
import glob

# --- Configuração ---
# ATENÇÃO: Verifique se estes caminhos estão corretos
# O script vai deletar TODOS os arquivos dentro destas pastas.

# Baseado no seu pedido, os caminhos são:
processed_dir = "../dataset/iot/processed"
error_dir = "../dataset/iot/error"

# Lista de pastas que serão limpas
diretorios_para_limpar = [processed_dir, error_dir]
# --------------------

def limpar_pasta(path_da_pasta):
    """
    Deleta todos os arquivos dentro de uma pasta específica.
    Não deleta sub-pastas, apenas arquivos.
    """
    print(f"--- Processando pasta: {path_da_pasta} ---")

    # Verifica se o diretório existe
    if not os.path.exists(path_da_pasta):
        print(f"AVISO: Pasta não encontrada. Pulando: {path_da_pasta}\n")
        return

    # Encontra todos os arquivos na pasta (usando *.* para pegar qualquer extensão)
    arquivos = glob.glob(os.path.join(path_da_pasta, "*"))

    if not arquivos:
        print("Pasta já está vazia.\n")
        return

    arquivos_deletados = 0
    erros = 0

    for f_path in arquivos:
        try:
            # Importante: Garante que é um ARQUIVO antes de tentar deletar
            # Isso evita erros ao tentar deletar uma sub-pasta
            if os.path.isfile(f_path):
                os.remove(f_path)
                arquivos_deletados += 1
            elif os.path.isdir(f_path):
                print(f"Aviso: Ignorando sub-pasta: {f_path}")

        except Exception as e:
            print(f"ERRO ao deletar o arquivo {f_path}: {e}")
            erros += 1

    print(f"Sucesso: {arquivos_deletados} arquivos deletados.")
    if erros > 0:
        print(f"Falhas: {erros} arquivos não puderam ser deletados.")
    print("") # Linha em branco para separar

# --- Execução Principal ---
print("Iniciando limpeza das pastas 'processed' e 'error'...\n")

for pasta in diretorios_para_limpar:
    limpar_pasta(pasta)

print("===== Limpeza Concluída =====")