#************************************************************************
#
#   sensehatanimate.py
#
#   Sense Hat based remote server monitor
#   Copyright (C) 2019 Simon Inns
#
#   This program is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#   Email: simon.inns@gmail.com
#
#************************************************************************/

# This class extends the sense hat class to support animation.
# Frames to be animated can be added and then the animation
# can be started at the required frame rate and then stopped.

# Import the sense hat and other required libraries
from sensehatfader import SenseHatFader
from time import sleep
import threading

# Define a class of SenseHatAnimate inheriting from SenseHatFader
class SenseHatAnimate(SenseHatFader):
    def __init__(self):
        # Initialise the inherited sense hat fader class
        super().__init__()

        # Default settings
        self.show_animation = False
        self.fps = 0.5
        self.current_frame = 0
        self.frames = []

        # Start the animation thread
        self.abort = False
        self.x = threading.Thread(target=self.__run, daemon=True)
        self.x.start()

    # Method to start the animation
    def start_animation(self, frames_per_second):
        if len(self.frames) > 0:
            self.set_animation_speed(frames_per_second)
            self.show_animation = True

    # Method to set the FPS rate of the animation
    def set_animation_speed(self, frames_per_second):
        self.fps = 1.0 / frames_per_second

    # Clear the current animation
    def clear_animation(self):
        # Stop the animation
        self.show_animation = False
        self.fps = 0.5

        # Remove any existing animation frames
        self.frames.clear()
        self.current_frame = 0
        
        # Clear the display
        super().clear()

    # Method to add a new frame to the animation
    def add_animation_frame(self, frame):
        self.frames.append(frame)
        self.current_frame = 0

    # Thread run private method
    def __run(self):
        # Keep running until program quits
        while 1:
            if self.show_animation:
                if len(self.frames) > 0:
                    super().set_pixels(self.frames[self.current_frame])
                    self.current_frame += 1
                    if self.current_frame == len(self.frames):
                        self.current_frame = 0

            # Sleep the thread based on the required FPS rate
            sleep(self.fps)