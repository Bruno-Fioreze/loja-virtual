window.addEventListener("load", function(){

    let cep = document.getElementById("id_cep")
    cep.addEventListener("keypress", function(event){
        if(event.which == 13 && cep.value.length == 8){
            get_cep(cep.value)
        }
    })
    if (cep.value.length == 0){
        cep.classList.add("pulse")
    }
})

function submit_form(){
    document.getElementById("form_atualizar_cadastrar").submit()
}

function get_cep(cep){
    url = "https://viacep.com.br/ws/"+cep+"/json/unicode/"
    fetch(url).then((response) => response.json())
    .then(function(dados) {

        if(dados["erro"] == true){
            Swal.fire(
              'Erro!',
              'Não encontrei o cep informado!',
              'error'
            )
            return
        }
        document.getElementById("id_bairro").value = dados["bairro"]
        document.getElementById("id_cidade").value = dados["localidade"]
        document.getElementById("id_estado").value = dados["uf"]
        document.getElementById("id_endereco").value = dados["logradouro"]
        document.getElementById("id_cep").classList.remove("pulse")
        document.getElementById("id_cep").classList.add("border-success")
        setTimeout(function(){
            document.getElementById("id_cep").classList.remove("border-success")
        }, 3000)
    })
    .catch(function(error) {
        Swal.fire(
          'Erro!',
          'Não encontrei o cep informado!',
          'error'
        )
        setTimeout(function(){
            document.getElementById("id_cep").focus()
        },1500)
    });
}