import cv2
from flask import Flask, render_template, request
from flask_sockets import Sockets
from flask_socketio import SocketIO, send, emit
import re
import numpy as np
import youtube_dl
from PIL import Image
from io import BytesIO
import torch
from threading import Thread
import time


from image_to_ascii.image_to_ascii import preprocess_image, create_an_alphabet

# from engineio.async_drivers import gevent

app = Flask(__name__, template_folder="web_app/templates", static_folder="web_app/static")
app.debug = True

socketio = SocketIO(app, max_http_buffer_size=32 * (1024**2), ping_timeout = 10*60)

#
# GLOBAL VARIABLES
#

## Alphabet
## LETTERS, PATTERNS, WIDTH, HEIGHT = create_an_alphabet(alphabet = ".:*|#/\\ _-≃^\"'")
LETTERS, PATTERNS, WIDTH, HEIGHT = create_an_alphabet()


## Kernel
KERNEL = torch.stack(PATTERNS, dim=0)[:,None,:,:]

#
# SOCKETIO EVENTS
#
@socketio.event
def connect(message):
    # print("++++++++")
    # print(message)
    # for i in range(10):
    #     print(i)
    #     emit("my_response", {"data": i})
    emit("my_response", {"data": "got it!"})


def image_to_ascii(image):
    """TODO

    Args:
        image (_type_): _description_
    """
    # convert image to torch tensor
    image = torch.tensor(image, dtype=torch.float32)

    # get lines and edges
    processed_image = preprocess_image(image, HEIGHT, WIDTH) 
    letter_index = ((processed_image - KERNEL)**2).mean(dim=(-2,-1)).argmin(dim=0).view(int(image.shape[0]/HEIGHT), int(image.shape[1]/WIDTH)).numpy()

    # Ascii image
    ascii_image = LETTERS[letter_index]

    # Return a success message
    return ascii_image.tolist()


@socketio.event
def youtube(message):
    """The YouTube event handler exists out of the following steps:
        1. Check if the message contains a valid id
        2. Create a YouTube link
        3. Extract the YouTube video info
        4. Select the highest quality video <= 720p with the lowest filesize
        5. Get the video
        6. Loop over the frames
         7. Convert the frame to ascii

    Args:
        message (dict): message.data contains the YouTube id

    """
    # 1) Quick check if the message contains an id
    if 5 < len(re.sub(message.get("data", "-"), "[^a-z0-9A-Z\-\=\_]+", "")) <= 20:
        return

    # 2) Create a youtube link
    link = f"https://www.youtube.com/watch?v={message['data']}"

    # 3) Extract the youtube video info
    ydl_opts = {}
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    info_dict = ydl.extract_info(link, download=False)

    # 4) Loop over the different qualities and select the highest quality with the lowest filesize
    formats = info_dict.get("formats", None)
    video_info = []
    for f in formats:
        if f.get("ext", None) != "mp4":
            continue
        if f.get("fps", 100) > 32:
            continue
        if f.get("fps", None) == None:
            continue
        if f.get("filesize", None) == None:
            continue
        if f.get("format_note", "") not in ["240p", "360p", "480p", "720p"]:
            continue

        video_info.append((int(f.get("quality", 0)), int(f.get("filesize", 0)), f))

    if len(video_info) == 0:
        emit("yt_message", {"msg": "We can't process this video"})
    # sort the video info by quality and filesize and
    # select the highest quality with the lowest filesize
    video_info = sorted(video_info, key=lambda x: (-x[0], x[1]))[0][-1]

    # 5) Get the video
    emit("yt_message", {"msg": "Starting to load the video"})
    socketio.sleep(1)

    # Setup the video
    threaded_camera = ThreadedCamera(video_info.get("url", None))
    emit("yt_message", {"msg": "Loading complete"})
    socketio.sleep(1)

    # 6) Loop over the frames
    while True:
        frame = threaded_camera.get_frame()
        if frame is None:
            break

        emit("response", {"frame": image_to_ascii(frame[:,:,0])})

        socketio.sleep(1/3)




@socketio.event
def image(message):
    """Get the image from the message and convert it to ascii
    
    Args:
        message (dict): message.image contains the image
    """
    # Open the image using PIL
    image = Image.open(BytesIO(message["image"]))

    # Convert the image to grayscale
    image = image.convert("L")

    # Resize the image

    max_size = 1560 if image.size[0] > image.size[1] else 1220
    ratio = image.size[0] / max_size if image.size[0] > image.size[1] else image.size[1] / max_size
    image.thumbnail((int( image.size[0] / ratio), int(image.size[1] / ratio)), Image.Resampling.LANCZOS)

    # Convert the image to a NumPy array
    image = np.array(image)
    print("image 5")

    # Convert the image to ascii
    emit("response", {"frame": image_to_ascii(image)})



@app.route("/")
def main():
    return render_template("index.html")


class ThreadedCamera(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
       
        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1/30 
        self.FPS_MS = int(self.FPS * 1000)
        
        # Start frame retrieval thread
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        time.sleep(2)
        
    def update(self):
        i = 0
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            time.sleep(self.FPS)
            
    def get_frame(self):
        return self.frame


if __name__ == "__main__":
    socketio.run(app)
