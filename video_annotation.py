# # # import tkinter as tk
# # # from tkinter import ttk
# # # import cv2
# # # from PIL import Image, ImageTk
# # # import json
# # # import csv
# # # import os
# # # from pathlib import Path
# # # import sys
# # #
# # # BTN_FONT = ("Helvetica", 14)  # Font for buttons/labels
# # # SLIDER_LENGTH = 400           # Length of the slider
# # #
# # # # Percentage of screen dimensions we allow the videos+controls to occupy
# # # SCREEN_WIDTH_PERCENT = 0.90
# # # SCREEN_HEIGHT_PERCENT = 0.80
# # #
# # # class VideoPlayer:
# # #     """
# # #     Handles loading a video file, extracting frames, and displaying them on a Tkinter widget.
# # #     Dynamically resizes frames based on a precomputed scale factor.
# # #     """
# # #     def __init__(self, video_path, widget, scale_factor):
# # #         """
# # #         Initialize the VideoPlayer.
# # #         :param video_path: Path to the video file.
# # #         :param widget: Tkinter Label widget where the video frame will be displayed.
# # #         :param scale_factor: A float scale factor (e.g. 0.5) to resize each frame.
# # #         """
# # #         self.video_path = video_path
# # #         self.widget = widget
# # #         self.cap = cv2.VideoCapture(video_path)
# # #         if not self.cap.isOpened():
# # #             raise Exception(f"Cannot open video file: {video_path}")
# # #
# # #         self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
# # #         self.fps = self.cap.get(cv2.CAP_PROP_FPS)
# # #         if self.fps == 0:
# # #             self.fps = 25  # fallback fps if not available
# # #
# # #         self.scale_factor = scale_factor
# # #         self.current_frame = 0
# # #         self.photo = None
# # #
# # #     def show_frame(self, frame_index):
# # #         """
# # #         Set the video capture to the specified frame index, read the frame, and display it.
# # #         :param frame_index: Index of the frame to display.
# # #         """
# # #         # Clamp frame index within valid bounds.
# # #         if frame_index < 0:
# # #             frame_index = 0
# # #         if frame_index >= self.total_frames:
# # #             frame_index = self.total_frames - 1
# # #
# # #         self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
# # #         ret, frame = self.cap.read()
# # #         if ret:
# # #             self.current_frame = frame_index
# # #             # Convert from BGR (OpenCV) to RGB (Pillow)
# # #             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# # #
# # #             # Resize using the precomputed scale factor
# # #             h, w = frame.shape[:2]
# # #             new_width = int(w * self.scale_factor)
# # #             new_height = int(h * self.scale_factor)
# # #             frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
# # #
# # #             # Convert to PIL and then to ImageTk
# # #             im = Image.fromarray(frame)
# # #             self.photo = ImageTk.PhotoImage(image=im)
# # #             self.widget.config(image=self.photo)
# # #         else:
# # #             print(f"Warning: Could not read frame {frame_index} from {self.video_path}")
# # #
# # #     def get_current_time(self):
# # #         """
# # #         Returns the current playback time in seconds.
# # #         """
# # #         return self.current_frame / self.fps
# # #
# # #     def release(self):
# # #         """
# # #         Release the video capture resource.
# # #         """
# # #         self.cap.release()
# # #
# # # class AnnotationManager:
# # #     """
# # #     Handles annotation controls, reading labels from a JSON file, and saving annotations to a CSV file.
# # #     Stores annotations in memory until user clicks "Save Annotations".
# # #     """
# # #     def __init__(self, parent, time_callback, video_file):
# # #         """
# # #         Initialize the AnnotationManager.
# # #         :param parent: Tkinter frame where the annotation widgets will be placed.
# # #         :param time_callback: Function to obtain the current playback time.
# # #         :param video_file: Path to one of the video files (used to determine CSV file location).
# # #         """
# # #         self.parent = parent
# # #         self.time_callback = time_callback
# # #         self.annotation_start = None
# # #         self.annotations = []  # store annotations in memory until saved
# # #
# # #         # Load annotation labels from JSON file.
# # #         try:
# # #             with open("labels.json", "r") as f:
# # #                 self.labels = json.load(f)
# # #                 # Ensure we have a list.
# # #                 if not isinstance(self.labels, list):
# # #                     raise ValueError("labels.json must contain a JSON array of labels.")
# # #         except Exception as e:
# # #             print("Error loading labels.json:", e)
# # #             self.labels = []
# # #
# # #         # Create a drop-down menu (Combobox) for annotation labels.
# # #         self.label_var = tk.StringVar()
# # #         self.combobox = ttk.Combobox(
# # #             parent,
# # #             textvariable=self.label_var,
# # #             values=self.labels,
# # #             state="readonly",
# # #             font=BTN_FONT
# # #         )
# # #         self.combobox.grid(row=0, column=0, padx=5, pady=5)
# # #         if self.labels:
# # #             self.combobox.current(0)
# # #
# # #         # Create buttons for marking the start and end of an annotation.
# # #         self.start_button = tk.Button(
# # #             parent,
# # #             text="Start of Activity",
# # #             command=self.start_activity,
# # #             font=BTN_FONT,
# # #             width=15,
# # #             height=2
# # #         )
# # #         self.start_button.grid(row=0, column=1, padx=5, pady=5)
# # #
# # #         self.end_button = tk.Button(
# # #             parent,
# # #             text="End of Activity",
# # #             command=self.end_activity,
# # #             font=BTN_FONT,
# # #             width=15,
# # #             height=2
# # #         )
# # #         self.end_button.grid(row=0, column=2, padx=5, pady=5)
# # #
# # #         # Create a button to explicitly save annotations to CSV
# # #         self.save_button = tk.Button(
# # #             parent,
# # #             text="Save Annotations",
# # #             command=self.save_annotations,
# # #             font=BTN_FONT,
# # #             width=15,
# # #             height=2
# # #         )
# # #         self.save_button.grid(row=0, column=3, padx=5, pady=5)
# # #
# # #         # Determine CSV file location: two levels above the video file directory.
# # #         video_path = Path(video_file)
# # #         try:
# # #             csv_folder = video_path.parents[1]  # two levels above
# # #             csv_folder.mkdir(parents=True, exist_ok=True)
# # #             self.csv_file = csv_folder / "annotations.csv"
# # #         except Exception as e:
# # #             print("Error determining CSV file location:", e)
# # #             self.csv_file = Path("annotations.csv")
# # #
# # #         # If CSV file does not exist, create it with a header.
# # #         if not self.csv_file.exists():
# # #             try:
# # #                 with open(self.csv_file, "w", newline="") as f:
# # #                     writer = csv.writer(f)
# # #                     writer.writerow(["Label", "Start Time (s)", "End Time (s)"])
# # #             except Exception as e:
# # #                 print("Error creating CSV file:", e)
# # #
# # #     def start_activity(self):
# # #         """
# # #         Capture the current playback time as the start of an annotation.
# # #         """
# # #         self.annotation_start = self.time_callback()
# # #         print("Annotation started at:", self.annotation_start)
# # #
# # #     def end_activity(self):
# # #         """
# # #         Capture the current playback time as the end and store the annotation in memory.
# # #         """
# # #         if self.annotation_start is None:
# # #             print("Error: Please press 'Start of Activity' before ending an annotation.")
# # #             return
# # #         annotation_end = self.time_callback()
# # #         annotation_label = self.label_var.get()
# # #
# # #         # Store in memory (will only be written to CSV when user clicks "Save Annotations")
# # #         self.annotations.append([annotation_label, self.annotation_start, annotation_end])
# # #         print(f"Annotation stored in memory: {annotation_label}, Start: {self.annotation_start}, End: {annotation_end}")
# # #
# # #         # Reset the start time
# # #         self.annotation_start = None
# # #
# # #     def save_annotations(self):
# # #         """
# # #         Write all stored annotations to the CSV file, then clear them from memory.
# # #         """
# # #         if not self.annotations:
# # #             print("No annotations to save.")
# # #             return
# # #
# # #         try:
# # #             with open(self.csv_file, "a", newline="") as f:
# # #                 writer = csv.writer(f)
# # #                 for ann in self.annotations:
# # #                     writer.writerow(ann)
# # #             print(f"{len(self.annotations)} annotations saved to {self.csv_file}")
# # #             self.annotations.clear()
# # #         except Exception as e:
# # #             print("Error writing annotation to CSV:", e)
# # #
# # #
# # # class MainApp:
# # #     """
# # #     Main application class that integrates the VideoPlayers and AnnotationManager into the Tkinter GUI.
# # #     Dynamically calculates how to scale both videos so they fit side by side on the screen
# # #     with space for controls.
# # #     """
# # #     def __init__(self, root, video_path1, video_path2):
# # #         """
# # #         Initialize the MainApp.
# # #         :param root: The Tkinter root window.
# # #         :param video_path1: Path to the first video file.
# # #         :param video_path2: Path to the second video file.
# # #         """
# # #         self.root = root
# # #         self.root.title("Dual Video Playback and Annotation Tool")
# # #
# # #         # Screen dimensions
# # #         screen_w = self.root.winfo_screenwidth()
# # #         screen_h = self.root.winfo_screenheight()
# # #
# # #         # Let's reserve some fraction of the screen for videos + controls
# # #         max_w = int(screen_w * SCREEN_WIDTH_PERCENT)
# # #         max_h = int(screen_h * SCREEN_HEIGHT_PERCENT)
# # #
# # #         # We will read the first frame of each video just to get their original dimensions
# # #         w1, h1 = self.get_video_dimensions(video_path1)
# # #         w2, h2 = self.get_video_dimensions(video_path2)
# # #
# # #         # Combined side-by-side dimensions
# # #         combined_width = w1 + w2
# # #         combined_height = max(h1, h2)
# # #
# # #         # Determine a scale factor so that combined_width <= max_w and combined_height <= max_h
# # #         scale_w = max_w / float(combined_width)
# # #         scale_h = max_h / float(combined_height)
# # #         scale_factor = min(scale_w, scale_h, 1.0)  # don't exceed 1.0 (no upscaling)
# # #
# # #         # Now we can set our window size to something close to the scaled dimensions
# # #         # Add some vertical space for the controls
# # #         scaled_width = int(combined_width * scale_factor)
# # #         scaled_height = int(combined_height * scale_factor)
# # #         extra_height = 200  # approximate space for controls/annotations
# # #         window_width = scaled_width
# # #         window_height = scaled_height + extra_height
# # #
# # #         # Center the window on the screen
# # #         x_pos = (screen_w - window_width) // 2
# # #         y_pos = (screen_h - window_height) // 2
# # #         self.root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
# # #
# # #         # Frame to hold the video displays.
# # #         self.video_frame = tk.Frame(root)
# # #         self.video_frame.pack()
# # #
# # #         # Labels where the video frames will be shown side by side.
# # #         self.video_label1 = tk.Label(self.video_frame)
# # #         self.video_label1.grid(row=0, column=0)
# # #         self.video_label2 = tk.Label(self.video_frame)
# # #         self.video_label2.grid(row=0, column=1)
# # #
# # #         # Initialize VideoPlayers for both videos with the computed scale factor.
# # #         self.player1 = VideoPlayer(video_path1, self.video_label1, scale_factor)
# # #         self.player2 = VideoPlayer(video_path2, self.video_label2, scale_factor)
# # #
# # #         # Use the lower total frame count to synchronize playback length.
# # #         self.total_frames = min(self.player1.total_frames, self.player2.total_frames)
# # #         self.fps = self.player1.fps  # Assume both videos have the same fps
# # #         self.current_frame = 0
# # #         self.playing = False
# # #
# # #         # Playback controls.
# # #         self.controls_frame = tk.Frame(root)
# # #         self.controls_frame.pack(pady=10)
# # #
# # #         self.play_button = tk.Button(
# # #             self.controls_frame,
# # #             text="Play",
# # #             command=self.play,
# # #             font=BTN_FONT,
# # #             width=10,
# # #             height=2
# # #         )
# # #         self.play_button.grid(row=0, column=0, padx=5)
# # #
# # #         self.pause_button = tk.Button(
# # #             self.controls_frame,
# # #             text="Pause",
# # #             command=self.pause,
# # #             font=BTN_FONT,
# # #             width=10,
# # #             height=2
# # #         )
# # #         self.pause_button.grid(row=0, column=1, padx=5)
# # #
# # #         self.forward_button = tk.Button(
# # #             self.controls_frame,
# # #             text="Next Frame",
# # #             command=self.next_frame,
# # #             font=BTN_FONT,
# # #             width=10,
# # #             height=2
# # #         )
# # #         self.forward_button.grid(row=0, column=2, padx=5)
# # #
# # #         self.backward_button = tk.Button(
# # #             self.controls_frame,
# # #             text="Previous Frame",
# # #             command=self.previous_frame,
# # #             font=BTN_FONT,
# # #             width=10,
# # #             height=2
# # #         )
# # #         self.backward_button.grid(row=0, column=3, padx=5)
# # #
# # #         # Slider for jumping to a specific frame.
# # #         self.slider = tk.Scale(
# # #             self.controls_frame,
# # #             from_=0,
# # #             to=self.total_frames - 1,
# # #             orient=tk.HORIZONTAL,
# # #             length=SLIDER_LENGTH,
# # #             command=self.slider_jump,
# # #             font=BTN_FONT
# # #         )
# # #         self.slider.grid(row=1, column=0, columnspan=4, pady=10)
# # #
# # #         # Annotation controls.
# # #         self.annotation_frame = tk.Frame(root)
# # #         self.annotation_frame.pack(pady=10)
# # #
# # #         # Pass a callback to get the current time and use video_path1 to determine CSV location.
# # #         self.annotation_manager = AnnotationManager(self.annotation_frame, self.get_current_time, video_path1)
# # #
# # #         # Display the initial frame.
# # #         self.update_frames(self.current_frame)
# # #
# # #     def get_video_dimensions(self, video_path):
# # #         """
# # #         Open the video, read the first frame to get its width and height.
# # #         Returns (width, height). If fail, returns (640, 480) as a fallback.
# # #         """
# # #         cap = cv2.VideoCapture(video_path)
# # #         if not cap.isOpened():
# # #             print(f"Warning: Could not open {video_path}. Using default dimensions.")
# # #             return 640, 480
# # #
# # #         ret, frame = cap.read()
# # #         if not ret:
# # #             print(f"Warning: Could not read first frame of {video_path}. Using default dimensions.")
# # #             cap.release()
# # #             return 640, 480
# # #
# # #         height, width = frame.shape[:2]
# # #         cap.release()
# # #         return width, height
# # #
# # #     def update_frames(self, frame_index):
# # #         """
# # #         Update both VideoPlayers to display the specified frame.
# # #         :param frame_index: The frame index to display.
# # #         """
# # #         self.player1.show_frame(frame_index)
# # #         self.player2.show_frame(frame_index)
# # #         self.slider.set(frame_index)
# # #
# # #     def get_current_time(self):
# # #         """
# # #         Returns the current playback time based on the current frame and fps.
# # #         """
# # #         return self.current_frame / self.fps
# # #
# # #     def play(self):
# # #         """
# # #         Start/resume video playback.
# # #         """
# # #         self.playing = True
# # #         self.play_loop()
# # #
# # #     def play_loop(self):
# # #         """
# # #         Playback loop that updates frames. Continues until paused or the end is reached.
# # #         """
# # #         if self.playing:
# # #             if self.current_frame < self.total_frames - 1:
# # #                 self.current_frame += 1
# # #                 self.update_frames(self.current_frame)
# # #                 # Delay based on fps
# # #                 delay = int(1000 / self.fps)
# # #                 self.root.after(delay, self.play_loop)
# # #             else:
# # #                 self.playing = False
# # #
# # #     def pause(self):
# # #         """
# # #         Pause video playback.
# # #         """
# # #         self.playing = False
# # #
# # #     def next_frame(self):
# # #         """
# # #         Advance to the next frame.
# # #         """
# # #         self.pause()
# # #         if self.current_frame < self.total_frames - 1:
# # #             self.current_frame += 1
# # #             self.update_frames(self.current_frame)
# # #
# # #     def previous_frame(self):
# # #         """
# # #         Go back to the previous frame.
# # #         """
# # #         self.pause()
# # #         if self.current_frame > 0:
# # #             self.current_frame -= 1
# # #             self.update_frames(self.current_frame)
# # #
# # #     def slider_jump(self, value):
# # #         """
# # #         Jump to a specific frame when the slider is moved.
# # #         :param value: The frame index (as a string) from the slider.
# # #         """
# # #         self.current_frame = int(value)
# # #         self.update_frames(self.current_frame)
# # #
# # #     def on_close(self):
# # #         """
# # #         Handle cleanup when the window is closed.
# # #         """
# # #         self.player1.release()
# # #         self.player2.release()
# # #         self.root.destroy()
# # #
# # # if __name__ == "__main__":
# # #     # Ensure two video file paths are provided.
# # #     if len(sys.argv) < 3:
# # #         print("Run python video_annotation.py path_to_video1 path_to_video2")
# # #         sys.exit(1)
# # #     video_path1 = sys.argv[1]
# # #     video_path2 = sys.argv[2]
# # #
# # #     root = tk.Tk()
# # #     app = MainApp(root, video_path1, video_path2)
# # #     root.protocol("WM_DELETE_WINDOW", app.on_close)
# # #     root.mainloop()
# # import tkinter as tk
# # from tkinter import ttk
# # import cv2
# # from PIL import Image, ImageTk
# # import json
# # import csv
# # import os
# # from pathlib import Path
# # import sys
# #
# # BTN_FONT = ("Helvetica", 14)
# # SLIDER_LENGTH = 300
# #
# # # Percent of the screen we allow for the videos area
# # VIDEOS_WIDTH_PERCENT = 0.70   # 70% of screen width used for videos
# # VIDEOS_HEIGHT_PERCENT = 0.80  # 80% of screen height used for videos
# #
# # class VideoPlayer:
# #     """
# #     Handles loading a video file, extracting frames, and displaying them on a Tkinter widget.
# #     Dynamically resizes frames based on a precomputed scale factor.
# #     """
# #     def __init__(self, video_path, widget, scale_factor):
# #         self.video_path = video_path
# #         self.widget = widget
# #         self.cap = cv2.VideoCapture(video_path)
# #         if not self.cap.isOpened():
# #             raise Exception(f"Cannot open video file: {video_path}")
# #
# #         self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
# #         self.fps = self.cap.get(cv2.CAP_PROP_FPS)
# #         if self.fps == 0:
# #             self.fps = 25  # fallback fps
# #
# #         self.scale_factor = scale_factor
# #         self.current_frame = 0
# #         self.photo = None
# #
# #     def show_frame(self, frame_index):
# #         if frame_index < 0:
# #             frame_index = 0
# #         if frame_index >= self.total_frames:
# #             frame_index = self.total_frames - 1
# #
# #         self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
# #         ret, frame = self.cap.read()
# #         if ret:
# #             self.current_frame = frame_index
# #             # Convert BGR -> RGB
# #             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# #
# #             # Resize
# #             h, w = frame.shape[:2]
# #             new_w = int(w * self.scale_factor)
# #             new_h = int(h * self.scale_factor)
# #             frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
# #
# #             # Convert to ImageTk
# #             im = Image.fromarray(frame)
# #             self.photo = ImageTk.PhotoImage(image=im)
# #             self.widget.config(image=self.photo)
# #         else:
# #             print(f"Warning: Could not read frame {frame_index} from {self.video_path}")
# #
# #     def get_current_time(self):
# #         return self.current_frame / self.fps
# #
# #     def release(self):
# #         self.cap.release()
# #
# #
# # class AnnotationManager:
# #     """
# #     Handles annotation controls, reading labels from a JSON file, and saving annotations to a CSV file.
# #     Stores annotations in memory until user clicks "Save Annotations".
# #     """
# #     def __init__(self, parent, time_callback, video_file):
# #         self.parent = parent
# #         self.time_callback = time_callback
# #         self.annotation_start = None
# #         self.annotations = []  # store until "Save Annotations" is clicked
# #
# #         # Load annotation labels
# #         try:
# #             with open("labels.json", "r") as f:
# #                 self.labels = json.load(f)
# #                 if not isinstance(self.labels, list):
# #                     raise ValueError("labels.json must contain a JSON array.")
# #         except Exception as e:
# #             print("Error loading labels.json:", e)
# #             self.labels = []
# #
# #         self.label_var = tk.StringVar()
# #         self.combobox = ttk.Combobox(
# #             parent,
# #             textvariable=self.label_var,
# #             values=self.labels,
# #             state="readonly",
# #             font=BTN_FONT
# #         )
# #         self.combobox.grid(row=0, column=0, padx=5, pady=5)
# #         if self.labels:
# #             self.combobox.current(0)
# #
# #         self.start_button = tk.Button(
# #             parent,
# #             text="Start of Activity",
# #             command=self.start_activity,
# #             font=BTN_FONT,
# #             width=15,
# #             height=2
# #         )
# #         self.start_button.grid(row=1, column=0, padx=5, pady=5)
# #
# #         self.end_button = tk.Button(
# #             parent,
# #             text="End of Activity",
# #             command=self.end_activity,
# #             font=BTN_FONT,
# #             width=15,
# #             height=2
# #         )
# #         self.end_button.grid(row=2, column=0, padx=5, pady=5)
# #
# #         self.save_button = tk.Button(
# #             parent,
# #             text="Save Annotations",
# #             command=self.save_annotations,
# #             font=BTN_FONT,
# #             width=15,
# #             height=2
# #         )
# #         self.save_button.grid(row=3, column=0, padx=5, pady=5)
# #
# #         # Determine CSV file location
# #         video_path = Path(video_file)
# #         try:
# #             csv_folder = video_path.parents[1]
# #             csv_folder.mkdir(parents=True, exist_ok=True)
# #             self.csv_file = csv_folder / "annotations.csv"
# #         except Exception as e:
# #             print("Error determining CSV file location:", e)
# #             self.csv_file = Path("annotations.csv")
# #
# #         # Create CSV file if not exists
# #         if not self.csv_file.exists():
# #             try:
# #                 with open(self.csv_file, "w", newline="") as f:
# #                     writer = csv.writer(f)
# #                     writer.writerow(["Label", "Start Time (s)", "End Time (s)"])
# #             except Exception as e:
# #                 print("Error creating CSV file:", e)
# #
# #     def start_activity(self):
# #         self.annotation_start = self.time_callback()
# #         print("Annotation started at:", self.annotation_start)
# #
# #     def end_activity(self):
# #         if self.annotation_start is None:
# #             print("Error: Press 'Start of Activity' first.")
# #             return
# #         annotation_end = self.time_callback()
# #         annotation_label = self.label_var.get()
# #         self.annotations.append([annotation_label, self.annotation_start, annotation_end])
# #         print(f"Annotation in memory: {annotation_label}, Start: {self.annotation_start}, End: {annotation_end}")
# #         self.annotation_start = None
# #
# #     def save_annotations(self):
# #         if not self.annotations:
# #             print("No annotations to save.")
# #             return
# #         try:
# #             with open(self.csv_file, "a", newline="") as f:
# #                 writer = csv.writer(f)
# #                 for ann in self.annotations:
# #                     writer.writerow(ann)
# #             print(f"Saved {len(self.annotations)} annotations to {self.csv_file}")
# #             self.annotations.clear()
# #         except Exception as e:
# #             print("Error writing annotation to CSV:", e)
# #
# #
# # class MainApp:
# #     """
# #     Main application class for stacking two videos vertically and placing controls on the right.
# #     """
# #     def __init__(self, root, video_path1, video_path2):
# #         self.root = root
# #         self.root.title("Vertical Dual Video & Annotation")
# #
# #         screen_w = self.root.winfo_screenwidth()
# #         screen_h = self.root.winfo_screenheight()
# #
# #         # We'll let the stacked videos occupy up to these dimensions:
# #         max_w = int(screen_w * VIDEOS_WIDTH_PERCENT)   # 70% of screen width
# #         max_h = int(screen_h * VIDEOS_HEIGHT_PERCENT)  # 80% of screen height
# #
# #         # Get original sizes
# #         w1, h1 = self.get_video_dimensions(video_path1)
# #         w2, h2 = self.get_video_dimensions(video_path2)
# #
# #         # Stacked: total height = h1 + h2, total width = max(w1, w2)
# #         combined_height = h1 + h2
# #         combined_width = max(w1, w2)
# #
# #         # Compute scale factor
# #         scale_w = max_w / float(combined_width)
# #         scale_h = max_h / float(combined_height)
# #         scale_factor = min(scale_w, scale_h, 1.0)
# #
# #         # Window size: We'll just scale the videos area + add some space for the side controls
# #         scaled_w = int(combined_width * scale_factor)
# #         scaled_h = int(combined_height * scale_factor)
# #
# #         # Add a bit of extra width for the side controls
# #         side_controls_width = 300
# #         window_width = scaled_w + side_controls_width
# #         window_height = max(scaled_h, 600)  # ensure a minimum height for controls
# #
# #         # Center the window
# #         x_pos = (screen_w - window_width) // 2
# #         y_pos = (screen_h - window_height) // 2
# #         self.root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
# #
# #         # Main container frames
# #         self.left_frame = tk.Frame(root)
# #         self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
# #
# #         self.right_frame = tk.Frame(root)
# #         self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
# #
# #         # Video labels (top and bottom)
# #         self.video_label1 = tk.Label(self.left_frame)
# #         self.video_label1.pack(side=tk.TOP, anchor="center")
# #
# #         self.video_label2 = tk.Label(self.left_frame)
# #         self.video_label2.pack(side=tk.TOP, anchor="center")
# #
# #         # Initialize VideoPlayers
# #         self.player1 = VideoPlayer(video_path1, self.video_label1, scale_factor)
# #         self.player2 = VideoPlayer(video_path2, self.video_label2, scale_factor)
# #
# #         # Synchronized playback
# #         self.total_frames = min(self.player1.total_frames, self.player2.total_frames)
# #         self.fps = self.player1.fps
# #         self.current_frame = 0
# #         self.playing = False
# #
# #         # Playback controls (in the right_frame)
# #         self.play_button = tk.Button(
# #             self.right_frame,
# #             text="Play",
# #             command=self.play,
# #             font=BTN_FONT,
# #             width=10,
# #             height=2
# #         )
# #         self.play_button.grid(row=0, column=0, padx=5, pady=5)
# #
# #         self.pause_button = tk.Button(
# #             self.right_frame,
# #             text="Pause",
# #             command=self.pause,
# #             font=BTN_FONT,
# #             width=10,
# #             height=2
# #         )
# #         self.pause_button.grid(row=1, column=0, padx=5, pady=5)
# #
# #         self.forward_button = tk.Button(
# #             self.right_frame,
# #             text="Next Frame",
# #             command=self.next_frame,
# #             font=BTN_FONT,
# #             width=10,
# #             height=2
# #         )
# #         self.forward_button.grid(row=2, column=0, padx=5, pady=5)
# #
# #         self.backward_button = tk.Button(
# #             self.right_frame,
# #             text="Previous Frame",
# #             command=self.previous_frame,
# #             font=BTN_FONT,
# #             width=10,
# #             height=2
# #         )
# #         self.backward_button.grid(row=3, column=0, padx=5, pady=5)
# #
# #         # Slider
# #         self.slider = tk.Scale(
# #             self.right_frame,
# #             from_=0,
# #             to=self.total_frames - 1,
# #             orient=tk.HORIZONTAL,
# #             length=SLIDER_LENGTH,
# #             command=self.slider_jump,
# #             font=BTN_FONT
# #         )
# #         self.slider.grid(row=4, column=0, padx=5, pady=10)
# #
# #         # Annotation controls below the slider
# #         self.annotation_frame = tk.Frame(self.right_frame)
# #         self.annotation_frame.grid(row=5, column=0, pady=10)
# #         self.annotation_manager = AnnotationManager(self.annotation_frame, self.get_current_time, video_path1)
# #
# #         # Display the first frame
# #         self.update_frames(self.current_frame)
# #
# #     def get_video_dimensions(self, path):
# #         cap = cv2.VideoCapture(path)
# #         if not cap.isOpened():
# #             print(f"Warning: Could not open {path}. Using default (640x480).")
# #             return 640, 480
# #         ret, frame = cap.read()
# #         cap.release()
# #         if not ret:
# #             print(f"Warning: Could not read first frame of {path}. Using default (640x480).")
# #             return 640, 480
# #         h, w = frame.shape[:2]
# #         return w, h
# #
# #     def update_frames(self, frame_index):
# #         self.player1.show_frame(frame_index)
# #         self.player2.show_frame(frame_index)
# #         self.slider.set(frame_index)
# #
# #     def get_current_time(self):
# #         return self.current_frame / self.fps
# #
# #     def play(self):
# #         self.playing = True
# #         self.play_loop()
# #
# #     def play_loop(self):
# #         if self.playing:
# #             if self.current_frame < self.total_frames - 1:
# #                 self.current_frame += 1
# #                 self.update_frames(self.current_frame)
# #                 delay = int(1000 / self.fps)
# #                 self.root.after(delay, self.play_loop)
# #             else:
# #                 self.playing = False
# #
# #     def pause(self):
# #         self.playing = False
# #
# #     def next_frame(self):
# #         self.pause()
# #         if self.current_frame < self.total_frames - 1:
# #             self.current_frame += 1
# #             self.update_frames(self.current_frame)
# #
# #     def previous_frame(self):
# #         self.pause()
# #         if self.current_frame > 0:
# #             self.current_frame -= 1
# #             self.update_frames(self.current_frame)
# #
# #     def slider_jump(self, value):
# #         self.current_frame = int(value)
# #         self.update_frames(self.current_frame)
# #
# #     def on_close(self):
# #         self.player1.release()
# #         self.player2.release()
# #         self.root.destroy()
# #
# # if __name__ == "__main__":
# #     if len(sys.argv) < 3:
# #         print("Usage: python dual_video_annotation.py video1 video2")
# #         sys.exit(1)
# #
# #     video_path1 = sys.argv[1]
# #     video_path2 = sys.argv[2]
# #
# #     root = tk.Tk()
# #     app = MainApp(root, video_path1, video_path2)
# #     root.protocol("WM_DELETE_WINDOW", app.on_close)
# #     root.mainloop()
#
#
# import tkinter as tk
# from tkinter import ttk
# import cv2
# from PIL import Image, ImageTk
# import json
# import csv
# import os
# from pathlib import Path
# import sys
#
# BTN_FONT = ("Helvetica", 14, "bold")
# SLIDER_LENGTH = 300
#
# # How many seconds to jump when user clicks Forward/Backward
# JUMP_SECONDS = 2
#
# class VideoPlayer:
#     """
#     Loads a video file, handles frame reading, scaling, and displaying on a Tkinter Label.
#     Scale factor can be updated dynamically (e.g., during window resizing).
#     """
#     def __init__(self, video_path, widget, orig_width, orig_height):
#         """
#         :param video_path: Path to the video file.
#         :param widget: Tkinter Label where the frames will be displayed.
#         :param orig_width: Original width (pixels) of the video’s first frame.
#         :param orig_height: Original height (pixels) of the video’s first frame.
#         """
#         self.video_path = video_path
#         self.widget = widget
#         self.cap = cv2.VideoCapture(video_path)
#         if not self.cap.isOpened():
#             raise Exception(f"Cannot open video file: {video_path}")
#
#         self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
#         self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 25  # fallback
#         self.current_frame = 0
#
#         # Store original dimensions (used for dynamic scaling)
#         self.orig_width = orig_width
#         self.orig_height = orig_height
#         self.scale_factor = 1.0  # default scale factor
#         self.photo = None
#
#     def set_scale_factor(self, factor):
#         """
#         Update the scaling factor used when resizing frames.
#         """
#         self.scale_factor = factor
#
#     def show_frame(self, frame_index):
#         """
#         Move to a specific frame index, read it, and display it with current scale factor.
#         """
#         if frame_index < 0:
#             frame_index = 0
#         if frame_index >= self.total_frames:
#             frame_index = self.total_frames - 1
#
#         self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
#         ret, frame = self.cap.read()
#         if not ret:
#             print(f"Warning: Could not read frame {frame_index} from {self.video_path}")
#             return
#
#         self.current_frame = frame_index
#         # Convert BGR -> RGB
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#         # Scale using the current scale_factor
#         new_w = int(self.orig_width * self.scale_factor)
#         new_h = int(self.orig_height * self.scale_factor)
#         if new_w > 0 and new_h > 0:
#             frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
#
#         # Convert to ImageTk
#         im = Image.fromarray(frame)
#         self.photo = ImageTk.PhotoImage(image=im)
#         self.widget.config(image=self.photo)
#
#     def get_current_time(self):
#         """
#         Return current playback time in seconds.
#         """
#         return self.current_frame / self.fps
#
#     def release(self):
#         """
#         Release the video capture resource.
#         """
#         self.cap.release()
#
#
# class AnnotationManager:
#     """
#     Manages annotation logic: reading labels, storing start/end times in memory,
#     and saving to CSV on demand.
#     """
#     def __init__(self, parent, time_callback, video_file):
#         self.parent = parent
#         self.time_callback = time_callback
#         self.annotation_start = None
#         self.annotations = []
#
#         # Load labels from JSON
#         try:
#             with open("labels.json", "r") as f:
#                 self.labels = json.load(f)
#                 if not isinstance(self.labels, list):
#                     raise ValueError("labels.json must contain a JSON array.")
#         except Exception as e:
#             print("Error loading labels.json:", e)
#             self.labels = []
#
#         self.label_var = tk.StringVar()
#         self.combobox = ttk.Combobox(
#             parent, textvariable=self.label_var,
#             values=self.labels, state="readonly",
#             font=BTN_FONT
#         )
#         self.combobox.grid(row=0, column=0, padx=5, pady=5)
#         if self.labels:
#             self.combobox.current(0)
#
#         self.start_button = tk.Button(
#             parent, text="Start of Activity",
#             command=self.start_activity,
#             font=BTN_FONT, width=15, height=2
#         )
#         self.start_button.grid(row=1, column=0, padx=5, pady=5)
#
#         self.end_button = tk.Button(
#             parent, text="End of Activity",
#             command=self.end_activity,
#             font=BTN_FONT, width=15, height=2
#         )
#         self.end_button.grid(row=2, column=0, padx=5, pady=5)
#
#         self.save_button = tk.Button(
#             parent, text="Save Annotations",
#             command=self.save_annotations,
#             font=BTN_FONT, width=15, height=2
#         )
#         self.save_button.grid(row=3, column=0, padx=5, pady=5)
#
#         # Determine CSV file location (two levels above)
#         video_path = Path(video_file)
#         try:
#             csv_folder = video_path.parents[2]
#             csv_folder.mkdir(parents=True, exist_ok=True)
#             self.csv_file = csv_folder / "annotations.csv"
#         except Exception as e:
#             print("Error determining CSV file location:", e)
#             self.csv_file = Path("L1_annotations.csv")
#
#         # If CSV doesn't exist, create it with a header
#         if not self.csv_file.exists():
#             try:
#                 with open(self.csv_file, "w", newline="") as f:
#                     writer = csv.writer(f)
#                     writer.writerow(["Label", "Start Time (s)", "End Time (s)"])
#             except Exception as e:
#                 print("Error creating CSV file:", e)
#
#     def start_activity(self):
#         self.annotation_start = self.time_callback()
#         print("Annotation started at:", self.annotation_start)
#
#     def end_activity(self):
#         if self.annotation_start is None:
#             print("Error: Please press 'Start of Activity' first.")
#             return
#         annotation_end = self.time_callback()
#         label = self.label_var.get()
#         self.annotations.append([label, self.annotation_start, annotation_end])
#         print(f"Annotation in memory: {label}, Start: {self.annotation_start}, End: {annotation_end}")
#         self.annotation_start = None
#
#     def save_annotations(self):
#         if not self.annotations:
#             print("No annotations to save.")
#             return
#         try:
#             with open(self.csv_file, "a", newline="") as f:
#                 writer = csv.writer(f)
#                 for ann in self.annotations:
#                     writer.writerow(ann)
#             print(f"Saved {len(self.annotations)} annotations to {self.csv_file}")
#             self.annotations.clear()
#         except Exception as e:
#             print("Error writing annotation to CSV:", e)
#
#
# class MainApp:
#     """
#     Main application with two videos stacked vertically on the left,
#     controls on the right, and dynamic resizing.
#     """
#     def __init__(self, root, video_path1, video_path2):
#         self.root = root
#         self.root.title("Video Annotation")
#         self._resize_after_id = None  # for debouncing resize events
#
#         # Read the first frame of each video to get original dimensions
#         w1, h1 = self.get_video_dimensions(video_path1)
#         w2, h2 = self.get_video_dimensions(video_path2)
#
#         # Create frames: left for videos (stacked), right for controls
#         self.left_frame = tk.Frame(root, bd=2, relief=tk.RAISED)
#         self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#
#         self.right_frame = tk.Frame(root, bd=2, relief=tk.RIDGE)
#         self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
#
#         # Video labels (top / bottom)
#         self.video_label1 = tk.Label(self.left_frame)
#         self.video_label1.pack(side=tk.TOP, anchor="center")
#
#         self.video_label2 = tk.Label(self.left_frame)
#         self.video_label2.pack(side=tk.TOP, anchor="center")
#
#         # Video players
#         self.player1 = VideoPlayer(video_path1, self.video_label1, w1, h1)
#         self.player2 = VideoPlayer(video_path2, self.video_label2, w2, h2)
#
#         # Determine min total frames (for sync)
#         self.total_frames = min(self.player1.total_frames, self.player2.total_frames)
#         self.fps = self.player1.fps
#         self.current_frame = 0
#         self.playing = False
#
#         # Playback controls
#         self.play_button = tk.Button(
#             self.right_frame, text="Play",
#             command=self.play, font=BTN_FONT,
#             width=12, height=2
#         )
#         self.play_button.grid(row=0, column=0, padx=5, pady=5)
#
#         self.pause_button = tk.Button(
#             self.right_frame, text="Pause",
#             command=self.pause, font=BTN_FONT,
#             width=12, height=2
#         )
#         self.pause_button.grid(row=1, column=0, padx=5, pady=5)
#
#         # Forward/Backward 5s
#         self.forward_button = tk.Button(
#             self.right_frame, text="Forward 5s",
#             command=self.forward_s, font=BTN_FONT,
#             width=12, height=2
#         )
#         self.forward_button.grid(row=2, column=0, padx=5, pady=5)
#
#         self.backward_button = tk.Button(
#             self.right_frame, text="Backward 2s",
#             command=self.backward_s, font=BTN_FONT,
#             width=12, height=2
#         )
#         self.backward_button.grid(row=3, column=0, padx=5, pady=5)
#
#         # Slider
#         self.slider = tk.Scale(
#             self.right_frame, from_=0, to=self.total_frames - 1,
#             orient=tk.HORIZONTAL, length=SLIDER_LENGTH,
#             command=self.slider_jump, font=BTN_FONT
#         )
#         self.slider.grid(row=4, column=0, padx=5, pady=10)
#
#         # Annotation manager
#         self.annotation_frame = tk.Frame(self.right_frame)
#         self.annotation_frame.grid(row=5, column=0, pady=10)
#         self.annotation_manager = AnnotationManager(self.annotation_frame, self.get_current_time, video_path1)
#
#         # Display first frame
#         self.update_frames(self.current_frame)
#
#         # Bind window resize event to recalc layout
#         self.root.bind("<Configure>", self.on_resize)
#
#     def get_video_dimensions(self, path):
#         """
#         Read the first frame to get (width, height). Fallback to (640, 480) if it fails.
#         """
#         cap = cv2.VideoCapture(path)
#         if not cap.isOpened():
#             print(f"Warning: Could not open {path}. Using default (640x480).")
#             return (640, 480)
#         ret, frame = cap.read()
#         cap.release()
#         if not ret:
#             print(f"Warning: Could not read first frame of {path}. Using default (640x480).")
#             return (640, 480)
#         h, w = frame.shape[:2]
#         return (w, h)
#
#     def on_resize(self, event):
#         """
#         Called whenever the window is resized. We'll debounce it with a small after() delay
#         to avoid flickering from continuous events.
#         """
#         # Only run if it's the root window's event (avoid child frame recursion)
#         if event.widget != self.root:
#             return
#
#         # Cancel any pending resize callback
#         if self._resize_after_id is not None:
#             self.root.after_cancel(self._resize_after_id)
#         # Schedule a new resize callback in 200ms
#         self._resize_after_id = self.root.after(200, self.apply_resize)
#
#     def apply_resize(self):
#         """
#         Actually recalculate the scale factors based on the left_frame size,
#         then update the current frames for both videos.
#         """
#         self._resize_after_id = None
#         left_w = self.left_frame.winfo_width()
#         left_h = self.left_frame.winfo_height()
#         if left_w < 10 or left_h < 10:
#             # Window might be minimized or too small
#             return
#
#         # We have two videos stacked: total original width = max(w1, w2), total original height = h1 + h2
#         w1, h1 = self.player1.orig_width, self.player1.orig_height
#         w2, h2 = self.player2.orig_width, self.player2.orig_height
#         combined_width = max(w1, w2)
#         combined_height = h1 + h2
#
#         # Scale factor so the stacked videos fit in (left_w x left_h)
#         scale_w = left_w / float(combined_width)
#         scale_h = left_h / float(combined_height)
#         scale_factor = min(scale_w, scale_h, 1.0)  # do not upscale beyond 1.0
#
#         # Update both players
#         self.player1.set_scale_factor(scale_factor)
#         self.player2.set_scale_factor(scale_factor)
#
#         # Redraw current frame
#         self.update_frames(self.current_frame)
#
#     def update_frames(self, frame_index):
#         self.player1.show_frame(frame_index)
#         self.player2.show_frame(frame_index)
#         self.slider.set(frame_index)
#
#     def get_current_time(self):
#         return self.current_frame / self.fps
#
#     def play(self):
#         self.playing = True
#         self.play_loop()
#
#     def play_loop(self):
#         if self.playing:
#             if self.current_frame < self.total_frames - 1:
#                 self.current_frame += 1
#                 self.update_frames(self.current_frame)
#                 delay = 1 #int(100 / self.fps)
#                 self.root.after(delay, self.play_loop)
#             else:
#                 self.playing = False
#
#     def pause(self):
#         self.playing = False
#
#     def forward_s(self):
#         self.pause()
#         frames_to_jump = int(JUMP_SECONDS * self.fps)
#         new_frame = self.current_frame + frames_to_jump
#         if new_frame >= self.total_frames:
#             new_frame = self.total_frames - 1
#         self.current_frame = new_frame
#         self.update_frames(self.current_frame)
#
#     def backward_s(self):
#         self.pause()
#         frames_to_jump = int((JUMP_SECONDS/2) * self.fps)
#         new_frame = self.current_frame - frames_to_jump
#         if new_frame < 0:
#             new_frame = 0
#         self.current_frame = new_frame
#         self.update_frames(self.current_frame)
#
#     def slider_jump(self, value):
#         self.current_frame = int(value)
#         self.update_frames(self.current_frame)
#
#     def on_close(self):
#         self.player1.release()
#         self.player2.release()
#         self.root.quit()
#         self.root.destroy()
#
#
# def main():
#     if len(sys.argv) < 3:
#         print("Run python video_annotation.py path_to_video1 path_to_video2")
#         sys.exit(1)
#
#     video_path1 = sys.argv[1]
#     video_path2 = sys.argv[2]
#
#     root = tk.Tk()
#     app = MainApp(root, video_path1, video_path2)
#     root.protocol("WM_DELETE_WINDOW", app.on_close)
#     root.mainloop()
#
# if __name__ == "__main__":
#     main()

import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import json
import csv
import os
from pathlib import Path
import sys

BTN_FONT = ("Helvetica", 14, "bold")
STATUS_FONT = ("Helvetica", 12, "bold")
SLIDER_LENGTH = 300

# How many seconds to jump when user clicks Forward/Backward
JUMP_SECONDS = 2

# Colors for status indicators
RECORDING_COLOR = "#ffcccc"  # Light red
IDLE_COLOR = "#ccffcc"  # Light green
SPEED_NORMAL_COLOR = "#e0e0e0"  # Light gray
SPEED_FAST_COLOR = "#ffe0b0"  # Light orange
SPEED_FASTER_COLOR = "#ffcc80"  # Deeper orange
SPEED_FASTEST_COLOR = "#ff9966"  # Almost red-orange

# Available playback speeds
SPEEDS = [1, 2, 5, 10]
SPEED_COLORS = [SPEED_NORMAL_COLOR, SPEED_FAST_COLOR, SPEED_FASTER_COLOR, SPEED_FASTEST_COLOR]


class VideoPlayer:
    """
    Loads a video file, handles frame reading, scaling, and displaying on a Tkinter Label.
    Scale factor can be updated dynamically (e.g., during window resizing).
    """

    def __init__(self, video_path, widget, orig_width, orig_height):
        """
        :param video_path: Path to the video file.
        :param widget: Tkinter Label where the frames will be displayed.
        :param orig_width: Original width (pixels) of the video's first frame.
        :param orig_height: Original height (pixels) of the video's first frame.
        """
        self.video_path = video_path
        self.widget = widget

        # Check if file exists before trying to open it
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise Exception(f"Cannot open video file: {video_path}")

        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 25  # fallback
        self.current_frame = 0

        # Store original dimensions (used for dynamic scaling)
        self.orig_width = orig_width
        self.orig_height = orig_height
        self.scale_factor = 1.0  # default scale factor
        self.photo = None

        # Store last valid frame for when we're past the end
        self.last_valid_frame = None

    def set_scale_factor(self, factor):
        """
        Update the scaling factor used when resizing frames.
        """
        self.scale_factor = factor

    def show_frame(self, frame_index):
        """
        Move to a specific frame index, read it, and display it with current scale factor.
        """
        # If frame index is beyond our total frames, show the last frame
        if frame_index >= self.total_frames:
            if self.last_valid_frame is not None:
                # Use the stored last valid frame
                frame = self.last_valid_frame.copy()
            else:
                # Try to get the last frame
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.total_frames - 1)
                ret, frame = self.cap.read()
                if not ret:
                    print(f"Warning: Could not read last frame from {self.video_path}")
                    return
                self.last_valid_frame = frame.copy()
        else:
            # Normal case - requested frame is within range
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame = self.cap.read()
            if not ret:
                print(f"Warning: Could not read frame {frame_index} from {self.video_path}")
                return

        self.current_frame = min(frame_index, self.total_frames - 1)

        # Convert BGR -> RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Scale using the current scale_factor
        new_w = int(self.orig_width * self.scale_factor)
        new_h = int(self.orig_height * self.scale_factor)
        if new_w > 0 and new_h > 0:
            frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)

        # Convert to ImageTk
        im = Image.fromarray(frame)
        self.photo = ImageTk.PhotoImage(image=im)
        self.widget.config(image=self.photo)

    def get_current_time(self):
        """
        Return current playback time in seconds.
        """
        return self.current_frame / self.fps

    def release(self):
        """
        Release the video capture resource.
        """
        self.cap.release()


class AnnotationManager:
    """
    Manages annotation logic: reading labels, storing start/end times in memory,
    and saving to CSV on demand.
    """

    def __init__(self, parent, time_callback, video_file):
        self.parent = parent
        self.time_callback = time_callback
        self.annotation_start = None
        self.annotations = []

        # For updating status during recording
        self._status_update_id = None

        # Load labels from JSON
        try:
            with open("labels.json", "r") as f:
                self.labels = json.load(f)
                if not isinstance(self.labels, list):
                    raise ValueError("labels.json must contain a JSON array.")
        except Exception as e:
            print("Error loading labels.json:", e)
            self.labels = []

        self.label_var = tk.StringVar()
        self.combobox = ttk.Combobox(
            parent, textvariable=self.label_var,
            values=self.labels, state="readonly",
            font=BTN_FONT
        )
        self.combobox.grid(row=0, column=0, padx=5, pady=5)
        if self.labels:
            self.combobox.current(0)

        self.start_button = tk.Button(
            parent, text="Start of Activity",
            command=self.start_activity,
            font=BTN_FONT, width=15, height=2
        )
        self.start_button.grid(row=1, column=0, padx=5, pady=5)

        self.end_button = tk.Button(
            parent, text="End of Activity",
            command=self.end_activity,
            font=BTN_FONT, width=15, height=2
        )
        self.end_button.grid(row=2, column=0, padx=5, pady=5)

        self.save_button = tk.Button(
            parent, text="Save Annotations",
            command=self.save_annotations,
            font=BTN_FONT, width=15, height=2
        )
        self.save_button.grid(row=3, column=0, padx=5, pady=5)

        # Add status frame to show current annotation activity
        self.status_frame = tk.Frame(parent, bd=2, relief=tk.SUNKEN, padx=5, pady=5)
        self.status_frame.grid(row=4, column=0, padx=5, pady=10, sticky="ew")

        # Status label header
        self.status_header = tk.Label(
            self.status_frame,
            text="Annotation Status:",
            font=STATUS_FONT
        )
        self.status_header.pack(anchor="w")

        # Status indicator label
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready - No Active Recording",
            font=STATUS_FONT,
            bg=IDLE_COLOR,
            width=25,
            height=2,
            anchor="w",
            padx=10
        )
        self.status_label.pack(fill="x", pady=5)

        # Time info label
        self.time_info = tk.Label(
            self.status_frame,
            text="",
            font=STATUS_FONT,
            anchor="w"
        )
        self.time_info.pack(fill="x")

        # Determine CSV file location (two levels above)
        video_path = Path(video_file)
        try:
            csv_folder = video_path.parents[2]
            csv_folder.mkdir(parents=True, exist_ok=True)
            self.csv_file = csv_folder / "annotations.csv"
        except Exception as e:
            print("Error determining CSV file location:", e)
            self.csv_file = Path("L1_annotations.csv")

        # If CSV doesn't exist, create it with a header
        if not self.csv_file.exists():
            try:
                with open(self.csv_file, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Label", "Start Time (s)", "End Time (s)"])
            except Exception as e:
                print("Error creating CSV file:", e)

    def start_activity(self):
        self.annotation_start = self.time_callback()
        print("Annotation started at:", self.annotation_start)

        # Update status to show recording
        current_label = self.label_var.get()
        self.status_label.config(
            text=f"RECORDING: {current_label}",
            bg=RECORDING_COLOR
        )

        # Start periodic updates of the time info
        self._update_time_info()

    def _update_time_info(self):
        """Update the time information during recording"""
        if self.annotation_start is not None:
            current_time = self.time_callback()
            duration = current_time - self.annotation_start
            self.time_info.config(
                text=f"Start: {self.annotation_start:.2f}s | Current: {current_time:.2f}s | Duration: {duration:.2f}s"
            )
            # Schedule next update (10 times per second)
            self._status_update_id = self.parent.after(100, self._update_time_info)
        else:
            # Clear time info when not recording
            self.time_info.config(text="")

    def end_activity(self):
        if self.annotation_start is None:
            print("Error: Please press 'Start of Activity' first.")
            return

        # Cancel any pending time updates
        if self._status_update_id is not None:
            self.parent.after_cancel(self._status_update_id)
            self._status_update_id = None

        annotation_end = self.time_callback()
        label = self.label_var.get()
        duration = annotation_end - self.annotation_start
        self.annotations.append([label, self.annotation_start, annotation_end])

        # Update status to show the segment was captured
        self.status_label.config(
            text=f"Captured: {label} ({duration:.2f}s)",
            bg=IDLE_COLOR
        )
        self.time_info.config(
            text=f"From {self.annotation_start:.2f}s to {annotation_end:.2f}s"
        )

        print(f"Annotation in memory: {label}, Start: {self.annotation_start}, End: {annotation_end}")
        self.annotation_start = None

    def save_annotations(self):
        if not self.annotations:
            print("No annotations to save.")
            self.status_label.config(text="No annotations to save")
            return
        try:
            with open(self.csv_file, "a", newline="") as f:
                writer = csv.writer(f)
                for ann in self.annotations:
                    writer.writerow(ann)

            self.status_label.config(
                text=f"Saved {len(self.annotations)} annotations",
                bg=IDLE_COLOR
            )
            self.time_info.config(text=f"to {self.csv_file}")

            print(f"Saved {len(self.annotations)} annotations to {self.csv_file}")
            self.annotations.clear()
        except Exception as e:
            print("Error writing annotation to CSV:", e)
            self.status_label.config(text=f"Error: {str(e)[:30]}...")


class MainApp:
    """
    Main application with one or two videos stacked vertically on the left,
    controls on the right, and dynamic resizing.
    """

    def __init__(self, root, video_path1, video_path2=None):
        self.root = root
        self.root.title("Video Annotation")
        self._resize_after_id = None  # for debouncing resize events

        # Speed control - index into the SPEEDS array
        self.speed_index = 0

        # Flag to track if we have one or two videos
        self.dual_video_mode = video_path2 is not None

        # Read the first frame of each video to get original dimensions
        w1, h1 = self.get_video_dimensions(video_path1)
        w2, h2 = (0, 0) if not self.dual_video_mode else self.get_video_dimensions(video_path2)

        # Create frames: left for videos (stacked), right for controls
        self.left_frame = tk.Frame(root, bd=2, relief=tk.RAISED)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(root, bd=2, relief=tk.RIDGE)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Video labels (top / bottom)
        self.video_label1 = tk.Label(self.left_frame)
        self.video_label1.pack(side=tk.TOP, anchor="center")

        # Initialize player1
        self.player1 = VideoPlayer(video_path1, self.video_label1, w1, h1)

        # Initialize player2 only if we have a second video
        self.player2 = None
        if self.dual_video_mode:
            self.video_label2 = tk.Label(self.left_frame)
            self.video_label2.pack(side=tk.TOP, anchor="center")
            self.player2 = VideoPlayer(video_path2, self.video_label2, w2, h2)

        # Determine total frames based on the longer video
        if self.dual_video_mode:
            self.total_frames = max(self.player1.total_frames, self.player2.total_frames)
        else:
            self.total_frames = self.player1.total_frames

        self.fps = self.player1.fps
        self.current_frame = 0
        self.playing = False
        self._play_loop_id = None

        # Create a frame for playback controls
        self.controls_frame = tk.Frame(self.right_frame)
        self.controls_frame.grid(row=0, column=0, pady=5)

        # Playback controls - use the controls_frame as parent
        self.play_button = tk.Button(
            self.controls_frame, text="Play",
            command=self.play, font=BTN_FONT,
            width=12, height=2
        )
        self.play_button.grid(row=0, column=0, padx=5, pady=5)

        self.pause_button = tk.Button(
            self.controls_frame, text="Pause",
            command=self.pause, font=BTN_FONT,
            width=12, height=2
        )
        self.pause_button.grid(row=0, column=1, padx=5, pady=5)

        # Speed toggle button - cycles through speeds
        self.speed_button = tk.Button(
            self.controls_frame, text=f"{SPEEDS[self.speed_index]}x Speed",
            command=self.toggle_speed, font=BTN_FONT,
            width=10, height=2,
            bg=SPEED_COLORS[self.speed_index]
        )
        self.speed_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        # Forward/Backward buttons
        self.forward_button = tk.Button(
            self.right_frame, text="Forward 5s",
            command=self.forward_s, font=BTN_FONT,
            width=12, height=2
        )
        self.forward_button.grid(row=1, column=0, padx=5, pady=5)

        self.backward_button = tk.Button(
            self.right_frame, text="Backward 2s",
            command=self.backward_s, font=BTN_FONT,
            width=12, height=2
        )
        self.backward_button.grid(row=2, column=0, padx=5, pady=5)

        # Slider
        self.slider = tk.Scale(
            self.right_frame, from_=0, to=self.total_frames - 1,
            orient=tk.HORIZONTAL, length=SLIDER_LENGTH,
            command=self.slider_jump, font=BTN_FONT
        )
        self.slider.grid(row=3, column=0, padx=5, pady=10)

        # Annotation manager
        self.annotation_frame = tk.Frame(self.right_frame)
        self.annotation_frame.grid(row=4, column=0, pady=10)
        self.annotation_manager = AnnotationManager(self.annotation_frame, self.get_current_time, video_path1)

        # Display first frame
        self.update_frames(self.current_frame)

        # Bind window resize event to recalc layout
        self.root.bind("<Configure>", self.on_resize)

    def toggle_speed(self):
        """Cycle through available playback speeds: 1x, 2x, 5x, 10x"""
        # Increment speed index and wrap around if needed
        self.speed_index = (self.speed_index + 1) % len(SPEEDS)

        # Update button appearance
        self.speed_button.config(
            text=f"{SPEEDS[self.speed_index]}x Speed",
            bg=SPEED_COLORS[self.speed_index]
        )

        # If we're currently playing, restart playback with new speed
        if self.playing and self._play_loop_id is not None:
            self.root.after_cancel(self._play_loop_id)
            self.play_loop()

    def get_video_dimensions(self, path):
        """
        Read the first frame to get (width, height). Fallback to (640, 480) if it fails.
        """
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            print(f"Warning: Could not open {path}. Using default (640x480).")
            return (640, 480)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            print(f"Warning: Could not read first frame of {path}. Using default (640x480).")
            return (640, 480)
        h, w = frame.shape[:2]
        return (w, h)

    def on_resize(self, event):
        """
        Called whenever the window is resized. We'll debounce it with a small after() delay
        to avoid flickering from continuous events.
        """
        # Only run if it's the root window's event (avoid child frame recursion)
        if event.widget != self.root:
            return

        # Cancel any pending resize callback
        if self._resize_after_id is not None:
            self.root.after_cancel(self._resize_after_id)
        # Schedule a new resize callback in 200ms
        self._resize_after_id = self.root.after(200, self.apply_resize)

    def apply_resize(self):
        """
        Actually recalculate the scale factors based on the left_frame size,
        then update the current frames for both videos.
        """
        self._resize_after_id = None
        left_w = self.left_frame.winfo_width()
        left_h = self.left_frame.winfo_height()
        if left_w < 10 or left_h < 10:
            # Window might be minimized or too small
            return

        if self.dual_video_mode:
            # We have two videos stacked: total original width = max(w1, w2), total original height = h1 + h2
            w1, h1 = self.player1.orig_width, self.player1.orig_height
            w2, h2 = self.player2.orig_width, self.player2.orig_height
            combined_width = max(w1, w2)
            combined_height = h1 + h2
        else:
            # Single video mode
            combined_width = self.player1.orig_width
            combined_height = self.player1.orig_height

        # Scale factor so the stacked videos fit in (left_w x left_h)
        scale_w = left_w / float(combined_width)
        scale_h = left_h / float(combined_height)
        scale_factor = min(scale_w, scale_h, 1.0)  # do not upscale beyond 1.0

        # Update player(s)
        self.player1.set_scale_factor(scale_factor)
        if self.dual_video_mode:
            self.player2.set_scale_factor(scale_factor)

        # Redraw current frame
        self.update_frames(self.current_frame)

    def update_frames(self, frame_index):
        """
        Update the displayed frame for one or both videos
        """
        self.player1.show_frame(frame_index)
        if self.dual_video_mode:
            self.player2.show_frame(frame_index)
        self.slider.set(frame_index)

    def get_current_time(self):
        return self.current_frame / self.fps

    def play(self):
        self.playing = True
        self.play_loop()

    def play_loop(self):
        if self.playing:
            if self.current_frame < self.total_frames - 1:
                # Get current speed multiplier from the SPEEDS array
                speed = SPEEDS[self.speed_index]

                # Calculate next frame based on speed
                frames_to_advance = speed
                next_frame = min(self.current_frame + frames_to_advance, self.total_frames - 1)

                self.current_frame = next_frame
                self.update_frames(self.current_frame)

                # Always use a consistent delay for UI responsiveness
                # Higher speeds advance more frames per tick
                delay = 1
                self._play_loop_id = self.root.after(delay, self.play_loop)
            else:
                self.playing = False
                self._play_loop_id = None

    def pause(self):
        self.playing = False
        if self._play_loop_id is not None:
            self.root.after_cancel(self._play_loop_id)
            self._play_loop_id = None

    def forward_s(self):
        self.pause()
        frames_to_jump = int(JUMP_SECONDS * self.fps)
        new_frame = self.current_frame + frames_to_jump
        if new_frame >= self.total_frames:
            new_frame = self.total_frames - 1
        self.current_frame = new_frame
        self.update_frames(self.current_frame)

    def backward_s(self):
        self.pause()
        frames_to_jump = int((JUMP_SECONDS / 2) * self.fps)
        new_frame = self.current_frame - frames_to_jump
        if new_frame < 0:
            new_frame = 0
        self.current_frame = new_frame
        self.update_frames(self.current_frame)

    def slider_jump(self, value):
        self.current_frame = int(value)
        self.update_frames(self.current_frame)

    def on_close(self):
        if self._play_loop_id is not None:
            self.root.after_cancel(self._play_loop_id)
        self.player1.release()
        if self.dual_video_mode:
            self.player2.release()
        self.root.quit()
        self.root.destroy()


def main():
    # Check if we have one or two video paths
    if len(sys.argv) < 2:
        print("Run python video_annotation.py path_to_video1 [path_to_video2]")
        sys.exit(1)

    # Clean up input paths by stripping whitespace
    video_path1 = sys.argv[1].strip()
    video_path2 = None if len(sys.argv) < 3 else sys.argv[2].strip()

    # Check if the first path exists
    if not os.path.exists(video_path1):
        print(f"Error: Video file not found: {video_path1}")
        print(f"Please check that the file exists and the path is correct.")
        sys.exit(1)

    # Check the second path if provided
    if video_path2 and not os.path.exists(video_path2):
        print(f"Error: Second video file not found: {video_path2}")
        print(f"Running with just the first video.")
        video_path2 = None

    # Create the GUI
    try:
        root = tk.Tk()
        app = MainApp(root, video_path1, video_path2)
        root.protocol("WM_DELETE_WINDOW", app.on_close)
        root.mainloop()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        if 'root' in locals():
            messagebox.showerror("File Not Found", str(e))
            root.destroy()
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if 'root' in locals():
            messagebox.showerror("Error", str(e))
            root.destroy()
        sys.exit(1)


if __name__ == "__main__":
    main()