import os
import requests
import logging
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"/tmp/{file.filename}"
    logging.info(f"Received upload request for file: {file.filename}")

    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)

    scan_result = scan_file(file_path)
    status = "clean" if scan_result else "infected"
    logging.info(f"Scan result for {file_path}: {status}")

    if scan_result:
        forward_file(file_path)
        logging.info(f"Forwarded file {file_path} to main service.")

    send_result(file_path, status)

    if not scan_result:
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.warning(f"Removed infected file: {file_path}")
        else:
            logging.error(f"File not found for removal: {file_path}")

    return JSONResponse(content={"message": "File processed"}, status_code=200)


def scan_file(file_path):
    try:
        with open(file_path, "rb") as file:
            content = file.read()

        suspicious_patterns = [
            b"virus",
            b"malware",
            b"trojan",
            b"exec(",
            b"system(",
            b"<script",
            b"eval(",
        ]

        for pattern in suspicious_patterns:
            if pattern in content.lower():
                return False  # Файл подозрительный

        return True  # Файл чистый
    except Exception as e:
        print(f"Error scanning file: {e}")
        return False


def forward_file(file_path):
    logging.info(f"Forwarding file: {file_path}")
    with open(file_path, "rb") as f:
        response = requests.post("http://nginx-main:88/api/upload", files={"file": f})
        if response.status_code == 201:
            logging.info(f"Successfully forwarded file: {file_path}")
        else:
            logging.error(
                f"Failed to forward file: {file_path}, status code: {response.status_code}"
            )


def send_result(file_path, status):
    filename = os.path.basename(file_path)
    logging.info(f"Sending scan result for {filename}: {status}")

    response = requests.post(
        "http://nginx-main:88/api/file_status",
        json={"filename": filename, "status": status},
    )
    if response.status_code in [200, 201]:
        logging.info(f"Successfully sent status for {filename}")
    else:
        logging.error(
            f"Failed to send status for {filename}, status code: {response.status_code}"
        )


if __name__ == "__main__":
    import uvicorn

    logging.info("Starting FastAPI server on port 8010...")
    uvicorn.run(app, host="0.0.0.0", port=8010)
