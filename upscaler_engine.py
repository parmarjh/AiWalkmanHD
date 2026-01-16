import numpy as np
import cv2
import os
import requests
from tqdm import tqdm

try:
    from moviepy.editor import VideoFileClip, AudioFileClip
except ImportError:
    from moviepy import VideoFileClip, AudioFileClip

class AiWalkmanEngine:
    def __init__(self, model_name="fsrcnn", scale=4, colorize=False):
        self.model_name = model_name.lower()
        self.scale = scale
        self.colorize = colorize
        self.sr = cv2.dnn_superres.DnnSuperResImpl_create()
        
        # Super Resolution setup
        self.model_path = f"{self.model_name}_x{self.scale}.pb"
        self._ensure_sr_model_exists()
        self.sr.readModel(self.model_path)
        self.sr.setModel(self.model_name, self.scale)

        # Colorization setup
        if self.colorize:
            self.prototxt = "colorization_deploy_v2.prototxt"
            self.model = "colorization_release_v2.caffemodel"
            self.points = "pts_in_hull.npy"
            self._ensure_color_models_exists()
            
            self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)
            pts = np.load(self.points)
            
            # Add the cluster centers as 1x1 convolutions to the model
            class8 = self.net.getLayerId("class8_ab")
            conv8 = self.net.getLayerId("conv8_313_rh")
            pts = pts.transpose().reshape(2, 313, 1, 1)
            self.net.getLayer(class8).blobs = [pts.astype("float32")]
            self.net.getLayer(conv8).blobs = [np.full((1, 313), 2.606, dtype="float32")]

    def _ensure_sr_model_exists(self):
        urls = {
            "fsrcnn_x4.pb": "https://github.com/Saafke/FSRCNN_Tensorflow/raw/master/models/FSRCNN_x4.pb",
            "fsrcnn_x2.pb": "https://github.com/Saafke/FSRCNN_Tensorflow/raw/master/models/FSRCNN_x2.pb",
            "edsr_x4.pb": "https://github.com/Saafke/EDSR_Tensorflow/raw/master/models/EDSR_x4.pb",
            "lapsrn_x4.pb": "https://github.com/fannymonori/TF-LapSRN/raw/master/export_models/LapSRN_x4.pb"
        }
        if not os.path.exists(self.model_path):
            self._download(urls.get(self.model_path), self.model_path)

    def _ensure_color_models_exists(self):
        links = {
            "colorization_deploy_v2.prototxt": "https://raw.githubusercontent.com/richzhang/colorization/master/colorization/models/colorization_deploy_v2.prototxt",
            "pts_in_hull.npy": "https://github.com/richzhang/colorization/raw/master/colorization/resources/pts_in_hull.npy",
            "colorization_release_v2.caffemodel": "https://github.com/richzhang/colorization/raw/master/colorization/models/colorization_release_v2.caffemodel"
        }
        for name, url in links.items():
            if not os.path.exists(name):
                print(f"Downloading Colorization model: {name}")
                self._download(url, name)

    def _download(self, url, path):
        r = requests.get(url, stream=True)
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    def process_frame(self, frame):
        """Colorizes and then upscales a single frame."""
        if self.colorize:
            # Colorization logic
            h, w = frame.shape[:2]
            scaled = frame.astype("float32") / 255.0
            lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
            
            resized = cv2.resize(lab, (224, 224))
            L = cv2.split(resized)[0]
            L -= 50
            
            self.net.setInput(cv2.dnn.blobFromImage(L))
            ab = self.net.forward()[0, :, :, :].transpose((1, 2, 0))
            ab = cv2.resize(ab, (w, h))
            
            L = cv2.split(lab)[0]
            colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
            colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
            colorized = np.clip(colorized, 0, 1)
            frame = (colorized * 255).astype("uint8")

        # Upscale logic
        return self.sr.upsample(frame)

    def upscale_video(self, input_path, output_path):
        cap = cv2.VideoCapture(input_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        new_width = width * self.scale
        new_height = height * self.scale
        
        temp_output = "temp_nosound.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_output, fourcc, fps, (new_width, new_height))
        
        pbar = tqdm(total=total_frames)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            processed = self.process_frame(frame)
            out.write(processed)
            pbar.update(1)
            
        pbar.close()
        cap.release()
        out.release()

        # Audio Merge
        try:
            video_clip = VideoFileClip(temp_output)
            original_clip = VideoFileClip(input_path)
            if original_clip.audio:
                final_clip = video_clip.with_audio(original_clip.audio)
                final_clip.write_videofile(output_path, codec="libx264")
            else:
                video_clip.write_videofile(output_path, codec="libx264")
            video_clip.close()
            original_clip.close()
            os.remove(temp_output)
        except Exception as e:
            print(f"Audio Merge Error: {e}")

    def stream_live(self, stream_url):
        cap = cv2.VideoCapture(stream_url)
        cv2.namedWindow("AiWalkmanHD - Live AI", cv2.WND_PROP_FULLSCREEN)
        while True:
            ret, frame = cap.read()
            if not ret: break
            
            processed = self.process_frame(frame)
            cv2.imshow("AiWalkmanHD - Live AI", processed)
            if cv2.waitKey(1) & 0xFF == ord('q'): break
        cap.release()
        cv2.destroyAllWindows()
