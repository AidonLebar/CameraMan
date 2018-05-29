import subprocess
import time
from time import gmtime, strftime
from datetime import datetime
import shutil
from os import listdir

#record and preview
cmd = 'ffmpeg -rtbufsize 256MB -video_size 1280x720 -pix_fmt uyvy422 -framerate 30 -f avfoundation -i "0:0" -vf hflip -c:v rawvideo -f nut -map 0:v pipe: \
-f avi -c:v copy output.avi | ffplay pipe:'

#compress video and rename output to current time
filename = "{}.avi".format(datetime.now().strftime('%Y-%m-%d %Hh%M'))
cmd2 = 'ffmpeg -i output.avi -vf hflip -c:v libx264 -crf 17 -f avi \"{}\"'.format(filename)

devices = listdir('/Volumes')
print("Please Insert USB Storage Device.")

while(True):
    devices2 = listdir('/Volumes')
    l = [x for x in devices2 if x not in devices]
    if l:
        usb = l[0]
        break
print("Found USB: {}".format(usb))

input("Press Enter to Start Recording.")
for i in range(3,0,-1): #count in
    print(i)
    time.sleep(1)
print("Recording...")

p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

input("Press Enter to Stop Recording.")
p.stdin.write('q'.encode())
p.stdin.close()
p.terminate()

p.wait()

print("Recording Completed. Compressing...")
p2 = subprocess.Popen(cmd2, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
p2.wait()
p3 = subprocess.Popen('rm output.avi', stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
print("Compression Complete. Moving video to USB...")

shutil.move("./{}".format(filename), "/Volumes/{}/{}".format(usb, filename))

print("Move Completed. Please Eject and Remove USB Storage Device")
