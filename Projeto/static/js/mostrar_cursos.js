// import { conectaApi } from "./conectaApi.js"


// const lista = document.querySelector("[data-lista]")

// function cadastrarCurso(titulo, descricao, url, imagem){
//     const curso = document.createElement("li")
//     curso.className = "cursos__item"
//     curso.innerHTML = `<iframe width="100%" height="72%" src="${url}"
//                     title="${titulo}" frameborder="0"
//                     allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
//                     allowfullscreen></iframe>
//                 <div class="descricao-curso">
//                 <img src="${imagem}">
//                     <h3>${titulo}</h3>
//                     <p>${descricao}</p>
//                 </div>`
//     return curso
// }

// async function listaCursos() {
//     const listaApi = await conectaApi.listaCursos();
//     listaApi.forEach(elemento => lista.appendChild(
//         cadastrarCurso(elemento.titulo, elemento.descricao,elemento.url, elemento.imagem)))
// }

// listaCursos();