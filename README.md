# sense-hat-network-monitor
A simple Raspberry Pi and Sense Hat monitoring application

## Synopsis

sense-hat-network-monitor is a simple Raspberry Pi and Sense Hat monitoring application which pings two servers and displays the result using the Sense Hat 8x8 RGB display. The display shows a green smiling face when both www.Google.com and www.Aftonbladet.se are available. If Google is unavailable (and AftonBladet is available) the display is blue.  If AftonBladet is unavailable (and Google is available) the display is yellow.  The display is red if both sites are unavailable.

## Motivation

This project was created as a demonstration IoT device for use with IoT security hardware and aims to provide a quick visual feedback to an audience without any complicated UI (or need for things like laptops). The program includes two extensions to the underlying Sense Hat libraries to provide animation and smooth fade-out of display pixels.

## Installation

Run the program from the command line using: python3 shnetmon.py

## Author

sense-hat-network-monitor is written and maintained by Simon Inns.

## License (Software)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
