import pandas as pd
from sklearn.preprocessing import StandardScaler

class LimpezaDados:
    def __init__(self):
        pass

    def remove_NA(self, dados):
        """
        remove colunas com mais de 70% de NA
        :param dados: recebe dataframes
        :return: retorna mesmo dataframe, com as colunas removidas
        """
        print("removendo colunas com mais de 70% de NA...", end="")
        aux = pd.DataFrame({'colunas': dados.columns,
                            'missing': ((dados.isna().sum() / dados.shape[0]) * 100)})
        to_drop = aux.query('missing > 70')
        to_drop = list(to_drop.colunas)
        dados.drop(to_drop, axis=1, inplace=True)
        print("ok")
        return dados

    def remove_desnecessarias(self, dados):
        """
        Remove colunas desnecessárias do dataframe
        :param dados: recebe dataframe
        :return: retorna dataframe sem as colunas desnecessárias
        """
        print("removendo colunas desnecessárias para o projeto...", end="")
        dados.drop(['fl_email', 'fl_telefone', 'dt_situacao',
                    'de_saude_rescencia', 'nu_meses_rescencia'], axis=1, inplace=True)
        print("ok")
        return dados

    def analise_exploratoria(self, dados):
        """
        Remove as colunas redundantes e desnecessárias, a partir da análise exploratória
        :param dados: recebe dataframe
        :return: retorna dataframe sem as colunas desnecessárias
        """
        print("removendo colunas redundantes e desnecessárias para o projeto...", end="")
        dados.drop(['fl_me', 'fl_sa', 'fl_epp', 'fl_mei', 'fl_ltda',
                    'fl_st_especial', 'fl_simples_irregular',
                    'fl_veiculo', 'fl_spa', 'fl_antt',
                    'setor', 'de_natureza_juridica', 'natureza_juridica_macro', 'de_saude_tributaria',
                    'sg_uf_matriz', 'nm_micro_regiao',
                    'qt_socios_pf', 'qt_socios_pj', 'idade_maxima_socios', 'idade_minima_socios',
                    'qt_socios_st_regular', 'qt_socios_masculino', 'qt_socios_feminino',
                    'de_faixa_faturamento_estimado', 'de_faixa_faturamento_estimado_grupo',
                    'vl_faturamento_estimado_aux','idade_emp_cat'], axis=1, inplace=True)
        print("ok")
        return dados

class Tratamento:
    def __init__(self):
        pass

    def tratando_categoricas(self, dados):
        """
        Trata dados categóricos do dataframe estudado
        :param dados: recebe dataframe
        :return: retorna dataframe com dados trabalhados
        """
        print("transformando nível de atividade em números...", end="")
        dados.de_nivel_atividade = dados.de_nivel_atividade.map({'ALTA':4,'BAIXA':2,'MEDIA':3,'MUITO BAIXA':1})
        dados.de_nivel_atividade = dados.de_nivel_atividade.fillna(0)
        print('ok')

        print("transformando alguns dados em booleanos...", end='')
        dados.fl_rm = dados.fl_rm.map({'SIM': True, 'NAO': False})
        dados.fl_passivel_iss = dados.fl_passivel_iss.astype('bool')
        dados.fl_optante_simei = dados.fl_optante_simei.astype('bool')
        dados.fl_optante_simples = dados.fl_optante_simples.astype('bool')
        print('ok')

        print('preenchendo os NA de meso_região com valores de UF correspondentes...', end='')
        dados.nm_meso_regiao = dados.nm_meso_regiao.fillna(0)
        for i in range(0, len(dados)):
            if dados.loc[i, 'nm_meso_regiao'] == 0:
                dados.loc[i, 'nm_meso_regiao'] = dados.loc[i, 'sg_uf']
        print('ok')

        print('preenchendo dados de divisao e segmento vazios com OUTROS...', end='')
        dados.nm_divisao = dados.nm_divisao.fillna('OUTROS')
        dados.nm_segmento = dados.nm_segmento.fillna('OUTROS')
        print('ok')

        return dados

    def tratando_numericas(self, dados):
        """
        Trata dados numéricos do dataframe estudado
        :param dados: recebe dataframe
        :return: retorna dataframe com valores imputados com média
        """
        print('imputando os NA com a média...', end='')
        dados.idade_empresa_anos = dados.idade_empresa_anos.fillna(dados.idade_empresa_anos.mean())
        dados.vl_total_veiculos_pesados_grupo = dados.vl_total_veiculos_pesados_grupo.fillna(dados.vl_total_veiculos_pesados_grupo.mean())
        dados.vl_total_veiculos_leves_grupo = dados.vl_total_veiculos_leves_grupo.fillna(dados.vl_total_veiculos_leves_grupo.mean())
        dados.empsetorcensitariofaixarendapopulacao = dados.empsetorcensitariofaixarendapopulacao.fillna(dados.empsetorcensitariofaixarendapopulacao.mean())
        dados.qt_socios = dados.qt_socios.fillna(dados.qt_socios.mean())
        dados.vl_faturamento_estimado_grupo_aux = dados.vl_faturamento_estimado_grupo_aux.fillna(dados.vl_faturamento_estimado_grupo_aux.mean())
        dados.idade_media_socios = dados.idade_media_socios.fillna(dados.idade_media_socios.mean())
        dados.qt_filiais = dados.qt_filiais.fillna(dados.qt_filiais.mean())
        print('ok')
        return dados

    def padronizando_numericas(self, dados):
        """
        Padroniza (com standard scaler) as variáveis numéricas
        :param dados: recebe dataframe
        :return: retorna dataframe com as variáveis numéricas padronizadas
        """
        print("padronizando as variáveis numéricas...", end='')
        scaler = StandardScaler()
        numericas = dados.select_dtypes('number')
        num_trans = scaler.fit_transform(numericas)
        num_trans = pd.DataFrame(num_trans, columns=numericas.columns)
        print('ok')
        categoricas = dados.drop(numericas.columns, axis=1)
        resultado = pd.concat([categoricas, num_trans], axis=1)
        return resultado