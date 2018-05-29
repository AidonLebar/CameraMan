import subprocess
import time

cmd = 'ffmpeg -rtbufsize 256MB -video_size 1280x720 -pix_fmt uyvy422 -framerate 30 -f avfoundation -i "0:0" -c:v rawvideo -f nut -map 0:v pipe: \
-f avi -c:v copy output.avi | ffplay pipe:'

input("Press Enter to Start Recording.")
print("Recording")

p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

input("Press Enter to Stop Filming.")
p.terminate()

print("Recording Completed.")
