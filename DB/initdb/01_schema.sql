CREATE TABLE IoT (
    id_dispositivo SERIAL PRIMARY KEY,
    localizacao VARCHAR(100),
    status VARCHAR(50),
    gaiola INT NOT NULL
);

CREATE INDEX idx_iot_gaiola ON IoT(gaiola);

CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    cargo VARCHAR(150) NOT NULL
);

CREATE INDEX idx_usuario_nome ON usuario(nome);

CREATE TABLE banco_imagens (
    id SERIAL PRIMARY KEY,
    id_dispositivo INT NOT NULL,
    gaiola INT NOT NULL,
    tamanho BIGINT NOT NULL,
    data_captura TIMESTAMP NOT NULL,
    caminho_arquivo TEXT NOT NULL,

    CONSTRAINT fk_dispositivo
        FOREIGN KEY (id_dispositivo)
        REFERENCES IoT(id_dispositivo)
        ON DELETE CASCADE
);

CREATE INDEX idx_banco_imagens_dispositivo ON banco_imagens(id_dispositivo);
CREATE INDEX idx_banco_imagens_data ON banco_imagens(data_captura);
CREATE INDEX idx_banco_imagens_gaiola ON banco_imagens(gaiola);

CREATE TABLE dados_ML (
    id_processamento SERIAL PRIMARY KEY,
    id_imagem INT NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    previsao_media NUMERIC(5,2) NOT NULL,
    velocidade_cpu NUMERIC(10,3),
    versao_modelo VARCHAR(50),
    data_processamento TIMESTAMP DEFAULT now(),
    parametros JSONB,

    CONSTRAINT fk_imagem
        FOREIGN KEY (id_imagem)
        REFERENCES banco_imagens(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_ml_imagem ON dados_ML(id_imagem);
CREATE INDEX idx_ml_data ON dados_ML(data_processamento);

CREATE TABLE dados_resultado (
    id_resultado SERIAL PRIMARY KEY,
    id_processamento INT NOT NULL,

    sexo CHAR(1) NOT NULL DEFAULT 'N',
    quantidade_insetos INT NOT NULL,
    etapa_ciclo VARCHAR(50),
    precisao NUMERIC(5,2) NOT NULL,

    CONSTRAINT sex_check CHECK (sexo IN ('M', 'F', 'N')),

    CONSTRAINT fk_processamento
        FOREIGN KEY (id_processamento)
        REFERENCES dados_ML(id_processamento)
        ON DELETE CASCADE
);

CREATE INDEX idx_resultado_processamento ON dados_resultado(id_processamento);
CREATE INDEX idx_resultado_sexo ON dados_resultado(sexo);
CREATE INDEX idx_resultado_etapa ON dados_resultado(etapa_ciclo);
