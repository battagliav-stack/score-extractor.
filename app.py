import streamlit as st
import os, tempfile, subprocess

st.set_page_config(page_title="Score Extractor", layout="wide")
st.title("🎼 Score Extractor - Simple Version")

st.markdown("Déposez une vidéo et récupérez directement la partition PDF + PNG")

uploaded_video = st.file_uploader("Vidéo (mp4, mov, avi...)", type=["mp4","mov","avi","mkv"])

if uploaded_video:
    tmp_dir = tempfile.mkdtemp()
    input_path = os.path.join(tmp_dir, uploaded_video.name)
    with open(input_path, "wb") as f:
        f.write(uploaded_video.read())

    out_pdf = os.path.join(tmp_dir, "partition.pdf")
    out_png = os.path.join(tmp_dir, "partition.png")

    cmd = ["python", "score_extractor.py", "--video", input_path, "--out", out_pdf]

    if st.button("Extraire la partition"):
        with st.spinner("Extraction en cours..."):
            try:
                subprocess.run(cmd, check=True)
                st.success("Extraction terminée !")
                with open(out_pdf, "rb") as f_pdf:
                    st.download_button("📥 Télécharger le PDF", f_pdf, file_name="partition.pdf")
                with open(out_png, "rb") as f_png:
                    st.download_button("📥 Télécharger le PNG", f_png, file_name="partition.png")
                st.image(out_png, caption="Aperçu de la partition", use_column_width=True)
            except subprocess.CalledProcessError as e:
                st.error("Erreur lors du traitement de la vidéo.")
                st.text(str(e))
else:
    st.info("Importez une vidéo pour commencer.")
