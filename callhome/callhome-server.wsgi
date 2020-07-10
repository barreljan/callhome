#!/usr/bin/env python3.7

import logging
import sys
sys.path.insert(0, '/var/www/html/callhome/server')
sys.path.insert(0, '/var/www/html/callhome/server')
sys.path.insert(0, '/var/www/html/callhome/venv/lib/python3.7/site-packages')
logging.basicConfig(stream=sys.stderr)

"""
CallHome Server
Copyright (C) 2020  Bartjan Hoogenbosch, <bartjan@pc-mania.nl>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from callhome.server.api import app as application
