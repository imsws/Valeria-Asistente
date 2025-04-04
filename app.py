import streamlit as st
import os
import csv
import datetime
import pytz

# Carpeta donde se guardarán los registros
data_folder = "registros"
os.makedirs(data_folder, exist_ok=True)
archivo = os.path.join(data_folder, "comidas.csv")

# Registro por texto
def registrar_comida_texto(comida):
    zona_horaria = pytz.timezone("America/Santo_Domingo")
    hora_actual = datetime.datetime.now(zona_horaria).strftime("%H:%M:%S")
    fecha_actual = datetime.datetime.now(zona_horaria).strftime("%Y-%m-%d")

    with open(archivo, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([fecha_actual, hora_actual, comida])

    return f"Comida registrada: {comida} a las {hora_actual}"

# Visualización de historial
def ver_historial():
    if not os.path.exists(archivo):
        return "No hay registros aún."
    
    historial = ""
    with open(archivo, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:
                historial += f"{row[0]} - {row[1]}: {row[2]}\n"
    return historial if historial else "No hay registros aún."

# Interfaz con Streamlit
st.set_page_config(page_title="Valeria Asistente de Nutrición", layout="centered")

tabs = st.tabs(["Registrar comida", "Ver historial"])

with tabs[0]:
    st.title("Valeria Asistente de Nutrición")
    st.write("Dime qué comiste y registraré la hora automáticamente.")
    comida = st.text_input("comida", placeholder="Ejemplo: arroz con pollo")
    if st.button("Registrar"):
        resultado = registrar_comida_texto(comida)
        st.success(resultado)

with tabs[1]:
    st.header("Historial de comidas")
    historial = ver_historial()
    st.text_area("Historial", value=historial, height=300)
