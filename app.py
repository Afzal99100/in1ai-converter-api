from fastapi import FastAPI, UploadFile, File
import subprocess, uuid, os

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API Running"}

@app.post("/word-to-pdf")
async def word_to_pdf(file: UploadFile = File(...)):
    uid = str(uuid.uuid4())
    input_path = f"/tmp/{uid}_{file.filename}"
    output_dir = "/tmp"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_dir,
        input_path
    ])

    pdf_file = input_path.replace(".docx", ".pdf")

    return {
        "download": f"/download/{os.path.basename(pdf_file)}"
    }

@app.get("/download/{filename}")
def download_file(filename: str):
    return FileResponse(f"/tmp/{filename}")
