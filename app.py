
import streamlit as st
import os
import csv
import datetime
import pytz
import speech_recognition as sr

data_folder = "registros"
os.makedirs(data_folder, exist_ok=True)
archivo = os.path.join(data_folder, "comidas.csv")

def registrar_comida(comida):
    zona_horaria = pytz.timezone("America/Santo_Domingo")
    hora_actual = datetime.datetime.now(zona_horaria).strftime("%H:%M:%S")
    fecha_actual = datetime.datetime.now(zona_horaria).strftime("%Y-%m-%d")
    with open(archivo, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([fecha_actual, hora_actual, comida])

def obtener_historial():
    if not os.path.exists(archivo):
        return []
    with open(archivo, mode="r") as file:
        reader = csv.reader(file)
        return list(reader)

def escuchar_comida():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Escuchando... habla ahora.")
        audio = r.listen(source)
    try:
        texto = r.recognize_google(audio, language="es-ES")
        st.success(f"Capturado: {texto}")
        return texto
    except sr.UnknownValueError:
        st.error("No se entendió lo que dijiste.")
    except sr.RequestError:
        st.error("Error de conexión con el servicio de voz.")
    return None

st.set_page_config(page_title="Valeria Asistente de Nutrición", layout="centered")

menu = st.sidebar.selectbox("Opciones", ["Registrar comida", "Ver historial"])
st.title("Valeria Asistente de Nutrición")

if menu == "Registrar comida":
    st.write("Dime qué comiste y registraré la hora automáticamente.")
    
    usar_microfono = st.checkbox("Usar micrófono")
    comida = ""

    if usar_microfono:
        if st.button("Hablar"):
            comida = escuchar_comida()
    else:
        comida = st.text_input("Comida", placeholder="Ejemplo: arroz con pollo")

    if st.button("Registrar") and comida:
        registrar_comida(comida)
        st.success("¡Comida registrada correctamente!")

elif menu == "Ver historial":
    st.subheader("Historial de comidas")
    historial = obtener_historial()
    if historial:
        for fila in historial[::-1]:
            st.write(f"{fila[0]} - {fila[1]}: {fila[2]}")
    else:
        st.info("Aún no has registrado comidas.")
