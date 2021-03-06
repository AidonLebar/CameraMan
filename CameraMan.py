import subprocess
import time
import shutil
import os
import re
import sys
from time import gmtime, strftime
from datetime import datetime

platform = sys.platform
filename = "{}.avi".format(datetime.now().strftime('%Y-%m-%d %Hh%M'))
if platform == 'linux':
    #input path may need to be changed depending on setup
    ip = '/dev/video0'
    #record and preview
    cmd = 'ffmpeg -rtbufsize 256MB -video_size 1280x720 -pix_fmt mjpeg -framerate 30 -f v4l2 -i {} -vf hflip -c:v rawvideo -f nut -map 0:v pipe: \
    -f avi -c:v copy output.avi | ffplay pipe:'.format(ip)

    #compress video and rename output to current time
    cmd2 = 'ffmpeg -i output.avi -vf hflip -c:v libx264 -crf 17 -f avi \"{}\"'.format(filename)

    print("Please Insert USB Storage Device.")

    devices = os.listdir('/media/{}'.format(os.getlogin()))

    while(True):
        devices2 = os.listdir('/media/{}'.format(os.getlogin()))
        l = [x for x in devices2 if x not in devices]

        if l:
            usb = l[0]
            break
    print("Found USB: {}".format(usb))

    #rm original output
    cmd3 = 'rm output.avi'

    #unmount USB
    cmd4 = 'umount /media/{}/{}'.format(os.getlogin(), usb)

elif platform == 'win32' or platform == 'cygwin':
    print("Windows is Not Currently Supported.")
    sys.exit(1)

elif platform == 'darwin':
    #device numbers may need to be changed depending on setup
    dn = "0:0"
    #record and preview
    cmd = 'ffmpeg -rtbufsize 256MB -video_size 1280x720 -pix_fmt uyvy422 -framerate 30 -f avfoundation -i {} -vf hflip -c:v rawvideo -f nut -map 0:v pipe: \
    -f avi -c:v copy output.avi | ffplay pipe:'.format(dn)

    #compress video and rename output to current time
    filename = "{}.avi".format(datetime.now().strftime('%Y-%m-%d %Hh%M'))
    cmd2 = 'ffmpeg -i output.avi -vf hflip -c:v libx264 -crf 17 -f avi \"{}\"'.format(filename)

    devices = os.listdir('/Volumes')

    d = os.listdir('/dev')
    r = re.compile('^disk.$')
    d = list(filter(r.match, d))

    print("Please Insert USB Storage Device.")

    while(True):
        devices2 = os.listdir('/Volumes')
        l = [x for x in devices2 if x not in devices]

        if l:
            usb = l[0]

            d2 = os.listdir('/dev')
            d2 = list(filter(r.match, d2))
            d2 = [x for x in d2 if x not in d]
            d2 = d2[0]

            break
    print("Found USB: {}".format(usb))

    #rm original output
    cmd3 = 'rm output.avi'

    #unmount USB
    cmd4 = 'diskutil unmountDisk /dev/{}'.format(d2)


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
p3 = subprocess.Popen(cmd3, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
print("Compression Complete. Moving Video to USB...")

if platform == 'linux':
    shutil.move("./{}".format(filename), "/media/{}/{}/{}".format(os.getlogin(),usb, filename))
elif platform == 'darwin':
    shutil.move("./{}".format(filename), "/Volumes/{}/{}".format(usb, filename))

p4 = subprocess.Popen(cmd4, stdout=subprocess.PIPE, shell=True)
p4.wait()

print("Completed. Please Remove USB Storage Device.")
