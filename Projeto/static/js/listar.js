
    var status = document.getElementById('atividades')
    var btn = document.getElementsById('excluir')
    function alterarBotao(){
        
    }

<td><button id="excluir"><a href="{{ url_for('desativar', id=item.id) }}">Desativar</a></button></td>