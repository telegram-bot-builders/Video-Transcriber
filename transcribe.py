import moviepy.editor as mp

def extract_audio(video_path: str) -> str:
    clip = mp.VideoFileClip(video_path)
    audio_path = video_path.replace('.mp4', '.mp3')
    clip.audio.write_audiofile(audio_path)
    return audio_path