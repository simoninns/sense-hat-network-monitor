#************************************************************************
#
#   drawface.py
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

# This class creates a face for use with the sense hat 8x8 RGB display.
# The eyes, mouth and overall colour can be set and a display-ready
# frame is returned containing the required tuples for set_pixels()

# Import the required libraries
from enum import Enum

# Enumeration for the type of mouth displayed
class Mouth_type(Enum):
    normal = 1
    smile = 2
    sad = 3
    shocked = 4

# Enumeration for the direction of the eyes
class Eye_direction(Enum):
    left = 1
    right = 2
    down_left = 3
    down_right = 4
    up_left = 5
    up_right = 6

# Enumeration for the pixel colours
class Face_colour(Enum):
    black = 0
    white = 1
    red = 2
    green = 3
    blue = 4
    yellow = 5
    cyan = 6
    magenta = 7

# Method to make a face frame
def make_face(mouth_type, eye_direction, face_colour):
    e = (0,0,0)  # empty/black
    c = (0,0,0)
    if face_colour == Face_colour.black:   c = (0,0,0)
    if face_colour == Face_colour.white:   c = (255,255,255)
    if face_colour == Face_colour.red:     c = (255,0,0)
    if face_colour == Face_colour.green:   c = (0,255,0)
    if face_colour == Face_colour.blue:    c = (0,0,255)
    if face_colour == Face_colour.yellow:  c = (255,255,0)
    if face_colour == Face_colour.cyan:    c = (0,255,255)
    if face_colour == Face_colour.magenta: c = (255,0,255)

    # Face is made up of 3 lines of eyes, 2 lines of nose and 3 lines of mouth

    eyes_left = [
        e, e, e, e, e, e, e, e,
        e, c, c, e, e, c, c, e,
        e, c, e, e, e, c, e, e,
    ]

    eyes_right = [
        e, e, e, e, e, e, e, e,
        e, c, c, e, e, c, c, e,
        e, e, c, e, e, e, c, e,
    ]

    eyes_down_left = [
        e, e, e, e, e, e, e, e,
        e, e, e, e, e, e, e, e,
        e, c, e, e, e, c, e, e,
    ]

    eyes_down_right = [
        e, e, e, e, e, e, e, e,
        e, e, e, e, e, e, e, e,
        e, e, c, e, e, e, c, e,
    ]

    eyes_up_left = [
        e, e, e, e, e, e, e, e,
        e, c, e, e, e, c, e, e,
        e, e, e, e, e, e, e, e,
    ]

    eyes_up_right = [
        e, e, e, e, e, e, e, e,
        e, e, c, e, e, e, c, e,
        e, e, e, e, e, e, e, e,
    ]

    nose = [
        e, e, e, e, e, e, e, e,
        e, e, e, e, e, e, e, e,
    ]

    mouth_smile = [
        e, c, e, e, e, e, c, e,
        e, c, c, c, c, c, c, e,
        e, e, e, e, e, e, e, e,
    ]

    mouth_normal = [
        e, e, e, e, e, e, e, e,
        e, c, c, c, c, c, c, e,
        e, e, e, e, e, e, e, e,
    ]

    mouth_sad = [
        e, c, c, c, c, c, c, e,
        e, c, e, e, e, e, c, e,
        e, e, e, e, e, e, e, e,
    ]

    mouth_shocked = [
        e, c, e, c, e, c, e, e,
        e, e, c, e, c, e, c, e,
        e, e, e, e, e, e, e, e,
    ]

    # Select the required eyes
    eye_pixels = eyes_left
    if eye_direction == Eye_direction.right:
        eye_pixels = eyes_right
    elif eye_direction == Eye_direction.down_left:
        eye_pixels = eyes_down_left
    elif eye_direction == Eye_direction.down_right:
        eye_pixels = eyes_down_right
    elif eye_direction == Eye_direction.up_left:
        eye_pixels = eyes_up_left
    elif eye_direction == Eye_direction.up_right:
        eye_pixels = eyes_up_right

    # Select the required nose
    nose_pixels = nose

    # Select the required mouth
    mouth_pixels = mouth_normal
    if mouth_type == Mouth_type.smile:
        mouth_pixels = mouth_smile
    elif mouth_type == Mouth_type.sad:
        mouth_pixels = mouth_sad
    elif mouth_type == Mouth_type.shocked:
        mouth_pixels = mouth_shocked

    face = eye_pixels + nose_pixels + mouth_pixels

    # Return the required face frame
    return face