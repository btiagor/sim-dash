# Dashboard SIM — Sistema de Informação sobre Mortalidade

Dashboard para exploração e análise dos dados do **Sistema de Informação sobre Mortalidade (SIM)**, desenvolvido com **Python**, **Streamlit**, **DuckDB**, **Pandas** e **Plotly**.

## Objetivo

Construir uma aplicação para visualização e análise dos óbitos registrados no SIM, permitindo explorar:

- volume de óbitos;
- evolução temporal;
- perfil demográfico;
- sexo;
- raça/cor;
- principais causas básicas de morte;
- distribuição territorial dos óbitos.

## Tecnologias

| Tecnologia | Utilização |
|---|---|
| Python | Linguagem principal |
| Streamlit | Dashboard |
| DuckDB | Banco analítico local |
| Pandas | Manipulação dos dados |
| Plotly | Visualizações interativas |

## Estrutura do projeto

```text
sim-dash/
│
├── app.py
├── app_geral.py
├── app_perfil.py
├── app_causas.py
├── app_territorio.py
│
├── queries.py
│
├── database/
│   ├── __init__.py
│   └── duckdb.py
│
├── ingestion_sim.py
├── transformation_sim.py
├── importar_sim.py
│
├── data/
│   ├── raw/
│   │   └── base_sim_do.xlsx
│   └── database/
│       └── sim.duckdb
│
├── requirements.txt
├── README.md
└── .gitignore
```

### Responsabilidade dos arquivos

- **`app.py`** — ponto de entrada e navegação entre as páginas.
- **`app_geral.py`** — página Visão Geral.
- **`app_perfil.py`** — análises do perfil demográfico.
- **`app_causas.py`** — análises das causas de morte e CID-10.
- **`app_territorio.py`** — análises territoriais.
- **`queries.py`** — consultas SQL executadas no DuckDB.
- **`ingestion_sim.py`** — leitura/entrada da base do SIM.
- **`transformation_sim.py`** — limpeza e transformação dos dados.
- **`importar_sim.py`** — script para orquestrar a importação dos dados para o banco.
- **`database/duckdb.py`** — conexão e operações relacionadas ao DuckDB.

## Fluxo de dados

```text
                BASE SIM
             arquivo XLSX
                   │
                   ▼
          ingestion_sim.py
                   │
                   ▼
        transformation_sim.py
                   │
                   ▼
              DuckDB
           sim.duckdb
                   │
                   ▼
              queries.py
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
      Geral     Perfil     Causas
        │          │          │
        └──────────┼──────────┘
                   ▼
              Território
                   │
                   ▼
             Streamlit
```

## Banco de dados

O banco analítico utilizado é o **DuckDB**:

```text
data/database/sim.duckdb
```

A base original fica em:

```text
data/raw/base_sim_do.xlsx
```

A separação permite preservar o arquivo bruto e utilizar o DuckDB para as consultas do dashboard.

## Consultas iniciais

A primeira versão utiliza:

```python
total_obitos()
obitos_por_ano()
obitos_por_sexo()
obitos_por_raca()
top_causas()
```

Essas consultas alimentam principalmente a página **Visão Geral**.

## Páginas do dashboard

### 1. Visão Geral

Panorama dos dados:

- total de óbitos;
- óbitos no último ano;
- evolução temporal;
- óbitos por sexo;
- óbitos por raça/cor;
- principais causas básicas de morte.

### 2. Perfil Demográfico

Análises de:

- sexo;
- raça/cor;
- idade;
- faixas etárias;
- cruzamentos demográficos.

### 3. Causas de Morte

Análises de:

- principais causas;
- CID-10;
- causas por período;
- causas por sexo;
- causas por raça/cor;
- causas por faixa etária.

### 4. Território

Análises de:

- município de residência;
- município de ocorrência;
- fluxo residência → ocorrência;
- óbitos fora do município de residência;
- mapas temáticos.

## Como Executar o Projeto

Siga os passos abaixo para configurar o ambiente, importar os dados e rodar o projeto na sua máquina:

### 1. Criar e Ativar o Ambiente Virtual (venv)

Na raiz do projeto, crie o ambiente virtual e ative-o:

- **No Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

- **No Windows (PowerShell / CMD):**
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```

### 2. Instalar as Dependências

Com o ambiente virtual ativado, instale os pacotes listados no `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Importar a Base de Dados

Execute o script de importação para processar a planilha bruta e gerar o banco DuckDB (`sim.duckdb`):

```bash
python importar_sim.py
```

Fluxo esperado da importação:
```text
base_sim_do.xlsx
       ↓
ingestion_sim.py
       ↓
transformation_sim.py
       ↓
sim.duckdb
```

### 4. Executar o Dashboard (Streamlit)

Com os dados devidamente importados, inicie a aplicação Streamlit:

```bash
streamlit run app.py
```

O painel estará disponível no navegador através do endereço:
```text
http://localhost:8501
```

## Desenvolvimento

As responsabilidades devem permanecer separadas:

```text
Entrada dos dados       → ingestion_sim.py
Tratamento              → transformation_sim.py
Banco                   → database/duckdb.py
Consultas SQL           → queries.py
Visualizações           → app_*.py
Navegação               → app.py
```

Evite colocar SQL diretamente nas páginas do Streamlit quando a consulta puder ser reutilizada.

## Análise exploratória

O Jupyter Notebook pode ser utilizado para:

- conhecer a estrutura da base;
- avaliar qualidade dos dados;
- testar transformações;
- desenvolver indicadores;
- prototipar visualizações.

Depois de validadas, as regras devem ser migradas para os módulos Python.

## Próximas etapas

### Curto prazo

- [ ] Validar a importação completa da base SIM.
- [ ] Validar as transformações.
- [ ] Validar as consultas iniciais.
- [ ] Construir a página Visão Geral.
- [ ] Padronizar sexo e raça/cor.
- [ ] Melhorar rótulos e tooltips.

### Médio prazo

- [ ] Filtro por período.
- [ ] Filtro por sexo.
- [ ] Filtro por raça/cor.
- [ ] Análise por faixa etária.
- [ ] Análise por capítulos CID-10.
- [ ] Página de causas.
- [ ] Página territorial.
- [ ] Mapas por município.

### Evolução analítica

- [ ] Mortalidade infantil.
- [ ] Mortalidade materna.
- [ ] Causas externas.
- [ ] Taxas de mortalidade.
- [ ] Indicadores por população.
- [ ] Análises temporais detalhadas.
- [ ] Comparação entre município de residência e ocorrência.

## Princípios

1. **Separação de responsabilidades** — cada arquivo possui uma função clara.
2. **Reprodutibilidade** — o processamento deve poder ser executado novamente.
3. **Preservação dos dados brutos** — a base original permanece separada.
4. **SQL separado da apresentação** — consultas ficam em `queries.py`.
5. **Dashboard focado em análise** — a camada Streamlit apresenta os resultados.
6. **Evolução incremental** — novas análises são adicionadas após validação.

## Dados e privacidade

A utilização e divulgação dos dados devem observar as regras aplicáveis à base do SIM, incluindo as orientações de proteção de informações pessoais e de uso adequado dos dados.

## Autor

Projeto desenvolvido para exploração, análise e visualização de dados do Sistema de Informação sobre Mortalidade (SIM).
