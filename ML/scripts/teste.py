import time
from ultralytics import YOLO
import cv2
import os
import glob
import shutil

# Caminho do modelo treinado
modelo_path = "../runs/detect/train2/weights/best.pt"

# Diretórios IoT
input_dir = "../dataset/iot/input"
processed_dir = "../dataset/iot/processed"
error_dir = "../dataset/iot/error"

os.makedirs(input_dir, exist_ok=True)
os.makedirs(processed_dir, exist_ok=True)
os.makedirs(error_dir, exist_ok=True)

model = YOLO(modelo_path)


# ---------------------------------------------------------
# Extrai o ID entre a letra inicial (P/I/E) e o próximo "-"
# Ex:  P15-02-001.jpg  → 15
#      I3001-02-09.jpg → 3001
# Retorna -1 em caso de erro
# ---------------------------------------------------------
def extrair_id_numero(nome):
    if not nome or nome[0] not in ["P", "I", "E"]:
        return -1
    nome_sem_ext = os.path.splitext(nome)[0]
    resto = nome_sem_ext[1:]  # remove 'P'/'I'/'E'
    partes = resto.split("-", 1)
    if not partes:
        return -1
    id_str = partes[0]
    return int(id_str) if id_str.isdigit() else -1


# ---------------------------------------------------------
# Garante nome único no destino (adiciona _1, _2, ...)
# ---------------------------------------------------------
def unique_path(dest_dir, filename):
    base, ext = os.path.splitext(filename)
    candidate = filename
    counter = 1
    full = os.path.join(dest_dir, candidate)
    while os.path.exists(full):
        candidate = f"{base}_{counter}{ext}"
        full = os.path.join(dest_dir, candidate)
        counter += 1
    return full


# ---------------------------------------------------------
# Procura o maior ID já processado nas pastas processed e error
# ---------------------------------------------------------
def obter_ultimo_id_processado():
    arquivos = []
    for ext in ("jpg", "jpeg", "png", "bmp", "webp"):
        arquivos.extend(glob.glob(os.path.join(processed_dir, f"*.{ext}")))
        arquivos.extend(glob.glob(os.path.join(error_dir, f"*.{ext}")))

    if not arquivos:
        return -1

    ids = [extrair_id_numero(os.path.basename(f)) for f in arquivos]
    ids_filtrados = [i for i in ids if i >= 0]
    return max(ids_filtrados) if ids_filtrados else -1


# ---------------------------------------------------------
# Se não houver histórico, começar do menor ID da pasta input
# Retorna último_id_processado inicial (menor_input - 1) ou -1 se não houver nada
# ---------------------------------------------------------
def obter_inicio_pela_input(se_ultimo):
    if se_ultimo != -1:
        return se_ultimo  # Já existe histórico

    imagens_input = []
    for ext in ("jpg", "jpeg", "png", "bmp", "webp"):
        imagens_input.extend(glob.glob(os.path.join(input_dir, f"*.{ext}")))

    if not imagens_input:
        return -1  # Nada para processar

    ids_input = [extrair_id_numero(os.path.basename(i)) for i in imagens_input]
    ids_input = [i for i in ids_input if i >= 0]

    if not ids_input:
        return -1

    menor_id = min(ids_input)
    return menor_id - 1  # Para garantir que o menor ainda será processado


# ---------------------------------------------------------
# Inicia ponteiro
# ---------------------------------------------------------
ultimo_id_processado = obter_ultimo_id_processado()
ultimo_id_processado = obter_inicio_pela_input(ultimo_id_processado)

print("\n>>> Ponteiro inicial:")
print(f"→ ultimo_id_processado = {ultimo_id_processado}\n")
print(">>> Monitorando novas imagens...\n")


# ---------------------------------------------------------
# LOOP INFINITO
# ---------------------------------------------------------
while True:
    imagens = []
    for ext in ("jpg", "jpeg", "png", "bmp", "webp"):
        imagens.extend(glob.glob(os.path.join(input_dir, f"*.{ext}")))

    if imagens:
        # Ordena imagens pelo ID usando o extrator (IDs inválidos viram -1 e ficam no começo)
        imagens.sort(key=lambda p: extrair_id_numero(os.path.basename(p)))
        # Vamos procurar a primeira imagem com ID > ponteiro e processá-la (mantendo comportamento incremental)
        proxima = None
        for p in imagens:
            nome = os.path.basename(p)
            id_atual = extrair_id_numero(nome)
            if id_atual > ultimo_id_processado:
                proxima = p
                break

        if proxima is None:
            print("Nenhuma nova imagem para processar.")
            time.sleep(1)
            continue

        ultima_imagem = proxima
        nome_original = os.path.basename(ultima_imagem)
        id_atual = extrair_id_numero(nome_original)

        print("\n-----------------------------")
        print(f"Ponteiro atual: {ultimo_id_processado}")
        print(f"ID da próxima imagem na input: {id_atual}")
        print(f"Arquivo: {nome_original}")
        print("-----------------------------")

        try:
            results = model(ultima_imagem)
            annotated_img = results[0].plot()
            boxes = results[0].boxes

            if boxes is not None and len(boxes) > 0:
                adults = sum(1 for c in boxes.cls if model.names.get(int(c), "") == "BL_adulto")
                eggs = sum(1 for c in boxes.cls if model.names.get(int(c), "") == "BL_ovo")
                print(f"→ Detectado: {adults} adultos | {eggs} ovos")
                novo_nome = "P" + nome_original[1:]
                destino_dir = processed_dir
            else:
                print("→ Nenhum objeto detectado.")
                novo_nome = "E" + nome_original[1:]
                destino_dir = error_dir

            destino_path = unique_path(destino_dir, novo_nome)
            # annotated_img pode ser um numpy array (BGR) ou PIL; cv2.imwrite espera BGR numpy
            if isinstance(annotated_img, (list, tuple)):
                # safety: se for lista, pega o primeiro item
                annotated_img = annotated_img[0]
            cv2.imwrite(destino_path, annotated_img)
            print(f"→ Imagem salva em: {destino_path}")

        except Exception as e:
            print(f"❌ Erro ao processar {nome_original}: {e}")
            novo_nome = "E" + nome_original[1:]
            dest_err = unique_path(error_dir, novo_nome)
            shutil.copy2(ultima_imagem, dest_err)
            print(f"→ Copiado para pasta de erro: {dest_err}")

        # Atualiza ponteiro
        ultimo_id_processado = id_atual
        print(f"→ Ponteiro atualizado para: {ultimo_id_processado}")

    else:
        # sem imagens
        pass

    time.sleep(1)
