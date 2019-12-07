CREATE DATABASE trab_asa;

CREATE SCHEMA trab_asa;

CREATE TABLE IF NOT EXISTS trab_asa.tb_user(
    id VARCHAR(20),
    nome VARCHAR(30) NOT NULL,
    senha VARCHAR(60) NOT NULL,
    permissao INT NOT NULL,

    CONSTRAINT pk_user_id PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS trab_asa.tb_admin(
    id  SERIAL NOT NULL UNIQUE,
    admin_id VARCHAR(20),

    CONSTRAINT fk_admin_id FOREIGN KEY(admin_id)
        REFERENCES trab_asa.tb_user(id),
    CONSTRAINT pk_admin_id PRIMARY KEY (admin_id)
);

CREATE TABLE IF NOT EXISTS trab_asa.tb_professor(
    id SERIAL NOT NULL UNIQUE,
    professor_id VARCHAR(20),
    afiliacao VARCHAR(50) NOT NULL,

    CONSTRAINT fk_professor_id FOREIGN KEY(professor_id)
        REFERENCES trab_asa.tb_user(id),
    CONSTRAINT pk_professor_id PRIMARY KEY (professor_id)
);

CREATE TABLE IF NOT EXISTS trab_asa.tb_aluno(
    id SERIAL NOT NULL UNIQUE,
    aluno_id VARCHAR(20),
    curso VARCHAR(50) NOT NULL,

    CONSTRAINT fk_aluno_id FOREIGN KEY(aluno_id)
        REFERENCES trab_asa.tb_user(id),
    CONSTRAINT pk_aluno_id PRIMARY KEY (aluno_id)
);

CREATE TABLE IF NOT EXISTS trab_asa.tb_materia(
    id SERIAL,
    prof_id VARCHAR(20) NOT NULL,
    curso VARCHAR(50) NOT NULL,

    CONSTRAINT fk_prof_id FOREIGN KEY(prof_id)
        REFERENCES trab_asa.tb_professor(professor_id),
    CONSTRAINT pk_materia_id PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS trab_asa.tb_nota(
    id SERIAL NOT NULL UNIQUE,
    aluno_id VARCHAR(20),
    mat_id INT,
    nota INT NOT NULL,

    CONSTRAINT fk_aluno_id FOREIGN KEY(aluno_id)
        REFERENCES trab_asa.tb_aluno(aluno_id),
    CONSTRAINT fk_mat_id FOREIGN KEY(mat_id)
        REFERENCES trab_asa.tb_materia(id),
    CONSTRAINT pk_nota_id PRIMARY KEY (aluno_id, mat_id)
);

INSERT INTO trab_asa.tb_user(id, nome, senha, permissao) VALUES ('admin', 'admin', 'nimda', 3);
INSERT INTO trab_asa.tb_admin(admin_id) VALUES ('admin');
