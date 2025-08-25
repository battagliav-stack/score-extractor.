import cv2, numpy as np
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import argparse, os

def extract_score(video_path, out_pdf):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(gray)
    cap.release()
    if not frames:
        raise ValueError("Aucune frame extraite")

    score_img = np.vstack(frames)
    pil_img = Image.fromarray(score_img)
    out_png = out_pdf.replace(".pdf", ".png")
    pil_img.save(out_png)

    a4_w, a4_h = A4
    c = canvas.Canvas(out_pdf, pagesize=A4)
    pil_w, pil_h = pil_img.size
    scale = min(a4_w/pil_w, a4_h/pil_h)
    c.drawImage(out_png, 0, a4_h - pil_h*scale, width=pil_w*scale, height=pil_h*scale)
    c.showPage()
    c.save()
    print("PDF et PNG générés :", out_pdf, out_png)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="Chemin de la vidéo")
    parser.add_argument("--out", required=True, help="Nom du PDF de sortie")
    args = parser.parse_args()
    extract_score(args.video, args.out)
