import streamlit as st
import subprocess, os, tempfile

st.title("🎷 Extracteur de Partition depuis une Vidéo")

uploaded_file = st.file_uploader("Choisissez une vidéo", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded_file.read())
        video_path = tmp.name

    out_pdf = os.path.join(tempfile.gettempdir(), "partition.pdf")

    try:
        st.info("⏳ Extraction en cours... (cela peut prendre un moment)")
        result = subprocess.run(
            ["python", "score_extractor.py", "--video", video_path, "--out", out_pdf, "--skip", "90"],
            capture_output=True, text=True
        )

        if result.returncode == 0 and os.path.exists(out_pdf):
            st.success("✅ Partition générée ! Téléchargez-la ci-dessous :")
            with open(out_pdf, "rb") as f:
                st.download_button("📥 Télécharger le PDF", f, file_name="partition.pdf")
        else:
            st.error("❌ Erreur lors de l'extraction :\n" + result.stderr)

    except Exception as e:
        st.error(f"⚠️ Une erreur est survenue : {e}")
