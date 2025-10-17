# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(
    page_title="Shein Sales Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# CSS melhorado
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        color: #EE4D2D;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f9fafb;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #EE4D2D;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: 0.3s;
        text-align: center;
    }
    .metric-card:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# Barra lateral com filtros
with st.sidebar:
    st.markdown("## 🛍️ Shein Dashboard")
    st.markdown("---")
    st.markdown("**Filtros:**")
    mes = st.selectbox("Mês", ["Todos", "Janeiro", "Fevereiro", "Março"])
    categoria = st.multiselect("Categoria", ["Eletrônicos", "Roupas", "Casa", "Beleza"])

# Dados de exemplo com meses
@st.cache_data
def load_data():
    meses = ['Janeiro', 'Fevereiro', 'Março']
    categorias = ["Eletrônicos","Roupas","Casa","Beleza"]
    data = []

    for mes in meses:
        for dia in range(1, 11):  # 10 dias por mês
            for cat in categorias:
                vendas = 1000 + dia*50 + len(cat)*10
                pedidos = 40 + dia*3
                ticket = vendas / pedidos
                data.append({
                    'Dia': f'{dia:02d}/{mes[:3]}',
                    'Mês': mes,
                    'Categoria': cat,
                    'Vendas (R$)': vendas,
                    'Pedidos': pedidos,
                    'Ticket Médio (R$)': ticket
                })
    return pd.DataFrame(data)

df = load_data()

# Aplicar filtros de mês e categoria
if mes != "Todos":
    df = df[df['Mês'] == mes]
if categoria:
    df = df[df['Categoria'].isin(categoria)]

# Cabeçalho
st.markdown("<div class='main-header'>Dashboard de Vendas - Shein</div>", unsafe_allow_html=True)

# Métricas principais
vendas_totais = df['Vendas (R$)'].sum()
pedidos_totais = df['Pedidos'].sum()
ticket_medio = df['Ticket Médio (R$)'].mean()
crescimento = 12  # exemplo

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <div>Vendas Totais</div>
        <div style='font-size: 1.5rem; font-weight: bold;'>R$ {vendas_totais:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <div>Pedidos</div>
        <div style='font-size: 1.5rem; font-weight: bold;'>{pedidos_totais}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <div>Ticket Médio</div>
        <div style='font-size: 1.5rem; font-weight: bold;'>R$ {ticket_medio:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    cor_crescimento = "green" if crescimento >= 0 else "red"
    st.markdown(f"""
    <div class='metric-card'>
        <div>Crescimento</div>
        <div style='font-size: 1.5rem; font-weight: bold; color:{cor_crescimento};'>{crescimento:+}%</div>
    </div>
    """, unsafe_allow_html=True)

# Gráficos
col1, col2 = st.columns(2)

with col1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Dia'],
        y=df['Vendas (R$)'],
        mode='lines+markers',
        name='Vendas Diárias',
        line=dict(color='#EE4D2D', width=3),
        marker=dict(size=6)
    ))
    fig.update_layout(
        title='Vendas Diárias',
        xaxis_title='Dia',
        yaxis_title='Valor (R$)',
        height=350,
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=df['Dia'].unique()[:7],
        y=[df[df['Dia']==d]['Pedidos'].sum() for d in df['Dia'].unique()[:7]],
        name='Pedidos Recentes',
        marker_color='#FF6B6B'
    ))
    fig2.update_layout(
        title='Pedidos na Última Semana',
        xaxis_title='Dia',
        yaxis_title='Quantidade de Pedidos',
        height=350,
        template='plotly_white'
    )
    st.plotly_chart(fig2, use_container_width=True)

# Tabela de dados
st.markdown("### Dados Detalhados")
st.dataframe(df, use_container_width=True)

# Status do Mês
st.markdown("### Status do Mês")
col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"**Meta do Mês:** R$ 40.000")
with col2:
    st.success(f"**Atingido:** {vendas_totais/40000*100:.0f}%")
with col3:
    st.warning("**Dias Restantes:** 15")

# Resumo de desempenho
st.markdown("### 📈 Resumo Geral")
col1, col2, col3 = st.columns(3)
if not df.empty:
    col1.metric("Melhor Dia", df.loc[df['Vendas (R$)'].idxmax(), 'Dia'])
    col2.metric("Maior Venda", f"R$ {df['Vendas (R$)'].max():,.2f}")
    col3.metric("Menor Venda", f"R$ {df['Vendas (R$)'].min():,.2f}")
else:
    col1.metric("Melhor Dia", "-")
    col2.metric("Maior Venda", "-")
    col3.metric("Menor Venda", "-")
