import streamlit as st
import pandas as pd
import plotly.express as px  # Importando o Plotly Express

# 1. Configuração da página da Web
st.set_page_config(page_title="Dashboard Interativo Plotly", layout="wide")

st.title("📊 Dashboard Interativo de Dados (Plotly)")
st.write("Gráficos modernos que atualizam em tempo real e reagem ao mouse.")

# Caixa de upload para CSV ou Excel
arquivo_enviado = st.file_uploader("Escolha um arquivo CSV ou Excel", type=["csv", "xlsx"])

if arquivo_enviado is not None:
    # Identifica e lê a extensão do arquivo enviado
    if arquivo_enviado.name.endswith('.csv'):
        df = pd.read_csv(arquivo_enviado)
    else:
        df = pd.read_excel(arquivo_enviado)
    
    # Validação das colunas
    if "Produto" in df.columns and "Vendas" in df.columns:
        
        # 2. PROCESSAMENTO DOS DADOS COM PANDAS
        df["Imposto"] = df["Vendas"] * 0.10
        df["Lucro"] = df["Vendas"] - df["Imposto"]
        
        lucro_por_produto = df.groupby("Produto")["Lucro"].sum().reset_index()
        lucro_por_produto = lucro_por_produto.sort_values(by="Lucro", ascending=False)
        
        # Métricas gerais
        faturamento_geral = df["Vendas"].sum()
        lucro_geral = df["Lucro"].sum()

        # 3. SEÇÃO DE MÉRICAS (Cards de destaque)
        col1, col2 = st.columns(2)
        col1.metric("Faturamento Bruto", f"R$ {faturamento_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        col2.metric("Lucro Líquido Real", f"R$ {lucro_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        
        st.markdown("---")

        # 4. SEÇÃO GRÁFICA INTERATIVA COM PLOTLY
        st.subheader("📈 Gráfico Dinâmico: Lucro por Produto")
        
        # Criando o gráfico de barras com Plotly Express (Apenas 1 linha de código!)
        fig = px.bar(
            lucro_por_produto, 
            x="Produto", 
            y="Lucro",
            text_auto='.2f', # Adiciona os valores em cima das barras automaticamente
            title="Lucro Total por Categoria",
            labels={"Lucro": "Lucro Líquido (R$)", "Produto": "Categorias"}, # Muda os nomes dos eixos
            color="Lucro", # Cria um degradê automático baseado no valor do lucro!
            color_continuous_scale="Oranges" # Paleta de cores laranja/coral combinando com o post
        )
        
        # Ajustes finos de layout do Plotly para remover linhas desnecessárias
        fig.update_layout(
            xaxis_title="Produtos",
            yaxis_title="Lucro (R$)",
            coloraxis_showscale=False, # Esconde a barra lateral de legenda do degradê
            template="plotly_white" # Fundo branco limpo e moderno
        )

        # Comando exclusivo do Streamlit para renderizar gráficos do Plotly
        st.plotly_chart(fig, use_container_width=True)
        
        # 5. TABELA DE DADOS
        st.markdown("---")
        st.subheader("👀 Dados Processados")
        st.dataframe(df, use_container_width=True)
        
    else:
        st.error("Erro: O arquivo precisa conter as colunas 'Produto' e 'Vendas'.")
else:
    st.info("💡 Aguardando o envio de um arquivo para gerar o painel.")
