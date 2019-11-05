#************************************************************************
#
#   shnetmon.py
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

# This program monitors Google and Aftonbladet using pings.  If either
# site is down, or both sites are down, it animates different faces on
# the Sense Hat 8x8 RGB display to show the current status.

# Import external libraries
from time import sleep
import os

# Import local libraries
from drawface import make_face
from drawface import Mouth_type
from drawface import Eye_direction
from drawface import Face_colour

from sensehatanimate import SenseHatAnimate

sense_hat = SenseHatAnimate()
sense_hat.rotation = 90

# Function to ping a hostname - requires fping to be installed locally
def ping_server(hostname):
    response = os.system("timeout 0.5 fping --count=1 --timeout=500 --period=20 --quiet --retry=0"
    + " " + hostname + " >/dev/null 2>&1")
    return response

# Function to handle detection of sense hat stick events
# Performs a shutdown if the joystick button is pressed
def check_stick():
    if (event.action == "held" and event.direction == "middle"):
        pre_quit_actions()
        os.system("sudo shutdown -h now")

# Function to perform actions before the program quits
def pre_quit_actions():
    animation_quit()
    sleep(3)
    sense_hat.clear_animation()
    sleep(1)

# Animation to show when both servers are available
def animation_both_servers_up():
    # Create a green smiling face animation

    # Clear the current animation
    sense_hat.clear_animation()

    # Frame 1
    sense_hat.add_animation_frame(make_face(
        Mouth_type.smile, Eye_direction.left, Face_colour.green))

    # Frame 2
    sense_hat.add_animation_frame(make_face(
        Mouth_type.smile, Eye_direction.right, Face_colour.green))

    # Animate at 2 frames per second
    sense_hat.start_animation(2)

# Animation to show when both servers are unavailable
def animation_both_servers_down():
    # Create a red sad face animation

    # Clear the current animation
    sense_hat.clear_animation()

    # Frame 1
    sense_hat.add_animation_frame(make_face(
        Mouth_type.sad, Eye_direction.down_left, Face_colour.red))

    # Frame 2
    sense_hat.add_animation_frame(make_face(
        Mouth_type.sad, Eye_direction.up_left, Face_colour.red))

    # Frame 3
    sense_hat.add_animation_frame(make_face(
        Mouth_type.sad, Eye_direction.up_right, Face_colour.red))

    # Frame 2
    sense_hat.add_animation_frame(make_face(
        Mouth_type.sad, Eye_direction.down_right, Face_colour.red))

    # Animate at 2 frames per second
    sense_hat.start_animation(8)

# Animation to show when only google is unavailable
def animation_google_down():
    # Create a blue normal face animation

    # Clear the current animation
    sense_hat.clear_animation()

    # Frame 1
    sense_hat.add_animation_frame(make_face(
        Mouth_type.normal, Eye_direction.left, Face_colour.blue))

    # Frame 2
    sense_hat.add_animation_frame(make_face(
        Mouth_type.normal, Eye_direction.right, Face_colour.blue))

    # Animate at 2 frames per second
    sense_hat.start_animation(2)

# Animation to show when only aftonbladet is unavailable
def animation_aftonbladet_down():
    # Create a yellow normal face animation

    # Clear the current animation
    sense_hat.clear_animation()

    # Frame 1
    sense_hat.add_animation_frame(make_face(
        Mouth_type.normal, Eye_direction.left, Face_colour.yellow))

    # Frame 2
    sense_hat.add_animation_frame(make_face(
        Mouth_type.normal, Eye_direction.right, Face_colour.yellow))

    # Animate at 2 frames per second
    sense_hat.start_animation(2)

# Animation to show when application is quitting
def animation_quit():
    # Create a magenta shocked face animation

    # Clear the current animation
    sense_hat.clear_animation()

    # Frame 1
    sense_hat.add_animation_frame(make_face(
        Mouth_type.shocked, Eye_direction.left, Face_colour.magenta))

    # Frame 2
    sense_hat.add_animation_frame(make_face(
        Mouth_type.shocked, Eye_direction.right, Face_colour.magenta))

    # Animate at 2 frames per second
    sense_hat.start_animation(2)

# Main program function
try:
    # Start the default animation
    animation_both_servers_up()
    current_state = 0
    while 1:
        # Check for sense hat stick events
        for event in sense_hat.stick.get_events():
           check_stick()

        # Monitor remote servers
        responseOne = ping_server("www.google.com")
        responseTwo = ping_server("www.aftonbladet.se")

        # Set the face type based on the result of the two pings
        # (Only start a new animation if the state has changed)

        # Both pings successful
        if responseOne == 0 and responseTwo == 0:
            if current_state != 0:
                animation_both_servers_up()
                current_state = 0

        # Google unavailable
        if responseOne != 0 and responseTwo == 0:
            if current_state != 1:
                animation_google_down()
                current_state = 1
        
        # Aftonbladet unavailable
        if responseOne == 0 and responseTwo != 0:
            if current_state != 2:
                animation_aftonbladet_down()
                current_state = 2

        # Both pings unsuccessful
        if responseOne != 0 and responseTwo != 0:
            if current_state != 3:
                animation_both_servers_down()
                current_state = 3

        # Sleep for 1 second to avoid ping flooding
        sleep(1)

except KeyboardInterrupt:
    pre_quit_actions()
    quit()
