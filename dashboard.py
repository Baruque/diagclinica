import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(layout="wide")

# --- SIMULAÇÃO DE DADOS ---
def gerar_dados_clinicos():
    # Cria datas para as últimas 24 horas
    datas = [datetime.now() - timedelta(hours=i) for i in range(24)]
    datas.reverse()
    # Gera valores aleatórios para simular sinais vitais
    freq_card = np.random.randint(60, 110, size=24)
    return pd.DataFrame({"Data/Hora": datas, "FC (bpm)": freq_card})

df = gerar_dados_clinicos()

# --- INTERFACE STREAMLIT ---
st.title("📊 Monitorização de Sinais Vitais")

# Métricas de resumo no topo
col1, col2, col3 = st.columns(3)
ultimo_valor = df["FC (bpm)"].iloc[-1]
delta = int(ultimo_valor - df["FC (bpm)"].iloc[-2])

col1.metric("Última FC", f"{ultimo_valor} bpm", delta=delta, delta_color="inverse")
col2.metric("Média (24h)", f"{int(df['FC (bpm)'].mean())} bpm")
col3.metric("Status", "Alerta" if ultimo_valor > 100 else "Estável")

# --- GRÁFICO INTERATIVO COM PLOTLY ---
fig = go.Figure()

# Linha de dados do paciente
fig.add_trace(go.Scatter(
    x=df["Data/Hora"], 
    y=df["FC (bpm)"],
    mode='lines+markers',
    name='Frequência Cardíaca',
    line=dict(color='#1f77b4', width=3),
    marker=dict(size=8)
))

# Zonas de Alerta (Faixas Horizontais)
fig.add_hrect(y0=60, y1=100, fillcolor="green", opacity=0.1, line_width=0, annotation_text="Zona Normal")
fig.add_hrect(y0=100, y1=120, fillcolor="red", opacity=0.1, line_width=0, annotation_text="Taquicardia")

fig.update_layout(
    title="Evolução da Frequência Cardíaca (Últimas 24h)",
    xaxis_title="Tempo",
    yaxis_title="Batimentos por Minuto (bpm)",
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Tabela detalhada opcional
with st.expander("Ver registos detalhados"):
    st.dataframe(df.sort_values(by="Data/Hora", ascending=False), use_container_width=True)

