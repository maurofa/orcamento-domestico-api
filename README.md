# orcamento-domestico-api

API do Sistema de Orçamento Doméstico, feito usando Python e Flask. Na persistência será utilizado o SQLite.

Serviços disponibilizados:

- POST /lancamentos: Lança débitos ou créditos
- GET /grupos: traz os grupos de conta
- GET /lancamentos: gerar o orçamento mensal
- PUT /lancamentos/<idLancamento>/alterar: altera um lançamento
- DELETE /lancamentos/<idLancamento>/excluir: exclui um lançamento

Será disponibilizado o swagger com a documentação no seguinte endereço: /openapi

---

## Como executar

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```shell
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```shell
(env)$ flask run --host 127.0.0.1 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte.

```shell
(env)$ flask run --host 127.0.0.1 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
