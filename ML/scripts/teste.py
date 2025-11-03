from ultralytics import YOLO
import cv2
import os
import glob
import shutil

# Caminho do modelo treinado (best.pt)
modelo_path = "../runs/detect/train2/weights/best.pt"

# Diretórios IoT
input_dir = "../dataset/iot/input"
processed_dir = "../dataset/iot/processed"
error_dir = "../dataset/iot/error"

# Extensão padrão
DEFAULT_EXT = "jpg"

# Cria as pastas se não existirem
os.makedirs(processed_dir, exist_ok=True)
os.makedirs(error_dir, exist_ok=True)

# Carrega o modelo YOLO
model = YOLO(modelo_path)

# Lista imagens da pasta input
imagens = []
for ext in ("jpg", "jpeg", "png", "bmp", "webp"):
    imagens.extend(glob.glob(os.path.join(input_dir, f"*.{ext}")))

if not imagens:
    print("Nenhuma imagem encontrada em:", input_dir)
    exit()

print(f"{len(imagens)} imagens encontradas. Iniciando detecção...\n")

# Função auxiliar para nome único
def unique_path(dest_dir, filename):
    base, ext = os.path.splitext(filename)
    candidate = filename
    counter = 1
    while os.path.exists(os.path.join(dest_dir, candidate)):
        candidate = f"{base}_{counter}{ext}"
        counter += 1
    return os.path.join(dest_dir, candidate)

# -------------------- PROCESSAMENTO -------------------------------
total_imgs = 0
imgs_com_detect = 0
imgs_sem_detect = 0
imgs_erro = 0
total_adultos = 0
total_ovos = 0

for idx, imagem_path in enumerate(imagens, start=1):
    nome_original = os.path.basename(imagem_path)
    print(f"[{idx}/{len(imagens)}] Processando: {nome_original}")
    total_imgs += 1

    try:
        results = model(imagem_path)
        annotated_img = results[0].plot()

        # Obtém classes detectadas
        boxes = results[0].boxes
        if boxes is not None and len(boxes) > 0:
            # Conta adultos e ovos
            adults = sum(1 for c in boxes.cls if model.names[int(c)] == "BL_adulto")
            eggs = sum(1 for c in boxes.cls if model.names[int(c)] == "BL_ovo")

            total_adultos += adults
            total_ovos += eggs

            novo_nome = f"P{nome_original[1:]}" if nome_original.startswith("I") else f"P{nome_original}"
            destino_dir = processed_dir
            imgs_com_detect += 1

            print(f"→ {adults} adultos e {eggs} ovos detectados.")
        else:
            novo_nome = f"E{nome_original[1:]}" if nome_original.startswith("I") else f"E{nome_original}"
            destino_dir = error_dir
            imgs_sem_detect += 1
            print("→ Nenhum objeto detectado.")

        # Salva a imagem anotada
        destino_path = unique_path(destino_dir, novo_nome)
        cv2.imwrite(destino_path, annotated_img)
        print(f"Imagem anotada salva em: {destino_path}\n")

    except Exception as e:
        imgs_erro += 1
        print(f"❌ Erro ao processar {nome_original}: {e}")
        erro_nome = f"E{nome_original[1:]}" if nome_original.startswith("I") else f"E{nome_original}"
        shutil.copy2(imagem_path, unique_path(error_dir, erro_nome))

# -------------------- RESUMO FINAL -------------------------------
print("\n----- RESUMO FINAL -----")
print(f"Total de imagens processadas: {total_imgs}")
print(f"Imagens com detecção: {imgs_com_detect}")
print(f"Imagens sem detecção: {imgs_sem_detect}")
print(f"Erros: {imgs_erro}")
print(f"Total detectado → Adultos: {total_adultos} | Ovos: {total_ovos}")
print("[ Processamento concluído ]")
