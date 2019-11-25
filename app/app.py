from flask import Flask, jsonify, request, render_template, url_for, json, abort, redirect
from flask_wtf import FlaskForm
from models.forms import loginForm, registerFormProf, registerFormAluno, registerFormMateria, matriculaMateria, SelectTable
from models.dbutils import DbUtils
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask import flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minha palavra secreta'
Bootstrap(app)

#Varíaves Globais
usuario = 0
materia = 0
permissao = 0
infoUsuario = 0

#Rota base, redireciona para a página adequada de acordo com o usuário logado
@app.route('/')
def base():
    global permissao
    if(permissao == 0): #Página de login
        return redirect("http://127.0.0.1:5000/login", code=302)
    if(permissao == 1): #Página do aluno
        return redirect("http://127.0.0.1:5000/aluno", code=302)
    if(permissao == 2): #Página do professor
        return redirect("http://127.0.0.1:5000/professor", code=302)
    if(permissao == 3): #Página do admin
        return redirect("http://127.0.0.1:5000/admin", code=302)

#Tela de Login
@app.route('/login', methods=['POST','GET'])
def login():
    global usuario
    global permissao
    global infoUsuario

    if(permissao == 1): #Página do aluno
        return redirect("http://127.0.0.1:5000/aluno", code=302)
    if(permissao == 2): #Página do professor
        return redirect("http://127.0.0.1:5000/professor", code=302)
    if(permissao == 3): #Página do admin
        return redirect("http://127.0.0.1:5000/admin", code=302)

    form = loginForm()
    db = DbUtils()
    if form.validate_on_submit(): #Na tentativa de login
        #Verifica na tabela user se a senha e o id estão corretos
        resultado = db.VerificaLogin(form.username.data,form.password.data)
        if(resultado == False):
            flash("Dados de login incorretos! Por favor tente novamente.")
        infoUsuario = db.NomeUsuario(form.username.data)
        result = db.Login(form.username.data,form.password.data) 
        permissao = result #Resultado é salvo na variável global permissao
        if(result == 0): #Caso resulte em erro no login
            print("Erro") #Printa uma mensagem de erro
            #Carrega novamente a tela de login
            return render_template('login/index.html', form=form)
        if(result == 1): #Caso onde um aluno fez login
            usuario = form.username.data #Atualiza ID do usuário
            #Carrega página adequada
            return redirect("http://127.0.0.1:5000/aluno", code=302) 
        if(result == 2): #Caso onde um professor fez login
            usuario = form.username.data #Atualiza ID do usuário
            #Carrega página adequada
            return redirect("http://127.0.0.1:5000/professor/perfil")
        if(result == 3): #Caso onde um admin fez login
            usuario = form.username.data #Atualiza ID do usuário
            #Carrega página adequada
            return render_template("admin/index.html", code=302,infoUsuario = infoUsuario)
    else:
        print(form.errors)
    return render_template('login/index.html', form=form)

#Botão de Sair
@app.route('/sair')
def logoff(): #Limpa todas as informações do usuário
    global materia 
    global usuario
    global permissao
    materia = 0
    usuario = 0
    permissao = 0
    infoUsuario = 0
    #Envia para a tela de login
    return redirect("http://127.0.0.1:5000/login", code=302)

#Telas do Admin

#Tela padrão do Admin
@app.route('/admin', methods=['GET','POST'])
def signup():
    global permissao
    if(permissao != 3): #Caso a permissão do usuário não seja adequada
        #Carrega a página base
        return redirect("http://127.0.0.1:5000/", code=302)
    return render_template('admin/index.html',infoUsuario = infoUsuario)

#Tela de Cadastro do aluno
@app.route('/signupAluno', methods=['GET','POST'])
def signupAluno():
    global permissao
    if(permissao != 3): #Caso a permissão do usuário não seja adequada
        #Carrega a página base
        return redirect("http://127.0.0.1:5000/", code=302)
    form = registerFormAluno()
    db = DbUtils()
    if form.validate_on_submit():
        resultado = db.VerificaUsuario(form.username.data)
        if(resultado == False):
            db.addNovoAluno(form.username.data,form.password.data,form.curso.data)
            return render_template('admin/index.html', infoUsuario = infoUsuario)
        else:
            flash("Aluno já cadastrado. Por favor verifique os dados!")
    return render_template('admin/signupAluno.html', form=form)

@app.route('/listarProf', methods=['GET','POST'])
def listarProf():
    global permissao
    if(permissao != 3): #Caso a permissão do usuário não seja adequada
        #Carrega a página base
        return redirect("http://127.0.0.1:5000/", code=302)
    dbUtils = DbUtils()
    listaM = []

    form = SelectTable()
    if form.validate_on_submit(): #Procurando por um aluno
        #Procura todos os alunos com nomes semelhantes
        result = dbUtils.ListarProfessoresNome(form.nome.data)
        if(result == False): 
            listaM = [False] #Registra erro
        else:
            listaM = result #Recebe os dados
    
    else:
        result = dbUtils.ListarProfessores()
        if(result == False):
            listaM = [False]
        else:
            listaM = result
    return render_template('admin/listarProf.html', listaM = listaM, form = form)

#Tela de Cadastro do Professor
@app.route('/signupProf', methods=['GET','POST'])
def signupProf():
    global permissao
    if(permissao != 3): #Caso a permissão do usuário não seja adequada
        #Carrega a página base
        return redirect("http://127.0.0.1:5000/", code=302)
    form = registerFormProf()
    db = DbUtils()
    result = db.ListarProfessores()
    listaM = []
    if(result == False):
        listaM = [False]
    else:
        listaM = result
    if form.validate_on_submit():
        resultado = db.VerificaUsuario(form.username.data)
        if(resultado == False):
            db.addNovoProfessor(form.username.data,form.password.data,form.afiliacao.data)
            return render_template('admin/index.html', infoUsuario = infoUsuario)
        else:
            flash("Professor já cadastrado. Por favor verifique os dados!")
    return render_template('admin/signupProf.html', form=form, listaM = listaM)

#Tela de Cadastro de Materia
@app.route('/addMaterias', methods=['GET','POST'])
def addMaterias():
    global permissao
    if(permissao != 3): #Caso a permissão do usuário não seja adequada
        #Carrega a página base
        return redirect("http://127.0.0.1:5000/", code=302)
    form = registerFormMateria()
    db = DbUtils()
    result = db.ListarProfessores()
    listaM = []
    if(result == False):
        listaM = [False]
    else:
        listaM = result
    if form.validate_on_submit():
        rest = db.SelecionarUmProfessor(form.nomeProfessor.data)
        if(rest == False):
            flash("Professor não cadastrado! Por favor tente novamente.")
        else:        
            db.addNovaMateria(form.nomeProfessor.data,form.nomeMateria.data)
            return render_template('admin/index.html', infoUsuario = infoUsuario)
    else:
        print(form.errors)
    return render_template('admin/addMaterias.html', form=form, listaM = listaM)

#Tela de Remoção do Professor
@app.route('/excluirProf', methods=['GET','POST'])
def excluirProf():
    global permissao
    if(permissao != 3): #Caso a permissão do usuário não seja adequada
        #Carrega a página base
        return redirect("http://127.0.0.1:5000/", code=302)
    dbUtils = DbUtils()
    listaM = []

    form = SelectTable()
    if form.validate_on_submit(): #Procurando por um aluno
        #Procura todos os alunos com nomes semelhantes
        result = dbUtils.ListarProfessoresNome(form.nome.data)
        if(result == False): 
            listaM = [False] #Registra erro
        else:
            listaM = result #Recebe os dados
    
    else:
        result = dbUtils.ListarProfessores()
        if(result == False):
            listaM = [False]
        else:
            listaM = result
    
    return render_template('admin/excluirProf.html', listaM = listaM, form = form)

#Tela de Remoção do Professor 2
@app.route('/excluirProf2/', methods=['POST'])
def excluirProf2():
    global permissao
    if(permissao != 3): #Caso a permissão do usuário não seja adequada
        #Carrega a página base
        return redirect("http://127.0.0.1:5000/", code=302)
    if request.method == 'POST':
    #data = id_prof
        dbUtils = DbUtils()
        data =  request.form['id']
        result = dbUtils.ExcluirProfessor(data)

        return render_template('admin/index.html', infoUsuario = infoUsuario)

#Tela de Remoção do Aluno
@app.route('/excluirAluno', methods=['GET','POST'])
def excluirAluno():
    global permissao
    if(permissao != 3): #Caso a permissão do usuário não seja adequada
        #Carrega a página base
        return redirect("http://127.0.0.1:5000/", code=302)
    dbUtils = DbUtils()
    listaM = []

    form = SelectTable()
    if form.validate_on_submit(): #Procurando por um aluno
        #Procura todos os alunos com nomes semelhantes
        result = dbUtils.ListarAlunosNome(form.nome.data)
        if(result == False): 
            listaM = [False] #Registra erro
        else:
            listaM = result #Recebe os dados
    
    else:
        result = dbUtils.ListarAlunos()
        if(result == False):
            listaM = [False]
        else:
            listaM = result
        
    return render_template('admin/excluirAluno.html', listaM = listaM, form = form)

#Tela de Remoção do Aluno 2
@app.route('/excluirAluno2/', methods=['POST'])
def excluirAluno2():
    global permissao
    if(permissao != 3): #Caso a permissão do usuário não seja adequada
        #Carrega a página base
        return redirect("http://127.0.0.1:5000/", code=302)
    if request.method == 'POST':
    #data = id_prof
        dbUtils = DbUtils()
        data =  request.form['id']
        result = dbUtils.ExcluirAluno(data)

        return render_template('admin/index.html', infoUsuario = infoUsuario)

#Tela de Remoção de Matéria
@app.route('/excluirMateria', methods=['GET','POST'])
def excluirMateria():
    global permissao
    if(permissao != 3): #Caso a permissão do usuário não seja adequada
        #Carrega a página base
        return redirect("http://127.0.0.1:5000/", code=302)
    dbUtils = DbUtils()
    listaM = []

    form = SelectTable()
    if form.validate_on_submit(): #Procurando por um aluno
        #Procura todos os alunos com nomes semelhantes
        result = dbUtils.ListarMateriasNome(form.nome.data)
        if(result == False): 
            listaM = [False] #Registra erro
        else:
            listaM = result #Recebe os dados

    else:
        result = dbUtils.ListarMaterias()
        if(result == False):
            listaM = [False]
        else:
            listaM = result
    
    return render_template('admin/excluirMaterias.html', listaM = listaM, form = form)

#Tela de Remoção de Matéria 2
@app.route('/excluirMaterias2', methods=['GET','POST'])
def excluirMateria2():
    global permissao
    if(permissao != 3): #Caso a permissão do usuário não seja adequada
        #Carrega a página base
        return redirect("http://127.0.0.1:5000/", code=302)
    if request.method == 'POST':
        dbUtils = DbUtils()
        data =  request.form['id']
        result = dbUtils.ExcluirMateria(data)
        return render_template('admin/index.html', infoUsuario = infoUsuario)

##Telas do Professor

#Tela de Transferência 1
@app.route('/professor')
def professor():
    global permissao
    if(permissao == 2): #Verifica se tem a permissão de professor
        #Direciona para a tela principal do professor
        return redirect("http://127.0.0.1:5000/professor/perfil", code=302)
    else: #Caso não tenha
        #Direciona para a tela de login
        return redirect("http://127.0.0.1:5000/login", code=302)

#Tela de Transferência 2
@app.route('/professor/')
def professor2():
    global permissao
    if(permissao == 2): #Verifica se tem a permissão de professor
        #Direciona para a tela principal do professor
        return redirect("http://127.0.0.1:5000/professor/perfil", code=302)
    else: #Caso não tenha
        #Direciona para a tela de login
        return redirect("http://127.0.0.1:5000/login", code=302)

#Tela principal do professor, seu perfil
@app.route('/professor/perfil')
def show_professor_perfil():
    global usuario
    global permissao
    if(permissao != 2): #Verifica se tem a permissão de professor
        #Caso não possua volta para a tela de login
        return redirect("http://127.0.0.1:5000/login", code=302)

    dbUtils = DbUtils() #Comunica com a base de dados e recebe todas as matéria do professor
    result = dbUtils.NovoSelecionarMateriaProfessor(usuario)
    if(result == False):
        listaM = [False] #Registra erro
    else:
        listaM = result #Registra as matérias

    #Recebe a informação do professor
    result = dbUtils.NovoSelecionarProfessor(usuario)
    if(result == False):
        user = False #Registra erro
    else:
        #Registra as informações
        user = {"nome": result['nome'], "senha": result['senha'], "permissao": result['permissao'], "afiliacao": result['afiliacao']}
    
    #Inicializa a pagina de perfil
    return render_template('professor/perfil.html',listaM=listaM, user=user, id=usuario)

#Recebe a matéria selecionada
@app.route('/professor/selecionar/materia/<int:mat>')
def get_professor_materia(mat):
    global materia
    global permissao
    if(permissao != 2): #Verifica se tem a permissão de professor
        #Caso não possua volta para a tela de login
        return redirect("http://127.0.0.1:5000/login", code=302)

    materia = mat #Salva a matéria selecionada como global
    #Chama a página das notas da matéria selecionada
    return redirect("http://127.0.0.1:5000/professor/notas", code=302)

#Página de atualização de notas da matéria selecionada
@app.route('/professor/notas', methods=['POST','GET'])
def show_notas():
    global usuario
    global materia
    global permissao
    if(permissao != 2): #Verifica se tem a permissão de professor
        #Caso não possua volta para a tela de login
        return redirect("http://127.0.0.1:5000/login", code=302)

    if(materia == 0): #Caso nenhuma matéria tenha sido selecionada, retorna para o perfil
        return redirect("http://127.0.0.1:5000/professor/perfil", code=302)

    dbUtils = DbUtils()
    result = dbUtils.NovoSelecionarMateriaProfessor(usuario)
    if(result == False): #Recebe as matérias do professor
        listaM = [False] #Registra erro
    else:
        listaM = result #Recebe os dados

    result = dbUtils.NovoSelecionarMateriaID(materia)
    if(result == False): #Recebe os dados da matéria selecionada
        mat = False #Registra erro
    else:
        mat = result['curso'] #Recebe o nome da matéria

    form = SelectTable()
    if form.validate_on_submit(): #Procurando por um aluno
        #Procura todos os alunos com nomes semelhantes
        result = dbUtils.SelecionarNotaMateriaProcurarAluno(materia, form.nome.data)
        if(result == False): 
            lista_alunos = [False] #Registra erro
        else:
            lista_alunos = result #Recebe os dados
    else: 
        result = dbUtils.NovoSelecionarNotaMateria(materia)
        if(result == False): #Recebe as notas da matéria selecionada
            lista_alunos = [False] #Registra erro
        else:
            lista_alunos = result #Recebe os dados

    #Incializa a página das notas da matéria selecionada
    return render_template('professor/table.html', listaM=listaM, materia=mat, lista_alunos=lista_alunos, id_mat=materia, form=form)

#Atualiza a nota de um aluno
@app.route('/db/nota/atualizar', methods = ['POST'])
def api_updatenotadb():
    if not request.json:
        abort(400)
    dbUtils = DbUtils()
    req_data = request.get_json()
    aluno_id = req_data['aluno_id']
    mat_id = req_data['mat_id']
    nota = req_data['nota']
    if (dbUtils.AtualizarNotas(aluno_id, mat_id, nota)):
        result = {"result": True}
    else:
        result = {"result": False}
    return jsonify(result)

#Telas do Aluno

#Tela principal do aluno
@app.route('/aluno', methods=['GET','POST'])
def loginAluno():
    global permissao
    if(permissao != 1): #Verifica se tem a permissão de aluno
        #Caso não possua volta para a tela de login
        return redirect("http://127.0.0.1:5000/login", code=302)
    return render_template('aluno/index.html')    

#Tela de cadastro na matricula
@app.route('/matricularMateria', methods=['GET','POST'] )
def matricularMateria():
    global permissao
    if(permissao != 1): #Verifica se tem a permissão de aluno
        #Caso não possua volta para a tela de login
        return redirect("http://127.0.0.1:5000/login", code=302)
    
    form = matriculaMateria()
    db = DbUtils()
    if form.validate_on_submit():
        db.addNovaNota(usuario,form.nome.data,0)
        return render_template('aluno/index.html')
    else:
        print(form.errors)
    return render_template('aluno/matricular.html', form=form)

#Tela de vizualização das matérias do aluno
@app.route('/visualizarMaterias')
def visualizarMaterias():
    global permissao
    if(permissao != 1): #Verifica se tem a permissão de aluno
        #Caso não possua volta para a tela de login
        return redirect("http://127.0.0.1:5000/login", code=302)
    
    dbUtils = DbUtils()
    result = dbUtils.ListarMateriasDoAluno(usuario)
    listaM = []
    if(result == False):
        listaM = [False]
    else:
        listaM = result
    return render_template('aluno/visualizarMaterias.html', listaM = listaM)

#Principal
if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=8080)