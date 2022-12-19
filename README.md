# Image to ASCII
## Project Description
This project is a web application that converts Images & YouTube videos into ASCII art. It uses the Flask framework and the SocketIO library to communicate with the web application.

## Getting Started
To run the project, follow these steps:

### Prerequisites
You will need to have the following installed on your machine:

 - Python 3
 - Flask
 - Flask Sockets
 - Flask SocketIO
 - youtube-dl
 - html2image
 - OpenCV
 - Pillow
 - NumPy
 - PyTorch

You can install these libraries using pip:
```cmd
 pip install -r requirements.txt
 ```
### File Descriptions
Python, image tot ASCII module:
 - image_to_ascii.py: A Python module that contains a function for converting images to ASCII art.
  
<br/>  
(Extra) Web Application Files:  

 - run.py: The main Python file that runs the Flask server and contains the SocketIO event handlers.
 - web_app/templates: A folder containing the HTML templates for the web application.
 - web_app/static: A folder containing the JavaScript, CSS, and image files for the web application.

### Running the Application
To start the application, run the run.py file in the root directory:

```cmd
 python run.py
 ```
This will start the Flask development server and the application will be available at http://localhost:5000.


## Notes
 - The YouTube event handler only downloads and processes videos that are <= 720p and have a frame rate <= 32 fps to ensure the best performance.
 - The ASCII art generated from the YouTube videos may not be as clear as the ASCII art generated from images, as the video frames are captured at a much lower frame rate.


 # Examples
 