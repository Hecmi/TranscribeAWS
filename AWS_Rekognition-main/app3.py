import streamlit as st
import requests
import base64

# URL de tu endpoint de Lambda vía API Gateway
API_URL = "https://dxtibjua57.execute-api.us-east-1.amazonaws.com/default/fnTranscribeAudioText"

st.set_page_config(page_title="Texto ⇆ Audio", layout="wide")
st.title("Conversor de Texto ⇄ Audio usando AWS")

col1, col2 = st.columns(2)

# --- Columna 1: Subir audio para transcripción ---
with col1:
    st.header("🎤 Subir Audio (MP3)")
    audio_file = st.file_uploader("Sube un archivo .mp3", type=["mp3", "m4a", "aac"], key="audio")

    if audio_file and st.button("Transcribir Audio"):
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

        payload = {
            "audio_base64": audio_base64
        }

        with st.spinner("Transcribiendo audio..."):
            response = requests.post(API_URL, json=payload)
            print(response.json())
            if response.status_code == 200:
                result = response.json()
                st.success("✅ Transcripción completada:")
                st.text_area("Texto transcrito", result.get("text"), height=200)
            else:
                st.error(f"❌ Error: {response.json().get('error', 'Desconocido')}")

with col2:
    st.header("✍️ Ingresar Texto")
    input_text = st.text_area("Escribe el texto que deseas convertir a audio", height=200)

    generar_audio = st.button("Generar Audio")

    if generar_audio:
        if not input_text.strip():
            st.warning("⚠️ Por favor, ingresa texto antes de generar el audio.")
        else:
            payload = {"text": input_text}
            with st.spinner("Generando audio..."):
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    audio_base64 = result.get("audio_base64")
                    audio_bytes = base64.b64decode(audio_base64)
                    st.success("✅ Audio generado:")
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button("Descargar Audio", audio_bytes, file_name="voz.mp3")
                else:
                    st.error(f"❌ Error: {response.json().get('error', 'Desconocido')}")
