from customtkinter import *
from PIL import Image, ImageTk
import cv2

from video_stream import VideoCapture
from ptz_control import PTZControl
from ultralytics import YOLO
from utils.load_images import load_arrow_images
from utils.config import CAMERA_CONFIG


class V380Camera:
    def __init__(self, window):
        self.window = window
        self.window.title("V380 Camera")
##        self.window.geometry("1000x610")
        self.window.geometry("1440x900")

        self.frame = CTkFrame(master=window, fg_color="#17212b")
        self.frame.pack(fill=BOTH, expand=True)

        self.canvas = CTkCanvas(master=self.frame, height=720, width=1280)
        self.canvas.grid(row=1, column=1, padx=5, pady=5)

        # Load arrow images
        self.left_arrow_img, self.right_arrow_img, self.up_arrow_img, self.down_arrow_img = load_arrow_images()

        # PTZ control
        self.ptz_control = PTZControl()

        # Create buttons for PTZ control
        self.up_button = CTkButton(master=self.frame,
                                   text=None,
                                   image=CTkImage(light_image=self.up_arrow_img, dark_image=self.up_arrow_img),
                                   command=self.ptz_control.move_up,
                                   height=26,
                                   width=15)
        self.up_button.grid(row=4, column=3, padx=5, pady=5)

        self.left_button = CTkButton(master=self.frame,
                                     text=None,
                                     image=CTkImage(light_image=self.left_arrow_img, dark_image=self.left_arrow_img),
                                     command=self.ptz_control.move_left,
                                     height=26,
                                     width=15)
        self.left_button.grid(row=5, column=2, padx=5, pady=5)

        self.right_button = CTkButton(master=self.frame,
                                      text=None,
                                      image=CTkImage(light_image=self.right_arrow_img, dark_image=self.right_arrow_img),
                                      command=self.ptz_control.move_right,
                                      height=26,
                                      width=15)
        self.right_button.grid(row=5, column=4, padx=5, pady=5)

        self.down_button = CTkButton(master=self.frame,
                                     text=None,
                                     image=CTkImage(light_image=self.down_arrow_img, dark_image=self.down_arrow_img),
                                     command=self.ptz_control.move_down,
                                     height=26,
                                     width=15)
        self.down_button.grid(row=6, column=3, padx=5, pady=5)

        # Video Capture for real-time processing
        self.video_capture = VideoCapture(f"rtsp://{CAMERA_CONFIG['usr']}:{CAMERA_CONFIG['pwd']}@{CAMERA_CONFIG['ip']}/live/")

        # Load the YOLOv8 model
        self.model = YOLO('utils/yolov8n.pt')

        # Start updating the camera feed
        self.update_camera()

    def update_camera(self):
        frame, success = self.video_capture.read()

        if success:
            results = self.model(frame)
            annotated_frame = results[0].plot()
            self.current_image = Image.fromarray(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGBA))
            photo = ImageTk.PhotoImage(image=self.current_image)
            self.canvas.create_image(0, 0, image=photo, anchor=NW)
            self.canvas.image = photo  # Keep a reference to the image

        self.window.after(15, self.update_camera)

    def on_closing(self):
        self.video_capture.stop()
        self.window.destroy()
