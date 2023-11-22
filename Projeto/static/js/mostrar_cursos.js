var email = localStorage.getItem('email')

function mostrarCurso(){
    var span = document.getElementsByClassName('adiciona_curso')
    var meuCurso = document.getElementsByClassName('bi bi-book')
    var adicionaCurso = document.getElementsByClassName('bi bi-camera-video')
    var btnShow = document.getElementById('adicionarCurso')
    
    

    if(email == 'teste@teste'){
        document.querySelector('nav').style.display = 'none'
        document.getElementById("[data-div]").style.display = "none";
    } else {
        alert('Sou else')
        
    }
    console.log(email == 'teste@teste')
}


// if(inputPass.type === 'password'){
//     inputPass.setAttribute('type', 'text')
    
// } else {
//     inputPass.setAttribute('type', 'password')
//     btnShowPass.classList.replace('bi-eye-slash-fill', 'bi-eye-fill')
// }