from ultralytics import YOLO
import cv2
import os

# Carrega o modelo treinado
model = YOLO("runs/detect/train3/weights/best.pt")

# Caminho da imagem a testar
imagem_path = "val/images/2.jpg"

# Faz a predição
results = model(imagem_path)

# Cria pasta de saída
os.makedirs("tratados", exist_ok=True)

# Gera nome incremental para saída
base_name = "resultado_teste"
ext = ".jpg"
count = 1
while True:
    saida_path = os.path.join("tratados", f"{base_name}_{count}{ext}")
    if not os.path.exists(saida_path):
        break
    count += 1

# Salva imagem anotada
annotated_img = results[0].plot()
cv2.imwrite(saida_path, annotated_img)
print(f"Imagem anotada salva em: {saida_path}")

# Mostra na tela
results[0].show()

# Mostra contagem
num = len(results[0].boxes)
print(f"Foram detectados {num} bichos lixeiros adultos.")
