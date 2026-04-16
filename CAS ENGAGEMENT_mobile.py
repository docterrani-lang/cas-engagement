import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import os

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Terrani Imaging CRM",
    page_icon="💼",
    layout="centered"
)

# --- STILE CSS PERSONALIZZATO ---
st.markdown("""
    <style>
    .stApp { background-color: #101010; }
    label { color: white !important; font-weight: bold !important; font-size: 1.1rem !important; }
    .stMarkdown p { color: white !important; }
    .stButton>button { 
        background-color: #1f538d !important; 
        color: white !important; 
        border: 2px solid #1f538d !important;
        border-radius: 12px; 
        height: 3.5em; 
        width: 100%;
        font-weight: bold !important;
        font-size: 18px !important;
        margin-top: 20px;
    }
    .stButton>button:hover { background-color: #2a71c2 !important; border-color: #2a71c2 !important; color: white !important; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 8px !important;
    }
    h1, h3 { color: #1f538d !important; font-weight: bold !important; }
    .stCheckbox { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER CON LOGO ---
col_titles, col_logo = st.columns([2, 1])
with col_titles:
    st.title("CUSTOMER ENGAGEMENT")
    st.write("Terrani Imaging Solutions - Mobile CRM")

with col_logo:
    logo_fn = "LOGO TERRANI IMAGING SOLUTIONS.png"
    if os.path.exists(logo_fn):
        st.image(logo_fn, use_container_width=True)
    else:
        st.write("Logo non trovato")

st.divider()

# --- FORM DI INSERIMENTO ---
with st.form("engagement_form", clear_on_submit=True):
    # Riga 1: Nome e Cognome
    c1, c2 = st.columns(2)
    with c1:
        nome = st.text_input("NOME")
    with c2:
        cognome = st.text_input("COGNOME")
    
    # Riga 2: Telefono e Email
    c3, c4 = st.columns(2)
    with c3:
        tel = st.text_input("NUMERO DI TELEFONO")
    with c4:
        email = st.text_input("E-MAIL")
    
    # Campo Drop-Down Referente
    referente = st.selectbox(
        "REFERENTE",
        options=["TERRANI", "CENTOLA", "SANGUINETTI", "COLOMBO", "CATELLO"]
    )
    
    cas_engagement = st.text_area(
        "CAS ENGAGEMENT", 
        height=250, 
        placeholder="Inserisci qui i dettagli dell'incontro..."
    )
    
    submit = st.form_submit_button("SALVA ANAGRAFICA CLIENTE")

# --- LOGICA DI SALVATAGGIO ---
db_path = "database_clienti_web.csv"

if submit:
    if nome and cognome:
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Preparazione dati per CSV
        new_data = {
            "Data": [timestamp],
            "Nome": [nome],
            "Cognome": [cognome],
            "Telefono": [tel],
            "Email": [email],
            "Referente": [referente],
            "Engagement": [cas_engagement.replace("\n", " ")]
        }
        df = pd.DataFrame(new_data)
        
        # Salvataggio su file CSV
        if not os.path.isfile(db_path):
            df.to_csv(db_path, index=False)
        else:
            df.to_csv(db_path, mode='a', header=False, index=False)
            
        st.success(f"✅ Dati di {nome} {cognome} salvati con successo!")
        
        # --- GENERAZIONE PDF ---
        pdf = FPDF()
        pdf.add_page()
        
        if os.path.exists(logo_fn):
            pdf.image(logo_fn, 150, 10, 40)
            
        pdf.set_font("Arial", "B", 16)
        pdf.set_text_color(31, 83, 141)
        pdf.cell(0, 15, "SCHEDA CUSTOMER ENGAGEMENT", ln=True)
        
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, f"Data report: {timestamp}", ln=True)
        pdf.ln(10)
        
        # Sezione Anagrafica e Referente
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(0, 10, " DATI CLIENTE E REFERENTE", 1, 1, "L", True)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 10, f"Nominativo: {nome} {cognome}", 1, 1)
        pdf.cell(0, 10, f"Tel: {tel} | Email: {email}", 1, 1)
        pdf.cell(0, 10, f"Referente Terrani Imaging: {referente}", 1, 1)
        
        # Sezione Note
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, " DETTAGLI ENGAGEMENT", 1, 1, "L", True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 10, cas_engagement)
        
        pdf_name = f"Engagement_{cognome}.pdf"
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        
        st.download_button(
            label="📥 SCARICA SCHEDA PDF",
            data=pdf_bytes,
            file_name=pdf_name,
            mime="application/pdf"
        )
    else:
        st.error("⚠️ Errore: Nome e Cognome sono campi obbligatori.")

# --- VISUALIZZAZIONE STORICO ---
st.divider()
show_db = st.checkbox("Visualizza Storico Database")
if show_db:
    if os.path.exists(db_path):
        history_df = pd.read_csv(db_path)
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("Il database è attualmente vuoto.")
