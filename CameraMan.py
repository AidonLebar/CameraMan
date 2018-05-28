import subprocess
import time

cmd = 'ffmpeg -pix_fmt uyvy422 -f avfoundation -framerate 30 -i \"0:0\" output.avi -hide_banner'

input("Press Enter to Start Recording.")
print("Recording")

p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

input()
p.terminate()

print("Recording Completed.")
