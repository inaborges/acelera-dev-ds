import pandas as pd

class Recomendação:
    def __init__(self):
        pass

    def cluster_rec(self, dados):
        """
        Retorna qual o cluster principal onde estão localizadas as empresas clientes
        :param dados: portfólio da empresa (dataframe)
        :return: número (int) do cluster
        """
        dados = dados[dados.empresas == 1]
        print("vendo qual o cluster predominante no dataframe...", end='')
        rec = pd.DataFrame(dados.clusters.value_counts())
        rec.reset_index(inplace=True)
        cluster = rec.iloc[0, 0]
        print('ok')
        return cluster

    def recomenda(self, i, segmento, dados):
        print("verificando quais empresas desse segmento correspondem ao cluster mais aderente a empresa...", end='')
        corte0 = dados[dados.empresas == 0]
        corte1 = corte0[corte0.segmento == segmento]
        corte2 = corte1[corte1.clusters == i]
        empresas_rec = corte2.loc[:,'id']
        print('ok')
        return list(empresas_rec)