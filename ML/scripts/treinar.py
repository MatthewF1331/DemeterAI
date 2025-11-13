from ultralytics import YOLO

# Criação do modelo base (versão nano)
model = YOLO("yolov8n.pt")

model.train(
    data="../dataset/data.yaml",      # caminho para o arquivo .yaml
    epochs=100,                       # número de ciclos de treino
    imgsz=640,                        # tamanho das imagens
    project="../runs/detect",         # pasta dos resultados
    name="train",                     # nome do teste
)
