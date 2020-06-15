import streamlit as st
import pandas as pd

def main():
	st.title("Sistema de Recomendação")
	st.image('conexao.jpeg')
	st.markdown("--------------")

	st.header("Objetivo")
	st.markdown("O objetivo dessa aplicação é, a partir de um portfólio de empresas, recomendar novas empresas aderentes à esse portfólio.")
	st.markdown("--------------")

	df = pd.read_csv("dados_trabalhados/ids_clusters.csv")
	df.drop('Unnamed: 0', axis=1, inplace=True)

	st.header("Faça o upload de seu portfólio de clientes:")
	file = st.file_uploader("Selecione seu arquivo *.csv", type='csv')
	if file is None:
		st.text("Nenhum arquivo selecionado")
	if file is not None:
		portfolio = pd.read_csv(file)
		st.markdown("Seu portfólio possui "+str(portfolio.shape[0])+" empresas e "+str(portfolio.shape[1])+" colunas.")
		numero = st.slider("Selecione o número de linhas que deseja visualizar:",1,10)
		st.dataframe(portfolio.head(numero))

		st.markdown("Se tudo estiver ok, vamos utilizar esse dataframe para selecionar possíveis clientes")
		botao = st.button("Clique para continuar.")
		if botao:
			st.markdown("Selecionando possíveis clientes...")
			portfolio = pd.DataFrame(portfolio.loc[:, 'id'])
			portfolio['empresas'] = 1

			#unindo o portfolio com a base de empresas
			df_unido = pd.merge(df, portfolio, how='outer', on='id')
			df_unido = df_unido.fillna(0)

			#selecionando os clientes:
			cluster = df_unido[df_unido.empresas == 1]
			rec = pd.DataFrame(cluster.clusters.value_counts())
			rec.reset_index(inplace=True)
			cluster = rec.iloc[0, 0]

			corte0 = df_unido[df_unido.empresas == 0]
			corte1 = corte0[corte0.clusters == cluster]
			empresas_rec = corte1.loc[:, 'id']

			st.markdown("Vendo algumas das empresas recomendadas:")
			st.markdown(list(empresas_rec[0:11]))

if __name__ == '__main__':
	main()

