from ultralytics import YOLO
import cv2
import os
import glob
import shutil

# Caminho do modelo treinado (best.pt)
modelo_path = "../runs/detect/train/weights/best.pt"

# Diretórios_IoT
input_dir = "../dataset/iot/input"
processed_dir = "../dataset/iot/processed"
error_dir = "../dataset/iot/error"

# Extensão padrão
DEFAULT_EXT = "jpg"

# Garante que as pastas existam
os.makedirs(processed_dir, exist_ok=True)
os.makedirs(error_dir, exist_ok=True)

# modelo YOLO
model = YOLO(modelo_path)

# Lista imagens da pasta input
imagens = []
for ext in ("jpg", "jpeg", "png", "bmp", "webp"):
    imagens.extend(glob.glob(os.path.join(input_dir, f"*.{ext}")))

if not imagens:
    print("Nenhuma imagem encontrada em:", input_dir)
    exit()

print(f"{len(imagens)} imagens encontradas. Iniciando detecção...\n")

# Helper: gera um nome único na pasta destino para evitar sobrescrever
def unique_path(dest_dir, filename):
    base, ext = os.path.splitext(filename)
    candidate = filename
    counter = 1
    while os.path.exists(os.path.join(dest_dir, candidate)):
        candidate = f"{base}_{counter}{ext}"
        counter += 1
    return os.path.join(dest_dir, candidate)

# -------------------- PROCESSAMENTO -------------------------------
total = 0
sucesso = 0
sem_detect = 0
erros = 0

for idx, imagem_path in enumerate(imagens, start=1):
    nome_original = os.path.basename(imagem_path)
    print(f"[{idx}/{len(imagens)}] Processando: {nome_original}")

    # define extensão (preserva a mesma do arquivo original)
    _, ext = os.path.splitext(nome_original)
    if not ext:
        ext = "." + DEFAULT_EXT

    total += 1
    try:
        # Faz a predição (resultados)
        results = model(imagem_path)
        annotated_img = results[0].plot()  # numpy array (BGR)

        # Conta as detecções
        num_bichos = len(results[0].boxes)

        # Monta o novo nome (remove prefixo I se existir)
        if nome_original.startswith("I"):
            base_nome = nome_original[1:]
        else:
            base_nome = nome_original

        if num_bichos > 0:
            novo_nome = f"P{base_nome}"
            destino_dir = processed_dir
            sucesso += 1
        else:
            novo_nome = f"E{base_nome}"
            destino_dir = error_dir
            sem_detect += 1

        # Garante nome único na pasta destino
        destino_path = unique_path(destino_dir, novo_nome)

        # Salva a imagem anotada no destino
        cv2.imwrite(destino_path, annotated_img)

        if num_bichos > 0:
            print(f"{num_bichos} bichos lixeiros detectados. Anotada salva em: {destino_path}\n")
        else:
            print(f"Nenhum bicho lixeiro detectado. Anotada salva em (error): {destino_path}\n")

    except Exception as e:
        erros += 1
        print(f"Erro ao processar {nome_original}: {e}")

        # Cria nome com prefixo 'E' e salva/copia o original para pasta de erro
        erro_nome = f"E{nome_original[1:]}" if nome_original.startswith("I") else f"E{nome_original}"
        destino_path = unique_path(error_dir, erro_nome)
        try:
            shutil.copy2(imagem_path, destino_path)
            print(f"Original copiado para pasta de erro como: {destino_path}\n")
        except Exception as e2:
            print(f"Falha ao copiar arquivo para error/: {e2}\n")

print("----- Resumo -----")
print(f"Total processadas: {total}")
print(f"Com detecção (salvas em processed): {sucesso}")
print(f"Sem detecção (salvas em error): {sem_detect}")
print(f"Erros durante processamento: {erros}")
print("[ Processamento concluído ]")
