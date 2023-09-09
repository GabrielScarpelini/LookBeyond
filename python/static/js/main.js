function TestaCPF(strCPF) {
    var Soma;
    var Resto;
    Soma = 0;
  if (strCPF == "00000000000") return false;

  for (i=1; i<=9; i++) Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (11 - i);
  Resto = (Soma * 10) % 11;

    if ((Resto == 10) || (Resto == 11))  Resto = 0;
    if (Resto != parseInt(strCPF.substring(9, 10)) ) return false;

  Soma = 0;
    for (i = 1; i <= 10; i++) Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (12 - i);
    Resto = (Soma * 10) % 11;

    if ((Resto == 10) || (Resto == 11))  Resto = 0;
    if (Resto != parseInt(strCPF.substring(10, 11) ) ) return false;
    return true;
}
  
const form = document.querySelector("#formulario")
console.log(document)
// window.alert("esta com JS")

form.addEventListener("submit", (e) => {
    // const aluno =  e.target.querySelector("#studant")
    // console.log(aluno.checked)
    
    var tipo;
    const name = document.querySelector("#name")
    const email = document.querySelector("#email")
    const cpf_cnpj = document.querySelector("#cpf")
    const senha = document.querySelector("#senha")
    const senhaConfirm = document.querySelector("#senha2")

    console.log(senha.value)
    console.log(senhaConfirm.value)

    if (senha.value != senhaConfirm.value){
        e.preventDefault()
        window.alert("as senhas devem ser iguais")
        
    }else if(TestaCPF(cpf_cnpj.value) == false){
        window.alert("O CPF/CNPJ não é válido")
        e.preventDefault()
    }else{
        window.alert("Sucesso no cadastro")
    }

//cnpj completo 18 carc cpf 14 

    const jsonPost = {
        "name": name.value,
        "email": email.value,
        "user_type_id": tipo,
        "password": senha,
        "is_active": "1",
        "cpf_cnpj": cpf_cnpj.value
    }

    var url = `/registrado?dados=${jsonPost}`;
    fetch(url)
        .then(response => response.text())
        .then(data => {
            console.log(data); // Exibe a resposta do servidor no console
        })
        .catch(error => {
            console.error('Erro:', error);
        });

    console.log(jsonPost)
    return true
    // window.location.href = `/registrado`
})


