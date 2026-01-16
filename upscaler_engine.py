import cv2
import os
import requests
from tqdm import tqdm
try:
    from moviepy.editor import VideoFileClip, AudioFileClip
except ImportError:
    from moviepy import VideoFileClip, AudioFileClip


class AIVideoUpscaler:
    def __init__(self, model_name="fsrcnn", scale=4):
        self.model_name = model_name.lower()
        self.scale = scale
        self.model_path = f"{self.model_name}_x{self.scale}.pb"
        self.sr = cv2.dnn_superres.DnnSuperResImpl_create()
        
        self._ensure_model_exists()
        self.sr.readModel(self.model_path)
        self.sr.setModel(self.model_name, self.scale)

    def _ensure_model_exists(self):
        # Links to pre-trained OpenCV SuperRes models
        urls = {
            "fsrcnn_x4.pb": "https://github.com/Saafke/FSRCNN_Tensorflow/raw/master/models/FSRCNN_x4.pb",
            "edsr_x4.pb": "https://github.com/Saafke/EDSR_Tensorflow/raw/master/models/EDSR_x4.pb",
            "lapsrn_x4.pb": "https://github.com/fannymonori/TF-LapSRN/raw/master/export_models/LapSRN_x4.pb"
        }
        
        if not os.path.exists(self.model_path):
            print(f"Downloading AI Model: {self.model_path}...")
            url = urls.get(self.model_path)
            if not url:
                raise ValueError(f"Model {self.model_path} not found in library.")
            
            r = requests.get(url, stream=True)
            with open(self.model_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Download Complete.")

    def upscale_video(self, input_path, output_path):
        cap = cv2.VideoCapture(input_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        new_width = width * self.scale
        new_height = height * self.scale
        
        # Temporary video only (no audio)
        temp_output = "temp_nosound.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_output, fourcc, fps, (new_width, new_height))

        print(f"Upscaling {total_frames} frames to {new_width}x{new_height}...")
        
        pbar = tqdm(total=total_frames)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # AI Upscale the frame
            upscaled_frame = self.sr.upsample(frame)
            out.write(upscaled_frame)
            pbar.update(1)
            
        pbar.close()
        cap.release()
        out.release()

        # Merge Audio back using MoviePy
        print("Merging Audio...")
        try:
            video_clip = VideoFileClip(temp_output)
            original_clip = VideoFileClip(input_path)
            
            if original_clip.audio:
                final_clip = video_clip.set_audio(original_clip.audio)
                final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
            else:
                video_clip.write_videofile(output_path, codec="libx264")
            
            video_clip.close()
            original_clip.close()
            os.remove(temp_output)
            print(f"Success! Saved to {output_path}")
        except Exception as e:
            print(f"Audio merging failed, but video is saved as {temp_output}. Error: {e}")

    def stream_live(self, stream_url):
        """Processes a live TV/IPTV stream and displays it in a window for HDMI output."""
        cap = cv2.VideoCapture(stream_url)
        if not cap.isOpened():
            raise ValueError("Could not open stream URL.")

        print(f"Starting Live AI Stream: {stream_url}")
        print("Press 'q' to stop the AI HDMI output.")
        
        cv2.namedWindow("AiWalkmanHD - Live AI Upscale", cv2.WND_PROP_FULLSCREEN)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # AI Upscale the frame
            upscaled_frame = self.sr.upsample(frame)
            
            # Show on screen (User can drag this to HDMI Monitor)
            cv2.imshow("AiWalkmanHD - Live AI Upscale", upscaled_frame)

            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # Example usage
    # upscaler = AIVideoUpscaler(model_name="fsrcnn", scale=4)
    # upscaler.upscale_video("old_movie.mp4", "hd_movie.mp4")
    pass
