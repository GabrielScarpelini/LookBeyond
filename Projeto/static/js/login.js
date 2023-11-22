function mostrarSenha(){
    var inputPass = document.getElementById('senha')
    var btnShowPass = document.getElementById('btn-senha')

    if(inputPass.type === 'password'){
        inputPass.setAttribute('type', 'text')
        btnShowPass.classList.replace('bi-eye-fill', 'bi-eye-slash-fill')
    } else {
        inputPass.setAttribute('type', 'password')
        btnShowPass.classList.replace('bi-eye-slash-fill', 'bi-eye-fill')
    }
}

const btnEntrar = document.getElementById('send')

btnEntrar.addEventListener('click', function(e) {
    //e.preventDefault();
    var email = document.getElementById('userEmail').value
    localStorage.setItem("email", email)
})



