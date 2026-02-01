import streamlit as st
import pandas as pd
from fpdf import FPDF

# Configuração da página (deve ser a primeira linha)
st.set_page_config(page_title="Protocolos Clínicos", page_icon="🏥")
# Função para gerar PDF
def gerar_pdf(nome, idade, pas, pad, status, recomendacao):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", fname="DejaVuSans.ttf") 
    pdf.set_font("DejaVu", size=12)
    #pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Relatório de Avaliação Clínica", ln=True, align='C')
    
    pdf.set_font("DejaVu", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Paciente: {nome}", ln=True)
    pdf.cell(200, 10, txt=f"Idade: {idade} anos", ln=True)
    pdf.cell(200, 10, txt=f"Pressão Arterial: {pas}/{pad} mmHg", ln=True)
    pdf.cell(200, 10, txt=f"Classificação: {status}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt=f"Conduta: {recomendacao}")
    
     # IMPORTANTE: Use 'dest="S"' para retornar os bytes da string/buffer

    return bytes(pdf.output())

# Estilização básica e Título
st.title("🏥 Gestão de Protocolos Clínicos")
st.sidebar.header("Dados do Paciente")

# 1. Entrada de Dados na Barra Lateral (Sidebar)
nome = st.sidebar.text_input("Nome Completo", placeholder="Ex: João Silva")
idade = st.sidebar.number_input("Idade", min_value=0, max_value=120, value=30)
pas = st.sidebar.number_input("Pressão Sistólica (PAS)", value=120, help="Valor superior")
pad = st.sidebar.number_input("Pressão Diastólica (PAD)", value=80, help="Valor inferior")


# 2. Lógica do Protocolo (O "Cérebro")
def classificar_pressao(pas, pad):
    if pas >= 180 or pad >= 120:
        return "Crise Hipertensiva", "🔴 Emergência: Encaminhamento imediato.", "error"
    if pas >= 140 or pad >= 90:
        return "Hipertensão", "🟡 Iniciar Protocolo de Tratamento.", "warning"
    if 130 <= pas <= 139 or 85 <= pad <= 89:
        return "Pré-hipertensão", "🟠 Mudança de Estilo de Vida (MEV).", "info"
    return "Normal", "🟢 Manter monitoramento.", "success"


# 3. Execução e Exibição do Resultado
if st.sidebar.button("Avaliar Protocolo"):
    if not nome:
        st.sidebar.warning("Por favor, insira o nome do paciente.")
    else:
        status, recomendacao, tipo_alerta = classificar_pressao(pas, pad)
    
        st.subheader(f"Avaliação: {nome}")
        
                # Alerta visual
        if tipo_alerta == "error": st.error(recomendacao)
        elif tipo_alerta == "warning": st.warning(recomendacao)
        elif tipo_alerta == "info": st.info(recomendacao)
        else: st.success(recomendacao)

        # Métricas
        col1, col2, col3 = st.columns(3)
        col1.metric("Pressão Sistólica", f"{pas} mmHg")
        col2.metric("Pressão Diastólica", f"{pad} mmHg")
        col3.metric("Status", status)

        # Botão para gerar "relatório" (simulado)
        #st.download_button("Exportar PDF do Atendimento", "Dados do protocolo...", file_name="atendimento.txt")
        dados_paciente = {
            "Paciente": [nome],
            "Idade": [idade],
            "PAS": [pas],
            "PAD": [pad],
            "Status": [status]
        }
        df = pd.DataFrame(dados_paciente)
        st.table(df) # Exibe uma tabela limpa


    # --- Exemplo de Uso na Interface ---

    # Geração automática dos bytes do PDF
    pdf_bytes = gerar_pdf(nome,idade, pas, pad, status, recomendacao)

    # Botão de Download
    st.download_button(
        label="📥 Descarregar Relatório PDF",
        data=pdf_bytes,
        file_name=f"relatorio_{nome}.pdf",
        mime="application/pdf"
    )
else:
    st.info("Aguardando entrada de dados na barra lateral para gerar o diagnóstico.")
