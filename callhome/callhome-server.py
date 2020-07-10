from callhome.server.api import app
from callhome import config

"""
--
This is for development only. This runs the app and API directly with Flask/Python. Use a proper WSGI server
for production.
--

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


if __name__ == '__main__':
    try:
        app.run(host=config['LISTENER']['APP_LISTENER'], port=config['LISTENER']['APP_PORT'])
    except OSError as e:
        raise SystemExit(f"The callhome server can not run: {e}")
