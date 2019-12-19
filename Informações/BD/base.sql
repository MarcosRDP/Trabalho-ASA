CREATE DATABASE trab_asa;

CREATE SCHEMA trab_asa;

CREATE TABLE IF NOT EXISTS trab_asa.tb_user(
    id SERIAL PRIMARY KEY,
    nome VARCHAR(30) NOT NULL,
    senha VARCHAR(60) NOT NULL,
    permissao INT NOT NULL,

    CONSTRAINT pk_user_id PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS trab_asa.tb_admin(
    id  SERIAL NOT NULL UNIQUE,
    admin_id INT NOT NULL UNIQUE,
    admin_mat VARCHAR(30),
    CONSTRAINT fk_admin_id FOREIGN KEY(admin_id)
        REFERENCES trab_asa.tb_user(id),
    CONSTRAINT pk_admin_id PRIMARY KEY (admin_mat)
);

CREATE TABLE IF NOT EXISTS trab_asa.tb_professor(
    id SERIAL NOT NULL UNIQUE,
    professor_id INT NOT NULL UNIQUE,
    professor_mat VARCHAR(30),
    afiliacao VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,

    CONSTRAINT fk_professor_id FOREIGN KEY(professor_id)
        REFERENCES trab_asa.tb_user(id),
    CONSTRAINT pk_professor_id PRIMARY KEY (professor_mat)
);

CREATE TABLE IF NOT EXISTS trab_asa.tb_aluno(
    id SERIAL NOT NULL UNIQUE,
    aluno_id INT NOT NULL UNIQUE,
    aluno_mat VARCHAR(30),
    curso VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    CONSTRAINT fk_aluno_id FOREIGN KEY(aluno_id)
        REFERENCES trab_asa.tb_user(id),
    CONSTRAINT pk_aluno_id PRIMARY KEY (aluno_mat)
);

CREATE TABLE IF NOT EXISTS trab_asa.tb_materia(
    id SERIAL,
    prof_id INT NOT NULL,
    curso VARCHAR(50) NOT NULL UNIQUE,

    CONSTRAINT fk_prof_id FOREIGN KEY(prof_id)
        REFERENCES trab_asa.tb_professor(professor_id),
    CONSTRAINT pk_materia_id PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS trab_asa.tb_nota(
    id SERIAL NOT NULL UNIQUE,
    aluno_id INT,
    mat_id INT,
    nota INT NOT NULL,

    CONSTRAINT fk_aluno_id FOREIGN KEY(aluno_id)
        REFERENCES trab_asa.tb_aluno(aluno_id),
    CONSTRAINT fk_mat_id FOREIGN KEY(mat_id)
        REFERENCES trab_asa.tb_materia(id),
    CONSTRAINT pk_nota_id PRIMARY KEY (aluno_id, mat_id)
);

INSERT into trab_asa.tb_user (nome,senha,permissao) VALUES ('Admin','123',3);
INSERT INTO trab_asa.tb_admin (admin_id,admin_mat) VALUES (1,'11921UFU1');
