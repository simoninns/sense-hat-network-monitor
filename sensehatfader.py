#************************************************************************
#
#   sensehatfader.py
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

# This class extends the sense hat to support pixel fading.  When
# a pixel is turned off using the set_pixels method, the class
# fades the pixels to off.  Setting fade_speed controls the speed
# at which the fade happens.

# Import the sense hat and other required libraries
from sense_hat import SenseHat # pylint: disable=import-error
import threading

# Define a class of SenseHatFader inheriting from SenseHat
class SenseHatFader(SenseHat):
    def __init__(self):
        # Initialise the inherited sense hat class
        super().__init__()
        
        # Initialise the local frame store
        e = (0, 0, 0)
        self.target_pixels = [
            e,e,e,e,e,e,e,e,
            e,e,e,e,e,e,e,e,
            e,e,e,e,e,e,e,e,
            e,e,e,e,e,e,e,e,
            e,e,e,e,e,e,e,e,
            e,e,e,e,e,e,e,e,
            e,e,e,e,e,e,e,e,
            e,e,e,e,e,e,e,e,
        ]
        self.current_pixels = self.target_pixels
        super().set_pixels(self.target_pixels)

        # Set the fade speed
        self.fade_speed = 20

        # Set up timer
        timer = threading.Timer(1/60, self._run) # 60 FPS
        timer.daemon = True
        timer.start()

    def _run(self):
        if self.fade_speed > 0:
            # Run through the pixels looking for ones that have been turned off
            # If they have been turned off, fade them down
            for pixel in range(len(self.current_pixels)):
                if self.target_pixels[pixel] == (0,0,0) and self.current_pixels[pixel] != (0,0,0):
                    red, green, blue = self.current_pixels[pixel]

                    red -= self.fade_speed
                    green -= self.fade_speed
                    blue -= self.fade_speed
                    if red < 0: red = 0
                    if green < 0: green = 0
                    if blue < 0: blue = 0
                    self.current_pixels[pixel] = (red, green, blue)
                else:
                    self.current_pixels[pixel] = self.target_pixels[pixel]
        else:
            # Fade speed is 0 - just copy the pixels over
            self.current_pixels[pixel] = self.target_pixels[pixel]

        # Use the base class set_pixels method
        super().set_pixels(self.current_pixels)

        # All done, restart the timer
        timer = threading.Timer(1/60, self._run) # 60 FPS
        timer.daemon = True
        timer.start()

    # Override method to set the display's pixels
    def set_pixels(self, pixels):
        self.target_pixels = pixels

    # Method to set the fade speed (0 = no fade)
    def set_fade_speed(self, speed):
        if speed > 255: speed = 255
        self.fade_speed = speed
