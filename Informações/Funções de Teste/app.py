@app.route('/db/professor/add', methods = ['POST'])
def api_newprofessordb():
    if not request.json:
        abort(400)
    dbUtils = DbUtils()
    req_data = request.get_json()
    nome = req_data['nome']
    senha = req_data['senha']
    afiliacao = req_data['afiliacao']
    if (dbUtils.addNovoProfessor(nome, senha, afiliacao)):
        result = {"result": True}
    else:
        result = {"result": False}
    return jsonify(result)

@app.route('/db/aluno/add', methods = ['POST'])
def api_newalunodb():
    if not request.json:
        abort(400)
    dbUtils = DbUtils()
    req_data = request.get_json()
    nome = req_data['nome']
    senha = req_data['senha']
    curso = req_data['curso']
    if (dbUtils.addNovoAluno(nome, senha, curso)):
        result = {"result": True}
    else:
        result = {"result": False}
    return jsonify(result)

@app.route('/db/materia/add', methods = ['POST'])
def api_newmateriadb():
    if not request.json:
        abort(400)
    dbUtils = DbUtils()
    req_data = request.get_json()
    prof_id = req_data['prof_id']
    curso = req_data['curso']
    if (dbUtils.addNovaMateria(prof_id, curso)):
        result = {"result": True}
    else:
        result = {"result": False}
    return jsonify(result)

@app.route('/db/nota/add', methods = ['POST'])
def api_newnotadb():
    if not request.json:
        abort(400)
    dbUtils = DbUtils()
    req_data = request.get_json()
    aluno_id = req_data['aluno_id']
    mat_id = req_data['mat_id']
    nota = req_data['nota']
    if (dbUtils.addNovaNota(aluno_id, mat_id, nota)):
        result = {"result": True}
    else:
        result = {"result": False}
    return jsonify(result)

@app.route('/db/professor/select', methods = ['POST'])
def api_selectprofessordb():
    if not request.json:
        abort(400)
    dbUtils = DbUtils()
    req_data = request.get_json()
    id = req_data['id']
    dbUtils = DbUtils()
    result = dbUtils.NovoSelecionarProfessor(id)
    if(result == False):
        answer = False
    else:
        answer = {"nome": result['nome'], "senha": result['senha'], "permissao": result['permissao'], "afiliacao": result['afiliacao']}
    return jsonify(answer)

@app.route('/db/aluno/select', methods = ['POST'])
def api_selectalunodb():
    if not request.json:
        abort(400)
    dbUtils = DbUtils()
    req_data = request.get_json()
    id = req_data['id']
    dbUtils = DbUtils()
    result = dbUtils.NovoSelecionarAluno(id)
    if(result == False):
        answer = False
    else:
        answer = {"nome": result['nome'], "senha": result['senha'], "permissao": result['permissao'], "afiliacao": result['afiliacao'], "curso": result['curso']}
    return jsonify(answer)

@app.route('/db/materia/select/id', methods = ['POST'])
def api_selectmateriaiddb():
    if not request.json:
        abort(400)
    dbUtils = DbUtils()
    req_data = request.get_json()
    id = req_data['id']
    dbUtils = DbUtils()
    result = dbUtils.NovoSelecionarMateriaID(id)
    if(result == False):
        answer = False
    else:
        answer = {"id": result['id'], "nome": result['nome'], "afiliacao": result['afiliacao'], "curso": result['curso']}
    return jsonify(answer)

@app.route('/db/nota/select/id', methods = ['POST'])
def api_selectnotaiddb():
    if not request.json:
        abort(400)
    dbUtils = DbUtils()
    req_data = request.get_json()
    id = req_data['id']
    dbUtils = DbUtils()
    result = dbUtils.NovoSelecionarNotaID(id)
    if(result == False):
        answer = False
    else:
        answer = {"nome": result['nome'], "aluno_id": result['aluno_id'], "mat_id": result['mat_id'], "curso": result['curso'], "nota": result['nota'], "professor_id": result['professor_id']}
    return jsonify(answer)

@app.route('/db/nota/select/materia', methods = ['POST'])
def api_selectnotamateriadb():
    if not request.json:
        abort(400)
    dbUtils = DbUtils()
    req_data = request.get_json()
    mat_id = req_data['mat_id']
    dbUtils = DbUtils()
    result = dbUtils.NovoSelecionarNotaMateria(mat_id)
    if(result == False):
        answer = False
    else:
        answer = result
    return jsonify(answer)

@app.route('/db/nota/select/aluno', methods = ['POST'])
def api_selectnotaalunodb():
    if not request.json:
        abort(400)
    dbUtils = DbUtils()
    req_data = request.get_json()
    aluno_id = req_data['aluno_id']
    dbUtils = DbUtils()
    result = dbUtils.NovoSelecionarNotaAluno(aluno_id)
    if(result == False):
        answer = False
    else:
        answer = result
    return jsonify(answer)

@app.route('/db/materia/select/professor', methods = ['POST'])
def api_selectmateriaprofessordb():
    if not request.json:
        abort(400)
    dbUtils = DbUtils()
    req_data = request.get_json()
    prof_id = req_data['prof_id']
    dbUtils = DbUtils()
    result = dbUtils.NovoSelecionarMateriaProfessor(prof_id)
    if(result == False):
        answer = False
    else:
        answer = result
    return jsonify(answer)

@app.route('/db/professor/select/all')
def api_selectprofessoralldb():
    dbUtils = DbUtils()
    result = dbUtils.ListarProfessores()
    if(result == False):
        answer = False
    else:
        answer = result
    return jsonify(answer)



