import pandas as pd

class UnindoDF:
    def __init__(self):
        pass

    def unir_df(self, df, portfolio):
        """
        Seleciona a coluna de ID do portfólio e une com o dataframe geral
        :param df: dataframe com todas as empresas
        :param portfolio: portfólio de uma empresa
        :return: retorna dataframe unido com coluna de 'pertencentes ao portfólio'
        """

        # selecionando só a coluna ID da empresa
        portfolio = pd.DataFrame(portfolio.loc[:, 'id'])
        # criando nova coluna de valores = 1
        portfolio['empresas'] = 1

        df_unido = pd.merge(df, portfolio, how='outer', on='id')
        df_unido = df_unido.fillna(0)

        return df_unido
