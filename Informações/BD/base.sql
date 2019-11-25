CREATE DATABASE trab_asa;

CREATE SCHEMA trab_asa;

CREATE TABLE IF NOT EXISTS trab_asa.tb_user(
    id  SERIAL PRIMARY KEY,
    nome VARCHAR(30) NOT NULL,
    senha VARCHAR(60) NOT NULL,
    permissao INT NOT NULL
);

CREATE TABLE IF NOT EXISTS trab_asa.tb_admin(
    id  SERIAL NOT NULL,
    admin_id INT NOT NULL PRIMARY KEY,

    CONSTRAINT fk_admin_id FOREIGN KEY(admin_id)
        REFERENCES trab_asa.tb_user(id)
);

CREATE TABLE IF NOT EXISTS trab_asa.tb_professor(
    id SERIAL NOT NULL,
    professor_id INT NOT NULL PRIMARY KEY,
    afiliacao VARCHAR(50) NOT NULL,

    CONSTRAINT fk_professor_id FOREIGN KEY(professor_id)
        REFERENCES trab_asa.tb_user(id)
);

CREATE TABLE IF NOT EXISTS trab_asa.tb_aluno(
    id SERIAL NOT NULL,
    aluno_id INT NOT NULL PRIMARY KEY,
    curso VARCHAR(50) NOT NULL,

    CONSTRAINT fk_aluno_id FOREIGN KEY(aluno_id)
        REFERENCES trab_asa.tb_user(id)
);

CREATE TABLE IF NOT EXISTS trab_asa.tb_materia(
    id SERIAL NOT NULL PRIMARY KEY,
    prof_id INT NOT NULL,
    curso VARCHAR(50) NOT NULL,

    CONSTRAINT fk_prof_id FOREIGN KEY(prof_id)
        REFERENCES trab_asa.tb_professor(professor_id)
);

CREATE TABLE IF NOT EXISTS trab_asa.tb_nota(
    id SERIAL NOT NULL PRIMARY KEY,
    aluno_id INT NOT NULL,
    mat_id INT NOT NULL,
    nota INT NOT NULL,

    CONSTRAINT fk_aluno_id FOREIGN KEY(aluno_id)
        REFERENCES trab_asa.tb_aluno(aluno_id),
    CONSTRAINT fk_mat_id FOREIGN KEY(mat_id)
        REFERENCES trab_asa.tb_materia(id)
);

INSERT INTO trab_asa.tb_user(nome, senha, permissao) VALUES ('admin', 'nimda', 3);
INSERT INTO trab_asa.tb_admin(admin_id) VALUES (1);