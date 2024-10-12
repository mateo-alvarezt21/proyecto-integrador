import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Configuración de la página
st.set_page_config(layout="wide")
st.subheader("Analizador de Datos de Google Sheets")
st.markdown("""
Este código lee datos de una hoja de cálculo de Google Sheets llamada "Sheet1", 
los procesa con Pandas y actualiza una segunda hoja llamada "Sheet2" con nuevos datos.
La interfaz de usuario de Streamlit permite al usuario ingresar el ID de la hoja de cálculo
y visualizar los datos procesados.
""")

# Definir los alcances de Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Rango de las hojas de cálculo
RANGE1 = "Sheet1!A:E"
RANGE2 = "Sheet2!A:E"

# Configuración de las credenciales
def get_google_sheet_service():
    try:
        google_sheet_credentials = st.secrets["GOOGLE_SHEET_CREDENTIALS"]  
        secrets_dict = google_sheet_credentials.to_dict()
        creds = service_account.Credentials.from_service_account_info(secrets_dict, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        return service.spreadsheets()
    except Exception as e:
        st.error(f"Error al configurar el servicio de Google Sheets: {e}")
        return None

# Leer datos de la hoja de cálculo
def read_sheet(sheet, spreadsheet_id):
    try:
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=RANGE1).execute()      
        values = result.get('values', [])
        if not values or len(values) < 2:
            st.warning("La hoja de cálculo está vacía o no contiene suficientes datos.")
            return pd.DataFrame()  # DataFrame vacío para evitar errores posteriores

        # Crear el DataFrame usando la primera fila como encabezado
        df = pd.DataFrame(values[1:], columns=values[0])
        return df
    except Exception as e:
        st.error(f"Error al leer la hoja de cálculo: {e}")
        return pd.DataFrame()

# Actualizar datos en la hoja de cálculo
def update_sheet(sheet, spreadsheet_id, df):
    try:
        body = {'values': df.values.tolist()}
        result = sheet.values().update(
            spreadsheetId=spreadsheet_id, range=RANGE2,
            valueInputOption="USER_ENTERED", body=body).execute()
        return result
    except Exception as e:
        st.error(f"Error al actualizar la hoja de cálculo: {e}")
        return None

# Main
def main():
    # Ingreso del ID de la hoja de cálculo
    spreadsheet_id = st.text_input("ID de la hoja de cálculo")

    # Verificar si se ha proporcionado el ID
    if not spreadsheet_id:
        st.info("Por favor, ingresa el ID de la hoja de cálculo.")
        return

    # Obtener el servicio de Google Sheets
    sheet = get_google_sheet_service()
    if not sheet:
        return

    # Botón para leer los datos
    if st.button("Analizar datos de Google Sheet"):
        # Leer datos de "Sheet1"
        df = read_sheet(sheet, spreadsheet_id)
        if df.empty:
            return  # Si el DataFrame está vacío, no continuar

        st.header("Datos de la Hoja 1")
        st.dataframe(df)

        # Realizar una operación (por ejemplo, suma de una columna específica)
        if 'Columna2' in df.columns:
            df['Columna2'] = pd.to_numeric(df['Columna2'], errors='coerce')  # Convertir a numérico
            suma = df['Columna2'].sum()  # Sumar la columna
            st.write(f"Suma de la columna 'Columna2': {suma}")

            # Crear un DataFrame para actualizar "Sheet2" con el resultado de la operación
            df_update = pd.DataFrame({
                'Resultado': ['Suma de Columna2'],
                'Valor': [suma]
            })

            # Actualizar "Sheet2" con el resultado
            result = update_sheet(sheet, spreadsheet_id, df_update)
            if result:
                st.header("Datos de la Hoja 2")
                st.success(f"Hoja actualizada. {result.get('updatedCells')} celdas actualizadas.")
                st.dataframe(df_update)
        else:
            st.error("La columna 'Columna2' no existe en la hoja de cálculo.")

# Ejecutar la función principal
if __name__ == "__main__":
    main()
