import os
import tempfile
from typing import Optional
from pytube import YouTube
from faster_whisper import WhisperModel

# Initialize Whisper model with 8-bit quantization for memory efficiency
model = WhisperModel("large-v3", device="cpu", compute_type="int8")

def download_audio(url: str) -> Optional[str]:
    """Download audio from YouTube video and save as temporary file."""
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        if not audio_stream:
            return None
            
        # Create temp file with .mp3 extension
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"{yt.video_id}.mp3")
        
        # Download audio
        audio_stream.download(output_path=temp_dir, filename=f"{yt.video_id}.mp3")
        return temp_path
        
    except Exception as e:
        print(f"Error downloading audio: {str(e)}")
        return None

def transcribe_video(url: str) -> Optional[str]:
    """Download and transcribe a YouTube video."""
    try:
        # Download audio
        audio_path = download_audio(url)
        if not audio_path:
            return None
            
        # Transcribe audio
        segments, _ = model.transcribe(
            audio_path,
            beam_size=5,
            word_timestamps=True,
            vad_filter=True
        )
        
        # Combine segments into full transcript
        transcript = " ".join([segment.text for segment in segments])
        
        # Clean up temp file
        try:
            os.remove(audio_path)
        except:
            pass
            
        return transcript
        
    except Exception as e:
        print(f"Error transcribing video: {str(e)}")
        return None