import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Configuração da página da Web
st.set_page_config(page_title="Dashboard Corporativo", layout="wide")

st.title("📊 Painel de Análise Financeira e de Vendas")
st.write("Insira sua planilha abaixo para rodar as análises automatizadas de lucro e imposto.")

# Caixa de upload que aceita CSV e Excel
arquivo_enviado = st.file_uploader("Escolha um arquivo CSV ou Excel", type=["csv", "xlsx"])

if arquivo_enviado is not None:
    # Identifica a extensão do arquivo enviado
    if arquivo_enviado.name.endswith('.csv'):
        df = pd.read_csv(arquivo_enviado)
    else:
        df = pd.read_excel(arquivo_enviado)
    
    # Validação de segurança das colunas originais
    if "Produto" in df.columns and "Vendas" in df.columns:
        
        # 2. ENRIQUECIMENTO DOS DADOS (O que aprendemos na Fase 2)
        df["Imposto"] = df["Vendas"] * 0.10
        df["Lucro"] = df["Vendas"] - df["Imposto"]
        
        # Consolidação e ordenação pelo lucro
        lucro_por_produto = df.groupby("Produto")["Lucro"].sum().reset_index()
        lucro_por_produto = lucro_por_produto.sort_values(by="Lucro", ascending=False)
        
        # Cálculos de somatórios gerais para os cards
        faturamento_geral = df["Vendas"].sum()
        imposto_geral = df["Imposto"].sum()
        lucro_geral = df["Lucro"].sum()

        # 3. SEÇÃO DE MÉTRICAS (Cards de destaque na tela)
        st.subheader("📌 Indicadores Financeiros Consolidados")
        col1, col2, col3 = st.columns(3) # Cria 3 colunas horizontais equilibradas
        
        # Exibe os valores formatados no padrão de moeda
        col1.metric("Faturamento Bruto", f"R$ {faturamento_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        col2.metric("Imposto Retido (10%)", f"R$ {imposto_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        col3.metric("Lucro Líquido Real", f"R$ {lucro_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        
        st.markdown("---") # Linha horizontal divisória

        # 4. SEÇÃO GRÁFICA (O que aprendemos na Fase 3)
        st.subheader("📈 Distribuição de Lucro por Categoria de Produto")
        
        # Criação do gráfico utilizando as customizações que vimos
        fig, ax = plt.subplots(figsize=(10, 4))
        barras = ax.bar(lucro_por_produto["Produto"], lucro_por_produto["Lucro"], color="#E67E22")
        
        # Adiciona a grade de fundo e rótulos
        ax.set_axisbelow(True)
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        ax.bar_label(barras, padding=3, fmt='R$ %.2f')
        
        # Estilização moderna removendo as bordas da caixa externa
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_ylabel("Lucro (R$)")
        
        plt.tight_layout()
        st.pyplot(fig) # Renderiza o gráfico do Matplotlib na interface web
        
        # 5. TABELA DE DADOS ATUALIZADA
        st.markdown("---")
        st.subheader("👀 Visualização da Tabela de Dados Processada")
        st.dataframe(df, use_container_width=True)
        
    else:
        st.error("Erro crítico: Verifique se sua planilha possui as colunas 'Produto' e 'Vendas'.")
else:
    st.info("💡 Pronto para iniciar. Faça o upload de um arquivo para estruturar o painel.")
