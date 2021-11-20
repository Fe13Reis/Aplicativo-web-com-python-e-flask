var var_lista = document.getElementById("div_lista");

var dados = ""

var db = firebase.database().ref().child("recados");
db.on('child_added', function(snapshot){
  var adicionado = snapshot.val();

  dados = '<table class="table">' + 
          '<tr><td style="width: 33%">' + adicionado.mensagem + "</td>" +
          '<td style="width: 33%">' + adicionado.asunto + "</td>" +
          '<td style="width: 33%">' + adicionado.date + "</td>" +
          '<td style="width: 33%">' + adicionado.morador + "</tr></td>" +
          dados +
          "</table>";

  var_lista.innerHTML = dados;
})