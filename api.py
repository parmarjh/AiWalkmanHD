from fastapi import FastAPI, UploadFile, File, BackgroundTasks
import os
import shutil
from upscaler_engine import AIVideoUpscaler
import uuid

app = FastAPI(title="AiWalkmanHD AI API")


# Directories
UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "RetroHD AI Video Upscaler API is Online"}

@app.post("/upscale/")
async def upscale_video_api(background_tasks: BackgroundTasks, file: UploadFile = File(...), model: str = "fsrcnn", scale: int = 4):
    """Upload a file and upscale it in the background."""
    job_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
    output_path = os.path.join(PROCESSED_DIR, f"upscaled_{job_id}_{file.filename}")

    # Save Upload
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run AI Task in Background
    background_tasks.add_task(run_upscale_job, input_path, output_path, model, scale)

    return {
        "status": "Processing Started",
        "job_id": job_id,
        "download_url": f"/download/{os.path.basename(output_path)}"
    }

@app.get("/stream-live/")
def stream_on_hdmi(channel_url: str, model: str = "fsrcnn"):
    """Command the server to open a live TV stream and upscale it to a local HDMI window."""
    try:
        upscaler = AIVideoUpscaler(model_name=model, scale=4)
        # We run this in the background usually, or just direct
        upscaler.stream_live(channel_url)
        return {"status": "Live stream window closed"}
    except Exception as e:
        return {"error": str(e)}

def run_upscale_job(input_path, output_path, model, scale):
    upscaler = AIVideoUpscaler(model_name=model, scale=scale)
    upscaler.upscale_video(input_path, output_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
