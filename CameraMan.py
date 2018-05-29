import subprocess
import time

#cmd = 'ffmpeg -rtbufsize 702000k -video_size 1280x720 -pix_fmt uyvy422 -framerate 30 -f avfoundation -i "0:0" -c:v libx264 -tune zerolatency -crf 0 -preset ultrafast -f avi -map 0:v pipe: \
#-f avi output.avi | ffplay pipe:'

cmd = 'ffmpeg -rtbufsize 702000k -video_size 1280x720 -pix_fmt uyvy422 -framerate 30 -f avfoundation -i "0:0" -f avi -map 0:v pipe: \
-f avi output.avi | ffplay pipe:'

input("Press Enter to Start Recording.")
print("Recording")

p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

input("Press Enter to Stop Filming.")
p.terminate()

print("Recording Completed.")
