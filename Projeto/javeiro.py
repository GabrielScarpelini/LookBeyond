# Definir os dados necessários
dados_necessarios = [
    "nome",
    "cpf",
    "rg",
    "data_nascimento",
    "endereco",
    "telefone",
    "email",
    "formacao_academica",
    "experiencia_profissional",
    "areas_atuacao",
]

# Criar um formulário
form = {
    campo: forms.CharField(max_length=255)
    for campo in dados_necessarios
}

# Validar os dados
for campo in dados_necessarios:
    dado = form.get(campo)
    if not dado:
        raise ValueError(f"O campo {campo} é obrigatório.")

    if not isinstance(dado, str):
        raise ValueError(f"O campo {campo} deve ser do tipo string.")

    if len(dado) > 255:
        raise ValueError(f"O campo {campo} deve ter no máximo 255 caracteres.")

# Cadastrar o professor
professor = Professor(
    nome=form["nome"],
    cpf=form["cpf"],
    rg=form["rg"],
    data_nascimento=form["data_nascimento"],
    endereco=form["endereco"],
    telefone=form["telefone"],
    email=form["email"],
    formacao_academica=form["formacao_academica"],
    experiencia_profissional=form["experiencia_profissional"],
    areas_atuacao=form["areas_atuacao"],
)

# Atualizar o status do professor
professor.status = "cadastrado"

# Salvar o professor no banco de dados
professor.save()