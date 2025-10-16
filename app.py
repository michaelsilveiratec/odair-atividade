# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(
    page_title="Shopee Sales Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# CSS simplificado
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        color: #EE4D2D;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #EE4D2D;
    }
</style>
""", unsafe_allow_html=True)

# Barra lateral
with st.sidebar:
    st.markdown("## 🛍️ Shopee Dashboard")
    st.markdown("---")
    st.markdown("**Filtros:**")
    mes = st.selectbox("Mês", ["Todos", "Janeiro", "Fevereiro", "Março"])
    categoria = st.multiselect("Categoria", ["Eletrônicos", "Roupas", "Casa", "Beleza"])

# Dados de exemplo
@st.cache_data
def load_data():
    return pd.DataFrame({
        'Dia': [f'{i}/06' for i in range(1, 31)],
        'Vendas (R$)': [1200 + i*100 + (-1)**i * 200 for i in range(30)],
        'Pedidos': [50 + i*5 for i in range(30)],
        'Ticket Médio (R$)': [45, 44, 47, 46, 48, 49, 50, 49, 51, 52] * 3,
    })

df = load_data()

# Conteúdo principal
st.markdown("<div class='main-header'>Dashboard de Vendas - Shopee</div>", unsafe_allow_html=True)

# Métricas principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class='metric-card'>
        <div>Vendas Totais</div>
        <div style='font-size: 1.5rem; font-weight: bold;'>R$ 42.350</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='metric-card'>
        <div>Pedidos</div>
        <div style='font-size: 1.5rem; font-weight: bold;'>1.240</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='metric-card'>
        <div>Ticket Médio</div>
        <div style='font-size: 1.5rem; font-weight: bold;'>R$ 48,50</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='metric-card'>
        <div>Crescimento</div>
        <div style='font-size: 1.5rem; font-weight: bold;'>+12%</div>
    </div>
    """, unsafe_allow_html=True)

# Gráficos
col1, col2 = st.columns(2)

with col1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Dia'], 
        y=df['Vendas (R$)'],
        mode='lines',
        name='Vendas Diárias',
        line=dict(color='#EE4D2D')
    ))
    fig.update_layout(title='Vendas Diárias (Últimos 30 dias)', height=300)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Dia'][:7], 
        y=df['Pedidos'][:7],
        name='Pedidos Recentes',
        marker_color='#FF6B6B'
    ))
    fig.update_layout(title='Pedidos na Última Semana', height=300)
    st.plotly_chart(fig, use_container_width=True)

# Tabela de dados
st.markdown("### Dados Detalhados")
st.dataframe(df, use_container_width=True)

# Status
st.markdown("### Status do Mês")
col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Meta do Mês:** R$ 40.000")

with col2:
    st.success("**Atingido:** 105%")

with col3:
    st.warning("**Dias Restantes:** 15")