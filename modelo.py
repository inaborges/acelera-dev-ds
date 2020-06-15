import pandas as pd
from sklearn.cluster import KMeans

class Modelo:
    def __init__(self):
        pass

    def pre_modelo(self, dados):
        """
        Seleciona features e aplica KMeans com k=7
        :param dados: dataframe com as empresas
        :return: retorna o dataframe com a coluna de clusters
        """
        print('selecionando as features...', end='')
        features = ['idade_empresa_anos', 'fl_rm', 'nm_segmento', 'vl_total_veiculos_pesados_grupo',
                    'de_nivel_atividade', 'sg_uf', 'qt_socios',
                    'vl_faturamento_estimado_grupo_aux', 'qt_filiais']
        X = dados[features]
        print('ok')
        print('aplicando get_dummies nas variáveis categóricas...', end='')
        X_dummies = pd.get_dummies(X)
        print('ok')
        return X_dummies

    def kmeans(self, dados, i):
        print("aplicando k-means no dataframe...", end='')
        kmeans = KMeans(i)
        clusters = kmeans.fit_predict(dados)
        dados['clusters'] = clusters
        print('ok')
        return dados

