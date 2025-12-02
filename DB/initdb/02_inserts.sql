-- Dispositivo fictício para testes
INSERT INTO IoT (localizacao, status, gaiola)
VALUES ('Setor de testes', 'ativo', 1);

-- O hash abaixo é o bcrypt da senha '123456'
INSERT INTO usuario (nome, email, senha, cargo)
VALUES ('john Doe', 'john@demeter.com', '$2b$12$tB0cKz1jE9RjX2m4f0gP6.v0.W4Y8hYhJ3dE5O5L0zK0jP1q2O', 'Administrador');


-- INSERÇÃO DAS 100 IMAGENS PADRÃO PARA TESTE
-- Das datas de 04/11/2025 até 28/11/2025 (4 fotos/dia)

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-04 08:12:45', 'I001-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-04 10:33:12', 'I002-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-04 14:55:54', 'I003-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-04 17:22:18', 'I004-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-05 07:44:31', 'I005-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-05 09:58:03', 'I006-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-05 13:15:44', 'I007-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-05 18:47:22', 'I008-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-06 08:21:10', 'I009-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-06 11:33:50', 'I010-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-06 14:09:05', 'I011-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-06 19:22:41', 'I012-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-07 07:13:22', 'I013-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-07 10:48:55', 'I014-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-07 15:22:11', 'I015-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-07 18:57:49', 'I016-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-08 08:55:10', 'I017-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-08 12:15:42', 'I018-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-08 16:40:08', 'I019-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-08 19:58:31', 'I020-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-09 07:01:20', 'I021-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-09 11:32:44', 'I022-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-09 14:12:55', 'I023-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-09 18:22:33', 'I024-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-10 08:11:22', 'I025-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-10 10:55:19', 'I026-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-10 15:31:02', 'I027-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-10 18:42:58', 'I028-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-11 07:33:14', 'I029-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-11 10:14:59', 'I030-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-11 14:22:31', 'I031-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-11 19:41:02', 'I032-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-12 08:44:03', 'I033-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-12 11:12:50', 'I034-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-12 15:01:15', 'I035-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-12 18:55:29', 'I036-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-13 07:21:44', 'I037-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-13 11:33:08', 'I038-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-13 14:12:51', 'I039-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-13 19:44:37', 'I040-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-14 08:09:40', 'I041-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-14 10:55:11', 'I042-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-14 15:49:23', 'I043-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-14 18:22:55', 'I044-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-15 07:55:12', 'I045-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-15 11:01:44', 'I046-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-15 14:22:03', 'I047-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-15 19:35:28', 'I048-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-16 08:44:19', 'I049-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-16 12:39:55', 'I050-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-16 16:55:10', 'I051-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-16 19:22:44', 'I052-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-17 07:21:05', 'I053-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-17 11:33:42', 'I054-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-17 14:44:28', 'I055-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-17 18:57:39', 'I056-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-18 08:41:33', 'I057-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-18 12:14:05', 'I058-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-18 15:01:50', 'I059-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-18 19:29:33', 'I060-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-19 07:55:22', 'I061-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-19 11:09:44', 'I062-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-19 14:55:31', 'I063-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-19 18:41:02', 'I064-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-20 08:22:11', 'I065-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-20 11:33:44', 'I066-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-20 15:09:12', 'I067-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-20 19:55:01', 'I068-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-21 07:11:59', 'I069-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-21 10:54:33', 'I070-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-21 14:29:44', 'I071-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-21 18:55:12', 'I072-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-22 08:01:55', 'I073-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-22 11:22:37', 'I074-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-22 15:02:18', 'I075-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-22 19:33:49', 'I076-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-23 07:33:14', 'I077-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-23 11:01:51', 'I078-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-23 14:29:55', 'I079-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-23 18:55:24', 'I080-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-24 08:45:31', 'I081-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-24 12:55:44', 'I082-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-24 15:44:09', 'I083-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-24 19:11:52', 'I084-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-25 07:33:19', 'I085-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-25 11:41:33', 'I086-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-25 15:12:50', 'I087-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-25 18:55:11', 'I088-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-26 08:44:03', 'I089-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-26 11:22:44', 'I090-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-26 15:04:18', 'I091-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-26 19:22:10', 'I092-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-27 07:12:33', 'I093-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-27 10:55:49', 'I094-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-27 14:21:09', 'I095-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-27 19:33:51', 'I096-01-001.jpg');

INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-28 08:41:44', 'I097-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-28 12:19:31', 'I098-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-28 15:44:08', 'I099-01-001.jpg');
INSERT INTO banco_imagens (id_dispositivo, gaiola, tamanho, data_captura, caminho_arquivo) 
VALUES (1, 1, 0, '2025-11-28 19:55:22', 'I100-01-001.jpg');