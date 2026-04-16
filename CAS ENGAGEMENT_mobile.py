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

# Stile CSS personalizzato per mantenere il look Dark/Blue
st.markdown("""
    <style>
    .stApp { background-color: #101010; color: white; }
    .stButton>button { 
        background-color: #1f538d; 
        color: white; 
        border-radius: 10px; 
        height: 3em; 
        width: 100%;
        font-weight: bold;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER CON LOGO ---
col1, col2 = st.columns([2, 1])

with col1:
    st.title("CUSTOMER ENGAGEMENT")
    st.write("Terrani Imaging Solutions - Mobile CRM")

with col2:
    # Nota: su Web App il percorso deve essere relativo o un URL. 
    # Se lo testi in locale sul tuo PC, questo percorso funzionerà:
    logo_path = r"D:\PHILIPS\CT\WIP\SIMONLAB\LOGO TERRANI IMAGING SOLUTIONS.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=200)

st.divider()

# --- FORM DI INSERIMENTO ---
with st.form("engagement_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        nome = st.text_input("NOME")
        email = st.text_input("E-MAIL")
    with c2:
        cognome = st.text_input("COGNOME")
        tel = st.text_input("TELEFONO")
    
    cas_engagement = st.text_area("CAS ENGAGEMENT", height=250, 
                                  placeholder="Inserisci qui i dettagli dell'incontro (min 500 caratteri)...")
    
    submit = st.form_submit_button("SALVA ANAGRAFICA")

# --- LOGICA DI SALVATAGGIO ---
if submit:
    if nome and cognome:
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Salvataggio dati (usiamo un file CSV per comodità web)
        new_data = {
            "Data": [timestamp],
            "Nome": [nome],
            "Cognome": [cognome],
            "Email": [email],
            "Telefono": [tel],
            "Engagement": [cas_engagement]
        }
        df = pd.DataFrame(new_data)
        
        # Salvataggio locale
        db_path = "database_clienti_web.csv"
        if not os.path.isfile(db_path):
            df.to_csv(db_path, index=False)
        else:
            df.to_csv(db_path, mode='a', header=False, index=False)
            
        st.success(f"Dati di {nome} {cognome} salvati con successo!")
        
        # Generazione PDF istantanea per il cellulare
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "TERRANI IMAGING SOLUTIONS", ln=True, align='C')
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Report Engagement - {timestamp}", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(0, 10, f"Cliente: {nome} {cognome}", ln=True)
        pdf.cell(0, 10, f"Contatti: {email} | {tel}", ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Dettagli CAS Engagement:", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 10, cas_engagement)
        
        pdf_name = f"Engagement_{cognome}.pdf"
        pdf.output(pdf_name)
        
        # Tasto per scaricare il PDF direttamente sul telefono
        with open(pdf_name, "rb") as f:
            st.download_button(
                label="📥 SCARICA REPORT PDF SUL TELEFONO",
                data=f,
                file_name=pdf_name,
                mime="application/pdf"
            )
    else:
        st.error("Nome e Cognome sono obbligatori!")

# --- VISUALIZZAZIONE DATABASE ---
if st.checkbox("Visualizza Storico Clienti"):
    if os.path.exists("database_clienti_web.csv"):
        history_df = pd.read_csv("database_clienti_web.csv")
        st.dataframe(history_df)
    else:
        st.write("Nessun dato presente.")