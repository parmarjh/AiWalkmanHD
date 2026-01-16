# 🎬 AiWalkmanHD
### *Breathe New Life into the Classics*


![RetroHD Banner](C:/Users/parma/.gemini/antigravity/brain/a32e62b2-6342-4ed8-b32a-9b97a21ae383/retro_hd_banner_1768539753996.png)

**AiWalkmanHD** is a premium AI-powered video reconstruction tool designed to transform low-resolution 90s, 60s, and 30s movies into modern High Definition (HD). Using state-of-the-art Deep Learning Super-Resolution models, AiWalkmanHD doesn't just stretch pixels—it **reconstructs** them.


---

## ✨ Key Features
- 🧠 **Deep Learning Models**: Multiple AI engines (FSRCNN, EDSR, LapSRN) for different types of movie restoration.
- 🎨 **AI Colorization**: Instantly transform vintage Black & White films into vibrant color using Neural Networks.
- 🚀 **4x Upscaling**: Convert standard 480p footage into extremely sharp 4K-like detail.
- 🎵 **Smart Audio Preservation**: Automatically extracts and merges original audio tracks back into the upscaled video.
- 🖥️ **Premium UI**: Built with a sleek, dark-mode Streamlit dashboard for effortless processing.
- 🎥 **Format Support**: Upload and process MP4, AVI, MOV, and MKV files.


---

## 🛠️ Performance & AI Models

| Model | Speed | Quality | Use Case |
| :--- | :--- | :--- | :--- |
| **FSRCNN** | ⚡ Fast | ⭐⭐⭐ | 90s VHS footage, casual home videos. |
| **EDSR** | 🐢 Slow | ⭐⭐⭐⭐⭐ | Cinema restoration, high-fidelity details. |
| **LapSRN** | ⚖️ Medium | ⭐⭐⭐⭐ | General purpose deep reconstruction. |

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.9+ installed and FFmpeg available for audio processing.

### 2. Installation
Install the required dependencies directly from your terminal:
```bash
pip install opencv-contrib-python moviepy streamlit tqdm requests fastapi uvicorn python-multipart
```

### 3. Run the Dashboard (Windows)
If you get an error saying `'streamlit' is not recognized`, use this command:
```powershell
python -m streamlit run app.py
```
*Note: Make sure you are inside the `ai_video_upscaler` folder.*

### 4. Run the API (For Developers)
To use the upscaler in other applications:
```powershell
python -m uvicorn api:app --host 0.0.0.0 --port 8000
```
API Documentation will be available at: `http://localhost:8000/docs`

---

## 📖 How to Use
1. **Launch**: Run the app using the `python -m` command above.
2. **Open Browser**: Go to `http://localhost:8501` in your web browser (Chrome/Edge). Do **not** type the URL in the terminal.
3. **Upload or Stream**: 
   - Use the **File Upscale** tab for 90s movies on your computer.
   - Use the **Live TV / HDMI** tab for online streams and IPTV.
4. **Configure**: 
   - Select your preferred AI model.
   - Check the **"Colorize B&W Movie"** box for vintage films.
5. **Process**: Click **"Start AI Upscaling"**.

6. **HDMI Output**: Drag the resulting Live window to your TV screen and press 'F'.


---

## 🛡️ Technology Stack
- **Engine**: OpenCV DNN (Deep Neural Networks) Super Resolution
- **Frontend**: Streamlit (Reactive Framework)
- **Multimedia**: MoviePy & FFmpeg
- **Algorithm**: Convolutional Neural Networks (CNN)

---

## 📜 License
This project is open-source. Please credit **AiWalkmanHD** when sharing upscaled footage.


---
*Created with ❤️ for Cinema Enthusiasts.*
