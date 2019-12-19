from sqlalchemy import create_engine

class DbUtils:
#    db_string = "postgresql+psycopg2://postgres:banco@127.0.0.1:5432/trab_asa"
    db_string = "postgresql+psycopg2://postgres:banco@teste-postgres-compose:5432/trab_asa"
    db_query = " "

    #CREATE functions

    def addNovoUsuario(self, nome, senha, permissao):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        
        #db = create_engine('postgresql://postgres:banco@{}:5432/database'.format('teste-postgres-compose'))
        try:
            result = db.execute("INSERT INTO trab_asa.tb_user(nome, senha, permissao) VALUES (%s, %s, %s) RETURNING id;", nome, senha, permissao)
            res = result.fetchone()[0]
        except Exception as e:
            print("Problemas ao inserir na tabela usuario\n")
            print(e)
            res = False
        return res

    def addNovoProfessor(self, nome, senha, afiliacao,email):
        res01 = self.addNovoUsuario(nome, senha, 2)
        if(res01 == False):
            res = False
        else:
            db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
            try:
                matricula = "11921UFU"+str(res01)
                db.execute("INSERT INTO trab_asa.tb_professor(professor_id, afiliacao,professor_mat,email) VALUES (%s, %s,%s,%s)", res01, afiliacao,matricula,email)
                res = True
            except Exception as e:
                print("Problemas ao inserir na tabela professor\n")
                print(e)
                res = False
        return res

    def addNovoAluno(self, nome, senha, curso,email):
        res01 = self.addNovoUsuario(nome, senha, 1) 
        if(res01 == False):
            res = False
        else:
            db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
            try:
                matricula = "11921ECP"+str(res01)
                db.execute("INSERT INTO trab_asa.tb_aluno(aluno_id, aluno_mat,curso,email) VALUES (%s, %s,%s,%s)", res01,matricula,curso,email)
                res = True
            except Exception as e:
                print("Problemas ao inserir na tabela aluno\n")
                print(e)
                res = False
        return res

    def addNovaMateria(self, nome, curso):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
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

    def addNovaNota(self,aluno_mat, id_materia, nota):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        try:
            aluno_id = db.execute("select aluno_id from trab_asa.tb_aluno WHERE aluno_mat=%s;", aluno_mat).fetchone()[0]
            mat_existe = db.execute("select mat_id from trab_asa.tb_nota where aluno_id=%s", aluno_id).fetchone()
            if(mat_existe != None):
                res = False
            else:
                db.execute("INSERT INTO trab_asa.tb_nota(aluno_id, mat_id, nota) VALUES (%s, %s, %s);", aluno_id, id_materia, nota)
                res = True
        except Exception as e:
            print("Problemas ao inserir na tabela matéria\n")
            print(e)
            res = False
        return res

    def NovoSelecionarUsuario(self, id):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        try:
            result = db.execute("SELECT * FROM trab_asa.tb_user WHERE id=%s;", id)
            res = result.fetchone()
        except Exception as e:
            print("Problemas ao ler a tabela usuario\n")
            print(e)
            res = False
        return res

    def NovoSelecionarProfessor(self, prof_mat):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        try:
            id = db.execute("select professor_id from trab_asa.tb_professor where professor_mat=%s", prof_mat).fetchone()[0]
            result = db.execute("SELECT use.id, use.nome, use.senha, use.permissao, prof.afiliacao prof.FROM trab_asa.tb_user use, trab_asa.tb_professor prof WHERE use.id=%s AND prof.professor_id=use.id;", id)
            res = result.fetchone()
        except Exception as e:
            print("Problemas ao ler a tabela profesor\n")
            print(e)
            res = False
        return res

    def NovoSelecionarAluno(self, id):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        try:
            result = db.execute("SELECT use.id, use.nome, use.senha, use.permissao, aluno.curso FROM trab_asa.tb_user use, trab_asa.tb_aluno aluno WHERE use.id=%s AND aluno.aluno_id=use.id;", id)
            res = result.fetchone()
        except Exception as e:
            print("Problemas ao ler a tabela profesor\n")
            print(e)
            res = False
        return res

    def NovoSelecionarMateriaID(self, id):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        try:
            result = db.execute("SELECT use.id, use.nome, prof.afiliacao, mat.curso FROM trab_asa.tb_user use, trab_asa.tb_professor prof, trab_asa.tb_materia mat WHERE use.id=mat.prof_id AND prof.professor_id=use.id AND mat.id=%s;", id)
            res = result.fetchone()
        except Exception as e:
            print("Problemas ao ler a tabela Martria\n")
            print(e)
            res = False
        return res

    def NovoSelecionarNotaID(self, id):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
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
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
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
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
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
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
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

    def NovoSelecionarMateriaProfessor(self, prof_mat):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        try:
            prof_id = db.execute("select professor_id from trab_asa.tb_professor where professor_mat=%s", prof_mat).fetchone()[0]
            result = db.execute("SELECT mat.id, use.nome, prof.afiliacao, mat.curso FROM trab_asa.tb_user use, trab_asa.tb_professor prof, trab_asa.tb_materia mat WHERE use.id=%s AND prof.professor_id=use.id AND mat.prof_id=use.id;", prof_id)
            #res = result.fetchone()
            answer = []
            for part in result:
                answer1 = {"nome": part['nome'], "id": part['id'], "afiliacao": part['afiliacao'], "curso": part['curso']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao ler a tabela profesor!!!\n")
            print(e)
            res = False
        return res

    def ListarProfessores(self):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        try:
            result = db.execute("SELECT use.id, use.nome, prof.afiliacao, prof.professor_mat FROM trab_asa.tb_user use, trab_asa.tb_professor prof WHERE use.id=prof.professor_id;")
            answer = []
            for part in result:
                answer1 = {"nome": part['nome'], "id": part['id'], "afiliacao": part['afiliacao'], "matricula": part['professor_mat']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao ler a tabela profesor\n")
            print(e)
            res = False
        return res

    #Novo
    def ListarProfessoresNome(self, prof_info):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        prof_info = '%' + prof_info + '%'
        try:
            result = db.execute("SELECT use.id, use.nome, prof.afiliacao, prof.professor_mat FROM trab_asa.tb_user use, trab_asa.tb_professor prof WHERE use.id=prof.professor_id AND use.nome LIKE %s;", prof_info)
            answer = []
            for part in result:
                answer1 = {"nome": part['nome'], "id": part['id'], "afiliacao": part['afiliacao'], "matricula": part['professor_mat']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao ler a tabela profesor\n")
            print(e)
            res = False
        return res

    def ListarAlunos(self):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        try:
            #result = db.execute("SELECT use.id, use.nome, prof.afiliacao FROM trab_asa.tb_user use, trab_asa.tb_professor prof WHERE use.id=prof.professor_id;")
            result = db.execute("SELECT use.id, use.nome, aluno.curso, aluno.aluno_mat FROM trab_asa.tb_user use, trab_asa.tb_aluno aluno WHERE use.id=aluno.aluno_id;")

            answer = []
            for part in result:
                answer1 = {"nome": part['nome'], "id": part['id'], "curso": part['curso'], "matricula": part['aluno_mat']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao ler a tabela alunos\n")
            print(e)
            res = False
        return res

    #Novo
    def ListarAlunosNome(self, aluno_info):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        aluno_info = '%' + aluno_info + '%'
        try:
            result = db.execute("SELECT use.id, use.nome, aluno.curso, aluno.aluno_mat FROM trab_asa.tb_user use, trab_asa.tb_aluno aluno WHERE use.id=aluno.aluno_id AND use.nome LIKE %s;", aluno_info)

            answer = []
            for part in result:
                answer1 = {"nome": part['nome'], "id": part['id'], "curso": part['curso'], "matricula": part['aluno_mat']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao ler a tabela alunos\n")
            print(e)
            res = False
        return res

#    def ListarMaterias(self):
#        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
#        try:
#            result = db.execute("SELECT mat.id, mat.curso,mat.prof_id FROM trab_asa.tb_materia mat;")
#            prof_id = result.fetchone()[1]
#            nome_professor = db.execute("Select nome from trab_asa.tb_user WHERE id=%s",prof_id).fetchone()[0]
#            answer = []
#            for part in result:
#                answer1 = { "id": part['id'],"curso": part['curso']}
#                answer.append(answer1)
#            res = answer
#        except Exception as e:
#            print("Problemas ao ler a tabela matérias\n")
#            print(e)
#            res = False
#        return res


    def ListarMaterias(self):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        try:
            result = db.execute("SELECT trab_asa.tb_user.nome,trab_asa.tb_materia.curso,trab_asa.tb_materia.id FROM trab_asa.tb_user INNER JOIN trab_asa.tb_materia ON trab_asa.tb_user.id = trab_asa.tb_materia.prof_id;")
            answer = []
            for part in result:
                answer1 = { "nome": part['nome'],"curso": part['curso'],"id": part['id']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao ler a tabela matérias\n")
            print(e)
            res = False
        return res

    def ListarMateriasN(self, mat_info):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        mat_info = '%' + mat_info + '%'
        try:
            result = db.execute("SELECT trab_asa.tb_user.nome,trab_asa.tb_materia.curso,trab_asa.tb_materia.id FROM trab_asa.tb_user INNER JOIN trab_asa.tb_materia ON trab_asa.tb_user.id = trab_asa.tb_materia.prof_id WHERE trab_asa.tb_materia.curso LIKE %s;", mat_info)
            answer = []
            for part in result:
                answer1 = { "nome": part['nome'],"curso": part['curso'],"id": part['id']}
                answer.append(answer1)
            res = answer
        except Exception as e:
            print("Problemas ao ler a tabela matérias\n")
            print(e)
            res = False
        return res


    #Novo
    def ListarMateriasNome(self, mat_info):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
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

    def ListarMateriasDoAluno(self,aluno_mat):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        try:
            result0 = db.execute("select aluno_id from trab_asa.tb_aluno where aluno_mat=%s", aluno_mat)
            aluno_id = result0.fetchone()[0]
            result = db.execute("select mat.mat_id, f.curso , mat.nota From trab_asa.tb_nota mat  inner join trab_asa.tb_materia as f on mat.mat_id = f.id   where mat.aluno_id=%s", aluno_id)
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
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
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
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
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
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
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
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
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
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        try:

            result1 = db.execute("SELECT admin_id FROM trab_asa.tb_admin WHERE admin_mat=%s ;", user_id)
            res1 = result1.fetchone()
            if(res1 != None):
                res = 3
            
            result2 = db.execute("SELECT professor_id FROM trab_asa.tb_professor WHERE professor_mat=%s ;", user_id)
            res2 = result2.fetchone()
            if(res2 != None):
                res = 2
                
            result3 = db.execute("SELECT aluno_id FROM trab_asa.tb_aluno WHERE aluno_mat=%s ;", user_id)
            res3 = result3.fetchone()
            if(res3 != None):
                res = 1
                
        except Exception as e:
            print("Problemas ao ler a tabela usuario(LOGIN)\n")
            print(e)
            res = False
        return res

    def NomeUsuario(self, user_id):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        result1 = db.execute("SELECT admin_id FROM trab_asa.tb_admin WHERE admin_mat=%s ;", user_id)
        res1 = result1.fetchone()
        if(res1 != None):
            try:
                #if(res01 != False):
                result = db.execute("SELECT nome FROM trab_asa.tb_user WHERE id=%s;",res1)
                res = result.fetchone()[0]
            except Exception as e:
                print("Problemas ao ler a tabela usuario(NOMEUSUARIO)\n")
                print(e)
                res = False
        
        result2 = db.execute("SELECT professor_id FROM trab_asa.tb_professor WHERE professor_mat=%s ;", user_id)        
        res2 = result2.fetchone()
        if(res2 != None):
            try:
                #if(res02 != False):
                result = db.execute("SELECT nome FROM trab_asa.tb_user WHERE id=%s;",res2)
                res = result.fetchone()[0]
            except Exception as e:
                print("Problemas ao ler a tabela usuario(NOMEUSUARIO)\n")
                print(e)
                res = False

        result3 = db.execute("SELECT aluno_id FROM trab_asa.tb_aluno WHERE aluno_mat=%s ;", user_id)
        res3 = result3.fetchone()
        if(res3 != None):
            try:
                #if(res03 != False):
                result = db.execute("SELECT nome FROM trab_asa.tb_user WHERE id=%s;",res3)
                res = result.fetchone()[0]
            except Exception as e:
                print("Problemas ao ler a tabela usuario(NOMEUSUARIO)\n")
                print(e)
                res = False
        return res

    def VerificaLogin(self, user_id, senha):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        res = False
        result1 = db.execute("SELECT admin_id FROM trab_asa.tb_admin WHERE admin_mat=%s;", user_id)
        res1 = result1.fetchone()
        if(res1 != None):
            try:
                result1 = db.execute("SELECT admin_id FROM trab_asa.tb_admin WHERE admin_mat=%s;", user_id)
                res01 = result1.fetchone()[0]
                resultado1 = db.execute("SELECT id FROM trab_asa.tb_user WHERE id=%s AND senha=%s;", res01, senha)
                res = resultado1.fetchone()[0]
            except Exception as e:
                print("Problemas ao ler a tabela usuario(VERIFICALOGIN RES1)\n")
                print(e)
                res = False

        result2 = db.execute("SELECT professor_id FROM trab_asa.tb_professor WHERE professor_mat=%s ;", user_id)
        res2 = result2.fetchone()
        if(res2 != None):
            try:
                result2 = db.execute("SELECT professor_id FROM trab_asa.tb_professor WHERE professor_mat=%s ;", user_id)
                res02 = result2.fetchone()[0]
                resultado2 = db.execute("SELECT id FROM trab_asa.tb_user WHERE id=%s AND senha=%s;", res02, senha)
                res = resultado2.fetchone()[0]
            except Exception as e:
                print(result2)
                print("Problemas ao ler a tabela usuario(VERIFICALOGIN RES2)\n")
                print(e)
                res = False

        result3 = db.execute("SELECT aluno_id FROM trab_asa.tb_aluno WHERE aluno_mat=%s ;", user_id)
        res3 = result3.fetchone()
        if(res3 != None):
            try:
                result3 = db.execute("SELECT aluno_id FROM trab_asa.tb_aluno WHERE aluno_mat=%s ;", user_id)
                res03 = result3.fetchone()[0]
                resultado3 = db.execute("SELECT id FROM trab_asa.tb_user WHERE id=%s AND senha=%s;", res03, senha)
                res = resultado3.fetchone()[0]
            except Exception as e:
                print("Problemas ao ler a tabela usuario(VERIFICALOGIN RES3)\n")
                print(e)
                res = False        
        return res
    
    def VerificaUsuario(self, nome_aluno):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        try:
            result = db.execute("SELECT nome FROM trab_asa.tb_user WHERE nome=%s;",nome_aluno)
            res01 = result.fetchone()
            if(res01 != None):
                res = True
            else:
                res = False
        except Exception as e:
            print("Problemas ao ler a tabela usuario(VERIFICAUSUARIO)\n")
            print(e)
            res = False
        return res

    def SelecionarUmProfessor(self,nome):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        try:
            result = db.execute("SELECT permissao FROM trab_asa.tb_user WHERE nome=%s;", nome)
            res0 = result.fetchone()
            if(res0 != None):
                result = db.execute("SELECT permissao FROM trab_asa.tb_user WHERE nome=%s;", nome)
                res0 = result.fetchone()[0]
                if(res0 != 2):
                    res = False
                else:
                    res = True
            else:
                res = False
                
        except Exception as e:
            print("Problemas ao ler a tabela profesor\n")
            print(e)
            res = False
        return res

    def Curso(self,nome):
        db = create_engine('postgresql://postgres:banco@{}:5432/trab_asa'.format('postgres'))
        try:
            result = db.execute("SELECT id FROM trab_asa.tb_user WHERE nome=%s", nome)
            res01 = result.fetchone()[0]
            result2 = db.execute("SELECT curso FROM trab_asa.tb_aluno WHERE aluno_id=%s",res01)
            res = result2.fetchone()[0]
        except Exception as e:
            print("Problemas ao ler a tabela profesor\n")
            print(e)
            res = False
        return res