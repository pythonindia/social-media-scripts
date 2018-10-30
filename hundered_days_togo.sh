#!/bin/bash

# 100 Days to go! - a CLI Bash script to show the number of days to PyCon India, 2018

# Within ~/.bashrc, append the following on a newline, so that this is run on bash start.
# '/location/to/hundered_days_togo.sh'

# Copyright (c) 2018 Devdutt Shenoi <mail@devdutt.me>

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# All ideas or/and suggestions would be appreciated either by email me or by 
# http://github.com/devdutt-shenoi/social-media-scripts.
# Thank you.

# Requires: bash 4.0+

# Some Variables
reset=$'\033[0m' # Reset Text
bold=$'\033[1m' # Bold Text
underline=$'\033[4m' # Underline Text

# Set the following date to that for PyCon India 2019
dest_date="2019-10-06"
diff=$(( ($(date '+%s' -d "$dest_date") - $(date '+%s')) / 86400))

echo "There are ${bold}$diff${reset} days to go for ${bold}${underline}in.PyCon.org${reset}"

# TODO : add support for colors and decoration
