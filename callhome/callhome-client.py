from callhome.client import client as application
from callhome.shared.workers.cisco import CiscoAsa

"""
CallHome Client
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
    client = application.CallHomeClient()
    client.callhome()
    if client.ip_is_changed():
        print(f"IP is changed: curr {client.get_current_ip()} vs config {client.get_config_ip()}\n")
        local_device = CiscoAsa(peer_data=client.vpn_data, change=True)
