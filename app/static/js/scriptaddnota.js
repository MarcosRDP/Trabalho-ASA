var number = 0;

function count(){
    number = number + 1
    document.write(number);
}      

function execute(id_aluno, id_mat){
    try {
        valor = document.getElementById(id_aluno).value;

        //Inicializa o processo para comunicar com a API
        var xhr = new XMLHttpRequest();

        json = '{"aluno_id": "' + id_aluno + '", "mat_id": "' + id_mat + '", "nota": "' + valor + '"}';
            
        var url = 'http://127.0.0.1:5000/db/nota/atualizar';
        xhr.open('POST',url,true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(json);
        }
    catch(err) {
        alert(err);
    }
}