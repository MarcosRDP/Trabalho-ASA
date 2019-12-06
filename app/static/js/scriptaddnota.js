$(function() {
    $('#btn_edit').click(function() {
        //alert(val('url'));
        alert(val('mat'));
        alert(val('id'));
        alert(val('aluno'));
        /*$.ajax({
            url: "/",
            callback: 'callback',
            crossDomain: true,
            contentType: 'application/json; charset=utf-8',
            dataType: 'application/json',
            complete: function(data){
                alert(data.status);// $1000
                var myResult = data
                console.log(myResult);
                var myDict = JSON.parse(data.responseText);
                var len = myDict.lenght;
                var list_html = "<ol>";
                for(var i=0;i<len;i++){
                     list_html += "<li>" + myDict[i].nome + " " + myDict[i].idade + " " + myDict[i].curso + "</li";
                     console.log(myDict[i])
                }
                list_html += "</ol"
                $("#jsonlist").html(list_html);
            },
            error: function(error) {
                console.log(error);
            }
        });*/
    });    
});