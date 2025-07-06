import streamlit as st
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Certificados Unimar", layout="centered")

st.title("🎓 Generador de Certificados - Unimar")

# Formulario de entrada
with st.form("cert_form"):
    nombre = st.text_input("Nombre completo del participante")
    curso = st.text_input("Nombre del curso")
    fecha = st.date_input("Fecha de finalización")
    submit = st.form_submit_button("Guardar en Google Sheets")

if submit:
    if nombre and curso:
        try:
            # Autenticación con Google Sheets
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds_dict = st.secrets["google_sheets"]
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            client = gspread.authorize(creds)

            # Abrir hoja y agregar datos
            sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1RsNWb6CwsKd6xt-NffyUDmVgDOgqSo_wgR863Mxje30/edit#gid=1441343050")
            worksheet = sheet.worksheet("TCertificados")
            worksheet.append_row([nombre, curso, fecha.strftime("%Y-%m-%d"), str(datetime.now())])

            st.success("✅ Certificado guardado correctamente.")
        except Exception as e:
            st.error(f"❌ Error al guardar en Google Sheets: {e}")
    else:
        st.warning("Por favor completa todos los campos.")