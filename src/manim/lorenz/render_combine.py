import subprocess
import os
from pathlib import Path

# Configuration
quality = "high" #"low"
manim_file = "lorenzCsound.py"  # Replace with your Manim script name
manim_class = "LorenzAttractor"             # Replace with your Manim scene class
if quality == "high":
    output_dir = "media/videos/lorenzCsound/1080p60"          # Manim's default output directory
else:
    output_dir = "media/videos/lorenzCsound/480p15"
wav_file = "assets/output.wav"         # Path to your WAV file
final_output = "assets/LorenzCsound.mp4"     # Desired output file

# Step 1: Render the Manim animation
print("Rendering Manim animation...")

if quality == "high":
    render_cmd = f"manim -qh {manim_file} {manim_class}"
else:
    render_cmd = f"manim -ql {manim_file} {manim_class}"
subprocess.run(render_cmd, shell=True, check=True)

# Find the latest rendered video file (Manim saves files with random suffixes)
video_files = list(Path(output_dir).glob(f"{manim_class}*.mp4"))
if not video_files:
    raise FileNotFoundError("No rendered video found!")

latest_video = max(video_files, key=os.path.getmtime)
print(f"Rendered video: {latest_video}")

# Step 2: Combine video and audio using ffmpeg
print("Combining video and audio...")
ffmpeg_cmd = [
    "ffmpeg",
    "-i", str(latest_video),  # Input video
    "-i", wav_file,          # Input audio
    "-c:v", "copy",          # Copy video stream (no re-encode)
    "-c:a", "aac",           # Encode audio to AAC (for MP4 compatibility)
    "-shortest",             # Trim to the shortest stream (video or audio)
    final_output
]

subprocess.run(ffmpeg_cmd, check=True)
print(f"Final output saved to: {final_output}")