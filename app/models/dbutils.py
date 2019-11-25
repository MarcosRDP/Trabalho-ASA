from sqlalchemy import create_engine

class DbUtils:
    db_string = "postgresql+psycopg2://postgres:banco@localhost:10001/proj_asa"
    db_query = " "

    #CREATE functions

    def addNovoUsuario(self, nome, senha, permissao):
        db = create_engine(self.db_string)
        try:
            result = db.execute("INSERT INTO trab_asa.tb_user(nome, senha, permissao) VALUES (%s, %s, %s) RETURNING id;", nome, senha, permissao)
            res = result.fetchone()[0]
        except Exception as e:
            print("Problemas ao inserir na tabela usuario\n")
            print(e)
            res = False
        return res

    def addNovoProfessor(self, nome, senha, afiliacao):
        res01 = self.addNovoUsuario(nome, senha, 2)
        if(res01 == False):
            res = False
        else:
            db = create_engine(self.db_string)
            try:
                db.execute("INSERT INTO trab_asa.tb_professor(professor_id, afiliacao) VALUES (%s, %s)", res01, afiliacao)
                res = True
            except Exception as e:
                print("Problemas ao inserir na tabela professor\n")
                print(e)
                res = False
        return res

    def addNovoAluno(self, nome, senha, curso):
        res01 = self.addNovoUsuario(nome, senha, 1)
        if(res01 == False):
            res = False
        else:
            db = create_engine(self.db_string)
            try:
                db.execute("INSERT INTO trab_asa.tb_aluno(aluno_id, curso) VALUES (%s, %s)", res01, curso)
                res = True
            except Exception as e:
                print("Problemas ao inserir na tabela aluno\n")
                print(e)
                res = False
        return res

    def addNovaMateria(self, nome, curso):
        db = create_engine(self.db_string)
        try:
            result = db.execute("select use.id from trab_asa.tb_user use, trab_asa.tb_professor prof WHERE use.nome=%s AND use.id=prof.professor_id", nome)
            prof_id = result.fetchone()[0]
            db.execute("INSERT INTO trab_asa.tb_materia(prof_id, curso) VALUES (%s, %s)", prof_id, curso)
            res = True
        except Exception as e:
            print("Problemas ao inserir na tabela matéria\n")
            print(e)
            res = False
        return res

    def addNovaNota(self,aluno_id, nomeMateria, nota):
        db = create_engine(self.db_string)
        try:
            mat_id = db.execute("select id from trab_asa.tb_materia WHERE curso=%s;", nomeMateria).fetchone()[0]
            db.execute("INSERT INTO trab_asa.tb_nota(aluno_id, mat_id, nota) VALUES (%s, %s, %s);", aluno_id, mat_id, nota)
            res = True
        except Exception as e:
            print("Problemas ao inserir na tabela matéria\n")
            print(e)
            res = False
        return res



#    def addNovaNota(self, aluno_id, mat_id, 0):
#        db = create_engine(self.db_string)
#        try:
#            db.execute("INSERT INTO trab_asa.tb_nota(aluno_id, mat_id, nota) VALUES (%s, %s, %s);", aluno_id, mat_id, nota)
#            res = True
#        except Exception as e:
#            print("Problemas ao inserir na tabela matéria\n")
#            print(e)
#            res = False
#        return res

    #SELECT functions

    def NovoSelecionarUsuario(self, id):
        db = create_engine(self.db_string)
        try:
            result = db.execute("SELECT * FROM trab_asa.tb_user WHERE id=%s;", id)
            res = result.fetchone()
        except Exception as e:
            print("Problemas ao ler a tabela usuario\n")
            print(e)
            res = False
        return res

    def NovoSelecionarProfessor(self, id):
        db = create_engine(self.db_string)
        try:
            result = db.execute("SELECT use.id, use.nome, use.senha, use.permissao, prof.afiliacao FROM trab_asa.tb_user use, trab_asa.tb_professor prof WHERE use.id=%s AND prof.professor_id=use.id;", id)
            res = result.fetchone()
        except Exception as e:
            print("Problemas ao ler a tabela profesor\n")
            print(e)
            res = False
        return res

    def NovoSelecionarAluno(self, id):
        db = create_engine(self.db_string)
        try:
            result = db.execute("SELECT use.id, use.nome, use.senha, use.permissao, aluno.curso FROM trab_asa.tb_user use, trab_asa.tb_aluno aluno WHERE use.id=%s AND aluno.aluno_id=use.id;", id)
            res = result.fetchone()
        except Exception as e:
            print("Problemas ao ler a tabela profesor\n")
            print(e)
            res = False
        return res

    def NovoSelecionarMateriaID(self, id):
        db = create_engine(self.db_string)
        try:
            result = db.execute("SELECT use.id, use.nome, prof.afiliacao, mat.curso FROM trab_asa.tb_user use, trab_asa.tb_professor prof, trab_asa.tb_materia mat WHERE use.id=mat.prof_id AND prof.professor_id=use.id AND mat.id=%s;", id)
            res = result.fetchone()
        except Exception as e:
            print("Problemas ao ler a tabela Martria\n")
            print(e)
            res = False
        return res

    def NovoSelecionarNotaID(self, id):
        db = create_engine(self.db_string)
        try:
            result = db.execute("SELECT use.nome, nota.aluno_id, nota.mat_id, mat.curso, nota.nota, prof.professor_id FROM trab_asa.tb_user use, trab_asa.tb_aluno aluno, trab_asa.tb_materia mat, trab_asa.tb_professor prof, trab_asa.tb_nota nota WHERE use.id=nota.aluno_id AND prof.professor_id=mat.prof_id AND aluno.aluno_id=nota.aluno_id AND mat.id=nota.mat_id AND nota.id=%s;", id)
            res = result.fetchone()
        except Exception as e:
            print("Problemas ao ler a tabela Martria\n")
            print(e)
            res = False
        return res

    #SELECT com mais de um resultado

    def NovoSelecionarNotaMateria(self, mat_id):
        db = create_engine(self.db_string)
        try:
            result = db.execute("SELECT use.nome, nota.aluno_id, nota.mat_id, mat.curso, nota.nota, prof.professor_id FROM trab_asa.tb_user use, trab_asa.tb_aluno aluno, trab_asa.tb_materia mat, trab_asa.tb_professor prof, trab_asa.tb_nota nota WHERE use.id=nota.aluno_id AND prof.professor_id=mat.prof_id AND aluno.aluno_id=nota.aluno_id AND mat.id=nota.mat_id AND nota.mat_id=%s;", mat_id)
            #res = result.fetchone()
            answer = []
            for part in result:
                answer1 = {"nome": part['nome'], "aluno_id": part['aluno_id'], "mat_id": part['mat_id'], "curso": part['curso'], "nota": part['nota'], "professor_id": part['professor_id']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao ler a tabela Martria\n")
            print(e)
            res = False
        return res

    #Novo
    def SelecionarNotaMateriaProcurarAluno(self, mat_id, aluno_info):
        db = create_engine(self.db_string)
        aluno_info = '%' + aluno_info + '%'
        try:
            result = db.execute("SELECT use.nome, nota.aluno_id, nota.mat_id, mat.curso, nota.nota, prof.professor_id FROM trab_asa.tb_user use, trab_asa.tb_aluno aluno, trab_asa.tb_materia mat, trab_asa.tb_professor prof, trab_asa.tb_nota nota WHERE use.id=nota.aluno_id AND prof.professor_id=mat.prof_id AND aluno.aluno_id=nota.aluno_id AND mat.id=nota.mat_id AND nota.mat_id=%s AND use.nome LIKE %s;", mat_id, aluno_info)
            answer = []
            for part in result:
                answer1 = {"nome": part['nome'], "aluno_id": part['aluno_id'], "mat_id": part['mat_id'], "curso": part['curso'], "nota": part['nota'], "professor_id": part['professor_id']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao ler a tabela Martria\n")
            print(e)
            res = False
        return res

    def NovoSelecionarNotaAluno(self, aluno_id):
        db = create_engine(self.db_string)
        try:
            result = db.execute("SELECT use.nome, nota.aluno_id, nota.mat_id, mat.curso, nota.nota, prof.professor_id FROM trab_asa.tb_user use, trab_asa.tb_aluno aluno, trab_asa.tb_materia mat, trab_asa.tb_professor prof, trab_asa.tb_nota nota WHERE use.id=nota.aluno_id AND prof.professor_id=mat.prof_id AND aluno.aluno_id=nota.aluno_id AND mat.id=nota.mat_id AND nota.aluno_id=%s;", aluno_id)
            answer = []
            for part in result:
                answer1 = {"nome": part['nome'], "aluno_id": part['aluno_id'], "mat_id": part['mat_id'], "curso": part['curso'], "nota": part['nota'], "professor_id": part['professor_id']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao ler a tabela Martria\n")
            print(e)
            res = False
        return res

    def NovoSelecionarMateriaProfessor(self, prof_id):
        db = create_engine(self.db_string)
        try:
            result = db.execute("SELECT mat.id, use.nome, prof.afiliacao, mat.curso FROM trab_asa.tb_user use, trab_asa.tb_professor prof, trab_asa.tb_materia mat WHERE use.id=%s AND prof.professor_id=use.id AND mat.prof_id=use.id;", prof_id)
            #res = result.fetchone()
            answer = []
            for part in result:
                answer1 = {"nome": part['nome'], "id": part['id'], "afiliacao": part['afiliacao'], "curso": part['curso']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao ler a tabela profesor\n")
            print(e)
            res = False
        return res

    def ListarProfessores(self):
        db = create_engine(self.db_string)
        try:
            result = db.execute("SELECT use.id, use.nome, prof.afiliacao FROM trab_asa.tb_user use, trab_asa.tb_professor prof WHERE use.id=prof.professor_id;")
            answer = []
            for part in result:
                answer1 = {"nome": part['nome'], "id": part['id'], "afiliacao": part['afiliacao']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao ler a tabela profesor\n")
            print(e)
            res = False
        return res

    #Novo
    def ListarProfessoresNome(self, prof_info):
        db = create_engine(self.db_string)
        prof_info = '%' + prof_info + '%'
        try:
            result = db.execute("SELECT use.id, use.nome, prof.afiliacao FROM trab_asa.tb_user use, trab_asa.tb_professor prof WHERE use.id=prof.professor_id AND use.nome LIKE %s;", prof_info)
            answer = []
            for part in result:
                answer1 = {"nome": part['nome'], "id": part['id'], "afiliacao": part['afiliacao']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao ler a tabela profesor\n")
            print(e)
            res = False
        return res


    def ListarAlunos(self):
        db = create_engine(self.db_string)
        try:
            #result = db.execute("SELECT use.id, use.nome, prof.afiliacao FROM trab_asa.tb_user use, trab_asa.tb_professor prof WHERE use.id=prof.professor_id;")
            result = db.execute("SELECT use.id, use.nome, aluno.curso FROM trab_asa.tb_user use, trab_asa.tb_aluno aluno WHERE use.id=aluno.aluno_id;")

            answer = []
            for part in result:
                answer1 = {"nome": part['nome'], "id": part['id'], "curso": part['curso']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao ler a tabela alunos\n")
            print(e)
            res = False
        return res

    #Novo
    def ListarAlunosNome(self, aluno_info):
        db = create_engine(self.db_string)
        aluno_info = '%' + aluno_info + '%'
        try:
            result = db.execute("SELECT use.id, use.nome, aluno.curso FROM trab_asa.tb_user use, trab_asa.tb_aluno aluno WHERE use.id=aluno.aluno_id AND use.nome LIKE %s;", aluno_info)

            answer = []
            for part in result:
                answer1 = {"nome": part['nome'], "id": part['id'], "curso": part['curso']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao ler a tabela alunos\n")
            print(e)
            res = False
        return res

    def ListarMaterias(self):
        db = create_engine(self.db_string)
        try:
            result = db.execute("SELECT mat.id, mat.curso FROM trab_asa.tb_materia mat;")
            answer = []
            for part in result:
                answer1 = { "id": part['id'],"curso": part['curso']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao ler a tabela matérias\n")
            print(e)
            res = False
        return res

    #Novo
    def ListarMateriasNome(self, mat_info):
        db = create_engine(self.db_string)
        mat_info = '%' + mat_info + '%'
        try:
            result = db.execute("SELECT mat.id, mat.curso FROM trab_asa.tb_materia mat WHERE mat.curso LIKE %s;", mat_info)
            answer = []
            for part in result:
                answer1 = { "id": part['id'],"curso": part['curso']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao ler a tabela matérias\n")
            print(e)
            res = False
        return res

    def ListarMateriasDoAluno(self,id_aluno):
        db = create_engine(self.db_string)
        try:
            result = db.execute("select mat.mat_id, f.curso , mat.nota From trab_asa.tb_nota mat  inner join trab_asa.tb_materia as f on mat.mat_id = f.id   where mat.aluno_id=%s", id_aluno)
            answer = []
            for part in result:
                answer1 = { "id": part['mat_id'],"curso": part['curso'], "nota": part['nota']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao listas as matérias do aluno\n")
            print(e)
            res = False
        return res  

    def ExcluirProfessor(self, id_prof):
        db = create_engine(self.db_string)
        try:
            db.execute("delete from trab_asa.tb_materia where prof_id =%s", id_prof)
            db.execute("DELETE FROM trab_asa.tb_professor WHERE professor_id=%s",id_prof)
            db.execute("DELETE FROM trab_asa.tb_user WHERE id=%s",id_prof)
            res = True
        except Exception as e:
            print("Problemas ao deletar professor\n")
            print(e)
            res = False
        return res

    def ExcluirAluno(self, id_aluno):
        db = create_engine(self.db_string)
        try:
            db.execute("delete from trab_asa.tb_nota where aluno_id = %s",id_aluno)
            db.execute("delete from trab_asa.tb_aluno where aluno_id = %s",id_aluno)
            db.execute("DELETE FROM trab_asa.tb_user WHERE id="+id_aluno)
            res = True
        except Exception as e:
            print("Problemas ao deletar aluno\n")
            print(e)
            res = False
        return res

    def ExcluirMateria(self, id_mat):
        db = create_engine(self.db_string)
        try:
            db.execute("DELETE FROM trab_asa.tb_materia WHERE id=%s", id_mat)
            res = True
        except Exception as e:
            print("Problemas ao deletar matéria\n")
            print(e)
            res = False
        return res
    
    #UPDATES

    def AtualizarNotas(self, aluno_id, mat_id, nota):
        db = create_engine(self.db_string)
        try:
            result = db.execute("UPDATE trab_asa.tb_nota SET nota=%s WHERE mat_id=%s AND aluno_id=%s", nota, mat_id, aluno_id)
            res = result
        except Exception as e:
            print("Problemas ao inserir na tabela usuario\n")
            print(e)
            res = False
        return res

##LOGIN
    def Login(self, user_id, senha):
        db = create_engine(self.db_string)
        try:
            result = db.execute("SELECT permissao FROM trab_asa.tb_user WHERE id=%s AND senha=%s;", user_id, senha)
            res = result.fetchone()[0]
        except Exception as e:
            print("Problemas ao ler a tabela usuario\n")
            print(e)
            res = False
        return res

    def NomeUsuario(self, user_id):
        db = create_engine(self.db_string)
        try:
            result = db.execute("SELECT nome FROM trab_asa.tb_user WHERE id=%s;", user_id)
            res = result.fetchone()[0]
        except Exception as e:
            print("Problemas ao ler a tabela usuario\n")
            print(e)
            res = False
        return res

    def VerificaLogin(self, user_id, senha):
        db = create_engine(self.db_string)
        try:
            result = db.execute("SELECT nome FROM trab_asa.tb_user WHERE id=%s AND senha=%s;", user_id, senha)
            res = result.fetchone()[0]
        except Exception as e:
            print("Problemas ao ler a tabela usuario\n")
            print(e)
            res = False
        return res
    
    def VerificaUsuario(self, nome_aluno):
        db = create_engine(self.db_string)
        try:
            result = db.execute("SELECT nome FROM trab_asa.tb_user WHERE nome=%s;",nome_aluno)
            res = result.fetchone()[0]
        except Exception as e:
            print("Problemas ao ler a tabela usuario\n")
            print(e)
            res = False
        return res

    def SelecionarUmProfessor(self,nome):
        db = create_engine(self.db_string)
        try:
            result = db.execute("SELECT nome FROM trab_asa.tb_user WHERE nome=%s;", nome)
            res = result.fetchone()[0]
        except Exception as e:
            print("Problemas ao ler a tabela profesor\n")
            print(e)
            res = False
        return res