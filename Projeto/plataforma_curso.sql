CREATE SCHEMA plataforma_curso;
USE plataforma_curso;

CREATE TABLE IF NOT EXISTS usuario(
    id INT AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    cpf_cnpj VARCHAR(255) NOT NULL,
    senha CHAR(15) NOT NULL,
    atividade char(4) 
    CONSTRAINT pk_id_usuario PRIMARY KEY (id),
    CONSTRAINT uk_email_usuario UNIQUE (email),
    CONSTRAINT uk_cpf_cnpj_usuario UNIQUE (cpf_cnpj)                                                                                                                     
);


SELECT * FROM usuario;
