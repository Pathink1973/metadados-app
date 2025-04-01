import streamlit as st
from PIL import Image
import piexif
import io

st.set_page_config(page_title="Analisador de Metadados", layout="wide")

st.title("📷 Analisador de Metadados de Fotografias")

uploaded_file = st.file_uploader("Arraste ou selecione uma imagem da sua câmara", type=["jpg", "jpeg", "tiff"])

def extract_exif_data(image_file):
    metadata = {}
    try:
        img = Image.open(image_file)
        exif_data = img.info.get("exif")
        if not exif_data:
            return {}
        exif_dict = piexif.load(exif_data)

        for ifd_name in exif_dict:
            for tag in exif_dict[ifd_name]:
                try:
                    tag_name = piexif.TAGS[ifd_name][tag]["name"]
                    value = exif_dict[ifd_name][tag]
                    if isinstance(value, bytes):
                        value = value.decode(errors="ignore")
                    metadata[tag_name] = str(value)
                except:
                    continue
    except Exception as e:
        st.error(f"Erro ao ler os metadados: {e}")
    return metadata

def export_txt(metadata_dict):
    output = io.StringIO()
    for k, v in metadata_dict.items():
        output.write(f"{k}: {v}\n")
    return output.getvalue().encode("utf-8")

if uploaded_file:
    st.image(uploaded_file, caption="Imagem carregada", use_container_width=True)
    st.subheader("📋 Metadados da imagem:")

    metadata = extract_exif_data(uploaded_file)

    if metadata:
        st.dataframe(metadata.items(), use_container_width=True)

        txt_data = export_txt(metadata)

        st.download_button(
            label="📥 Exportar metadados em TXT",
            data=txt_data,
            file_name="metadados.txt",
            mime="text/plain"
        )
    else:
        st.info("⚠️ Esta imagem não possui metadados EXIF. Tente outra tirada diretamente com uma câmara fotográfica.")
