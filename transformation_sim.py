import pandas as pd


def transformar_sim(df: pd.DataFrame) -> pd.DataFrame:
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

    return df

