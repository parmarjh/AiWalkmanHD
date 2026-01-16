import streamlit as st
import os
from upscaler_engine import AiWalkmanEngine

import time

# Page Config
st.set_page_config(
    page_title="AiWalkmanHD | AI Movie Upscaler",
    page_icon="🎬",
    layout="wide"
)


# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background: linear-gradient(45deg, #FF4B2B, #FF416C);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(255, 75, 43, 0.3);
    }
    .header-text {
        font-family: 'Outfit', sans-serif;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0;
    }
    .sub-text {
        color: #888;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .card {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)


def main():
    st.markdown('<h1 class="header-text">AiWalkmanHD</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-text">Transform 90s & 60s Classics into Modern Masterpieces</p>', unsafe_allow_html=True)


    tab1, tab2 = st.tabs(["📂 File Upscale", "📺 Live TV / HDMI"])

    with tab1:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📁 Upload Your Movie")
            uploaded_file = st.file_uploader("Choose a video file...", type=["mp4", "avi", "mov", "mkv"])
            
            st.subheader("⚙️ Settings")
            model_choice = st.selectbox(
                "Choose AI Model",
                ["FSRCNN (Fast & Sharp)", "EDSR (Ultra Quality - Slow)", "LapSRN (Deep Reconstruction)"],
                index=0,
                key="file_model"
            )
            
            scale_factor = st.slider("Upscale Factor", 2, 4, 4, key="file_scale")
            do_colorize = st.checkbox("Colorize B&W Movie", value=False, key="file_color")
            st.markdown('</div>', unsafe_allow_html=True)


        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🚀 Processing")
            
            if uploaded_file is not None:
                input_path = os.path.join("uploads", uploaded_file.name)
                os.makedirs("uploads", exist_ok=True)
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.video(input_path)
                if st.button("Start AI Upscaling", key="btn_file"):
                    model_name = model_choice.split(" ")[0].lower()
                    output_name = f"upscaled_{scale_factor}x_{uploaded_file.name}"
                    output_path = os.path.join("processed", output_name)
                    os.makedirs("processed", exist_ok=True)

                    with st.spinner(f"AI is reconstructing and colorizing frames..."):
                        try:
                            upscaler = AiWalkmanEngine(model_name=model_name, scale=scale_factor, colorize=do_colorize)
                            upscaler.upscale_video(input_path, output_path)
                            st.balloons()

                            st.success("Transformation Complete!")
                            with open(output_path, "rb") as file:
                                st.download_button(label="⬇️ Download", data=file, file_name=output_name)
                        except Exception as e:
                            st.error(f"Error: {e}")
            else:
                st.info("Waiting for file...")
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🌐 Online Channel / IPTV")
        stream_url = st.text_input("Paste M3U8 or Stream Link", placeholder="http://example.com/channel.m3u8")
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            model_stream = st.selectbox("AI Model for Live", ["FSRCNN", "LapSRN"], key="stream_model")
        with col_s2:
            stream_colorize = st.checkbox("Colorize Live B&W", value=False, key="stream_color")
        
        if st.button("📺 Start HDMI Output"):
            if stream_url:
                st.warning("A new window will open on your computer. Drag it to your HDMI screen and press 'F' for Fullscreen. (Press 'Q' to quit)")
                try:
                    upscaler = AiWalkmanEngine(model_name=model_stream.lower(), scale=2, colorize=stream_colorize) # Scale 2 for better FPS
                    upscaler.stream_live(stream_url)
                except Exception as e:

                    st.error(f"Could not connect to channel: {e}")
            else:
                st.error("Please enter a valid channel URL.")
        st.markdown('</div>', unsafe_allow_html=True)


    st.markdown("---")
    st.caption("Powered by OpenCV Deep Learning Super-Resolution Engine")

if __name__ == "__main__":
    main()
