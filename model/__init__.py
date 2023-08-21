from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, event
import os

# importando os elemetos definidos no modelo
from model.base import Base
from model.grupo import Grupo
from model.grupo import SubGrupo
from model.lancamento import Lancamento

db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
  # então cria o diretório
  os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

#cria a engine de conexão com o banco
engine = create_engine(db_url, echo=True)

# cria o banco se ele não existir
if not database_exists(engine.url):
  create_database(engine.url)

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)

with Session(engine) as session:
  count = session.query(Grupo).count()
  if not count:
    grupoReceita = Grupo(
        descricao = "Receita",
        subGrupos = [
          SubGrupo(descricao = "Salário / Adiantamento"),
          SubGrupo(descricao = "Férias"),
          SubGrupo(descricao = "13º salário"),
          SubGrupo(descricao = "Aposentadoria"),
          SubGrupo(descricao = "Receita extra (aluguel, restituição IR)"),
          SubGrupo(descricao = "Outras Receitas"),
        ]
      )
    grupoAlimentacao = Grupo(
      descricao = "Alimentação",
      subGrupos = [
        SubGrupo(descricao = "Supermercado"),
        SubGrupo(descricao = "Feira / Sacolão"),
        SubGrupo(descricao = "Padaria"),
        SubGrupo(descricao = "Refeição fora de casa"),
        SubGrupo(descricao = "Outros (café, água, sorvetes, etc)"),
      ]
    )
    grupoMoradia = Grupo(
      descricao = "Moradia",
      subGrupos = [
        SubGrupo(descricao = "Prestação / Aluguel de imóvel"),
        SubGrupo(descricao = "Condomínio"),
        SubGrupo(descricao = "Consumo de água"),
        SubGrupo(descricao = "Serviço de limpeza (diarista ou mensalista)"),
        SubGrupo(descricao = "Energia Elétrica"),
        SubGrupo(descricao = "Gás"),
        SubGrupo(descricao = "IPTU"),
        SubGrupo(descricao = "Decoração da casa"),
        SubGrupo(descricao = "Manutenção / Reforma da casa"),
        SubGrupo(descricao = "Celular"),
        SubGrupo(descricao = "Telefone fixo"),
        SubGrupo(descricao = "Internet / TV a cabo"),
      ]
    )
    grupoEducacao = Grupo(
      descricao = "Educação",
      subGrupos = [
        SubGrupo(descricao = "Matrícula Escolar / Mensalidade"),
        SubGrupo(descricao = "Material Escolar"),
        SubGrupo(descricao = "Outros Cursos"),
        SubGrupo(descricao = "Transporte Escolar"),
      ]
    )
    grupoAnimalEstimacao = Grupo(
      descricao = "Animal de Estimação",
      subGrupos = [
        SubGrupo(descricao = "Ração"),
        SubGrupo(descricao = "Banho / Tosa"),
        SubGrupo(descricao = "Veterinário / medicamento"),
        SubGrupo(descricao = "Outros (acessórios, brinquedos, hotel, dog walker)"),
      ]
    )
    grupoSaude = Grupo(
      descricao = "Saúde",
      subGrupos = [
        SubGrupo(descricao = "Plano de saúde"),
        SubGrupo(descricao = "Medicamentos"),
        SubGrupo(descricao = "Dentista"),
        SubGrupo(descricao = "Terapia / Psicólogo / Acunputura"),
        SubGrupo(descricao = "Médicos / Exames fora do plano de saúde"),
        SubGrupo(descricao = "Academia / Tratamento Estético"),
      ]
    )
    grupoTransporte = Grupo(
      descricao = "Transporte",
      subGrupos = [
        SubGrupo(descricao = "Ônibus / Metrô"),
        SubGrupo(descricao = "Taxi"),
        SubGrupo(descricao = "Combustível"),
        SubGrupo(descricao = "Estacionamento"),
        SubGrupo(descricao = "Seguro Auto"),
        SubGrupo(descricao = "Manutenção / Lavagem / Troca de óleo"),
        SubGrupo(descricao = "Licenciamento"),
        SubGrupo(descricao = "Pedágio"),
        SubGrupo(descricao = "IPVA"),
      ]
    )
    grupoPessoais = Grupo(
      descricao = "Pessoais",
      subGrupos = [
        SubGrupo(descricao = "Vestuário / Calçados / Acessórios"),
        SubGrupo(descricao = "Cabeleireiro / Manicure / Higiene pessoal"),
        SubGrupo(descricao = "Presentes"),
        SubGrupo(descricao = "Outros"),
        SubGrupo(descricao = "Dízimos e ofertas"),
      ]
    )
    grupoLazer = Grupo(
      descricao = "Lazer",
      subGrupos = [
        SubGrupo(descricao = "Cinema / Teatro / Shows"),
        SubGrupo(descricao = "Livros / Revistas / Cd's"),
        SubGrupo(descricao = "Clube / Parques / Casa Noturna"),
        SubGrupo(descricao = "Viagens"),
        SubGrupo(descricao = "Restaurantes / Bares / Festas"),
      ]
    )
    grupoFinanceiro = Grupo(
      descricao = "Serviços Financeiros",
      subGrupos = [
        SubGrupo(descricao = "Empréstimos"),
        SubGrupo(descricao = "Seguros (vida / residencial)"),
        SubGrupo(descricao = "Previdência privada"),
        SubGrupo(descricao = "Juros Cheque Especial"),
        SubGrupo(descricao = "Tarifas bancárias"),
        SubGrupo(descricao = "Financiamento de veículo"),
        SubGrupo(descricao = "Pagamento da fatura do cartão de crédito"),
        SubGrupo(descricao = "Imposto de Renda a Pagar"),
        SubGrupo(descricao = "Saque"),
      ]
    )
    session.add_all([
      grupoReceita,
      grupoAlimentacao,
      grupoMoradia,
      grupoEducacao,
      grupoAnimalEstimacao,
      grupoSaude,
      grupoTransporte,
      grupoPessoais,
      grupoLazer,
      grupoFinanceiro,
    ])
    session.commit()
