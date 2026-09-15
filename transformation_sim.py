import pandas as pd

# ============================================================
# CID-10
# ============================================================

def carregar_tabela_cid(df: pd.DataFrame):
    """
    Carrega e padroniza a tabela de referência da CID-10.
    """

    df_cid = df

    df_cid["CID"] = (
        df_cid["CID"]
        .astype("string")
        .str.upper()
        .str.strip()
    )

    df_cid["Descrição"] = (
        df_cid["Descrição"]
        .astype("string")
        .str.strip()
    )

    return df_cid


def adicionar_descricao_causa(df, df_):
    """
    Adiciona ao DataFrame do SIM a descrição da causa básica
    utilizando a tabela de referência da CID-10.

    Primeiro tenta o código completo.
    Caso não encontre, tenta os 3 primeiros caracteres.
    """

    df = df.copy()

    # --------------------------------------------------------
    # Padroniza CAUSABAS
    # --------------------------------------------------------

    df["CAUSABAS_LIMPA"] = (
        df["CAUSABAS"]
        .astype("string")
        .str.upper()
        .str.strip()
    )

    # --------------------------------------------------------
    # Carrega CID
    # --------------------------------------------------------

    df_cid = carregar_tabela_cid(df_)

    # --------------------------------------------------------
    # Mapeamento pelo código completo
    # --------------------------------------------------------

    mapa_cid = (
        df_cid
        .drop_duplicates(subset=["CID"])
        .set_index("CID")["Descrição"]
    )

    df["DS_CAUSABAS"] = df["CAUSABAS_LIMPA"].map(mapa_cid)

    # --------------------------------------------------------
    # Para os que não encontraram, tenta os 3 primeiros
    # caracteres
    # --------------------------------------------------------

    mascara_sem_descricao = df["DS_CAUSABAS"].isna()

    df.loc[mascara_sem_descricao, "DS_CAUSABAS"] = (
        df.loc[mascara_sem_descricao, "CAUSABAS_LIMPA"]
        .str[:3]
        .map(mapa_cid)
    )

    # --------------------------------------------------------
    # Causas não encontradas
    # --------------------------------------------------------

    df["DS_CAUSABAS"] = (
        df["DS_CAUSABAS"]
        .fillna("Causa Desconhecida / Não Especificada")
    )

    # --------------------------------------------------------
    # Remove coluna auxiliar
    # --------------------------------------------------------

    df = df.drop(columns=["CAUSABAS_LIMPA"])

    return df


def transformar_sim(df: pd.DataFrame, df_cid: pd.DataFrame) -> pd.DataFrame:
    """
    Executa as transformações da base do SIM.
    """

    df = df.copy()

    # Colunas candidatas a remoção (vazias, constantes ou irrelevantes para a análise)
    COLUNAS_PARA_REMOVER = [
        'ESTABDESCR', 'CB_PRE', 'NUDIASOBIN', 'NUDIASINF', 'FONTESINF',
        'ORIGEM', 'NUMEROLOTE', 'FONTE', 'FONTEINV', 'FONTES', 'FONTESINF',
        'DTRECEBIM', 'DTRECORIGA', 'DTCADASTRO', 'DTATESTADO', 'DTINVESTIG',
        'DTCADINV', 'DTCONINV', 'DTCADINF', 'DTCONCASO', 'OCUPMAE',
        'STCODIFICA', 'CODIFICADO', 'VERSAOSIST', 'VERSAOSCB',
        'STDOEPIDEM', 'STDONOVA', 'TPPOS', 'TPRESGINFO', 'TPNIVELINV',
        'NUDIASOBIN', 'NUDIASINF', 'CIRURGIA', 'EXAME', 'SERIESCMAE',
        'ALTCAUSA', 'CB_PRE', 'COMUNSVOIM', 'ATESTANTE',
        'ESTABDESCR', 'NATURAL', 'CODMUNNATU', 'CONTADOR',
        'TIPOBITO', 'HORAOBITO', 'SERIESCFAL', 'MORTEPARTO', 'GESTACAO',
        'SEMAGESTAC', 'QTDFILMORT', 'PESO', 'QTDFILVIVO', 'OBITOPARTO',
        'ESCMAE2010', 'ESCMAEAGR1', 'IDADEMAE', 'PARTO', 'ESCMAE',
        'GRAVIDEZ', 'ACIDTRAB', 'NUDIASOBCO', 'TPMORTEOCO', 'OBITOGRAV',
        'OBITOPUERP', 'TPOBITOCOR',
    ]


    def decode_idade(x):
        """Decodifica o campo IDADE do SIM (1º dígito = unidade, restante = valor)."""
        if pd.isna(x):
            return None
        x = str(int(x)).zfill(3)
        unidade, valor = x[0], int(x[1:])
        if unidade == '4':
            return valor            # anos
        if unidade == '3':
            return valor / 12       # meses -> fração de ano
        if unidade in ('1', '2'):
            return valor / 365      # horas/dias -> fração de ano
        return None


    # remove colunas vazias/constantes/irrelevantes
    colunas_existentes = [c for c in COLUNAS_PARA_REMOVER if c in df.columns]
    df = df.drop(columns=colunas_existentes)

    # datas
    df['DTOBITO'] = pd.to_datetime(df['DTOBITO'], format='%d%m%Y', errors='coerce')
    df['DTNASC'] = pd.to_datetime(df['DTNASC'], format='%d%m%Y', errors='coerce')

    # idade em anos
    df['idade_anos'] = df['IDADE'].apply(decode_idade)

    # categoria CID (3 dígitos) da causa básica, útil para os gráficos de causas
    df['causa_cat'] = df['CAUSABAS'].str[:3]

    # remove duplicatas
    df = df[~df.duplicated()]

     # 1. Conversão para SEXO -> DS_SEXO
    mapeamento_sexo = {
        1: 'Masculino',
        2: 'Feminino',        
        0: 'Ignorado',
        9: 'Ignorado'
    }
    df['DS_SEXO'] = df['SEXO'].map(mapeamento_sexo).fillna('Ignorado')


    # 2. Conversão para RACACOR -> DS_RACACOR
    mapeamento_racacor = {
        1: 'Branca',
        2: 'Preta',
        3: 'Amarela',
        4: 'Parda',
        5: 'Indígena',
        9: 'Ignorado'
    }
    df['DS_RACACOR'] = df['RACACOR'].map(mapeamento_racacor).fillna('Ignorado')


    # 3. Tratamento para CAUSABAS
    df = adicionar_descricao_causa(df, df_cid)

    return df

