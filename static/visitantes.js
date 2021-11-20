var var_lista = document.getElementById("div_lista");

var dados = ""
var dados2 = ""

var db = firebase.database().ref().child("visitantes");
db.on('child_added', function(snapshot){
  var adicionado = snapshot.val();

  dados = '<table class="table">' + 
            '<tr><td style="width: 30%">' + adicionado.nome + "</td>" +
            '<td style="width: 20%">' + adicionado.doc + "</td>" +
            '<td style="width: 20%">' + adicionado.date + "</td>" +
            '<td style="width: 30%">' + adicionado.morador + "</tr></td>" +
            dados +
          "</table>";

  var_lista.innerHTML = dados;
})