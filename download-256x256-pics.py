###
#
# Usage: `$ python download-256x256-pics.py [labelId] [labelsFile] [screenshots/screendumps] [if screendumps, set amount of caps per video, max 128]`
###

import csv, PIL, sys, os, subprocess
from PIL import Image

# Set working dir
os.path.dirname(os.path.realpath(__file__)) 

# function for resizing and cropping to 256x256
def resizeAndCrop(imgPath):
    
    with Image.open(imgPath) as im:

        # remove original
        os.remove(imgPath)
        
        # Get size
        x, y = im.size

        # New sizes
        yNew = 256
        xNew = yNew # should be equal

        # First, set right size
        if x > y:
            # Y is smallest, figure out relation to 256
            xNew = round(x * 256 / y)
        else:
            yNew = round(y * 256 / x)

        # resize
        im.resize((int(xNew), int(yNew)), PIL.Image.ANTIALIAS)

        # crop
        im.crop(((int(xNew) - 256)/2, (int(yNew) - 256)/2, (int(xNew) + 256)/2, (int(yNew) + 256)/2))

        # save
        print("SAVE", imgPath + "2")
        im.save(imgPath)

# Make results dir
os.system("mkdir -p results")

# Count total of occurences
totalLabels = 0
totalLabelsDone = 1
with open(sys.argv[2], 'rb') as labelfile:
    labels = csv.reader(labelfile, delimiter=',')
    for label in labels:
        if sys.argv[1] in label:
            totalLabels = totalLabels + 1

# Open label file
with open(sys.argv[2], 'rb') as labelfile:
    # Itterate over the labels
    labels = csv.reader(labelfile, delimiter=',')
    for label in labels:
        if sys.argv[1] in label:
            # Show progress
            print("Downloading and proccessing (" + str(totalLabelsDone) + "/" + str(totalLabels) + "): " + label[0])
            
            # download video
            if sys.argv[3] == "screendumps":
                # Start the MP4 download
                subprocess.check_output('youtube-dl -f bestvideo[ext=mp4] --output "results/' + label[0] + '.mp4" "http://www.youtube.com/watch?v=' + label[0] + '"', shell=True)
                # Get the duration of the video
                videoInSeconds = int(float(subprocess.check_output("ffprobe -i results/" + label[0] + ".mp4 -show_format -v quiet | sed -n 's/duration=//p'", shell=True)))
                # Make label dir
                os.system("mkdir -p results/" + sys.argv[1])
                # Take 20 second snapshots
                snapSecCount = 5 # start at 5 sec to avoid intros
                snapCount = 0 # count actual snapshots
                while (snapSecCount < videoInSeconds):
                    # Get image
                    out = subprocess.check_output("ffmpeg -loglevel panic -i results/" + label[0] + ".mp4 -ss " + str(snapSecCount) + " -vframes 1 results/" + sys.argv[1] + "/" + label[0] + "-" + str(snapCount) + ".png", shell=True)
                    # Resize and crop
                    resizeAndCrop("./results/" + sys.argv[1] + "/" + label[0] + "-" + str(snapCount) + ".png")
                    # edit counter
                    snapSecCount = snapSecCount + 20
                    snapCount = snapCount + 1
                # Remove the file
                os.system("rm results/" + label[0] + ".mp4")
            # go for the screenshots
            else:
                print("Not implemented yet")

            # Total labels done + 1
            totalLabelsDone = totalLabelsDone + 1

        break # for now, a break

print("DONE")