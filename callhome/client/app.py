import json
import requests
from requests.auth import HTTPBasicAuth
from callhome import config
from callhome.server import error


class CallHomeClient(object):
    """
    Callhome-Client

    This class executes by default an API-call to the Callhome-Server. It retrieves nessecary information about
    the site it requests for.

    Functions to call:
        - get_current_ip (ret: str)
        - get_config_ip (ret: str)
        - ip_is_changed (ret: bool)
        - run (automated process)
    """

    def __init__(self):
        try:
            if config['CLIENT'] or config['SERVER']:
                pass
        except KeyError:
            raise SystemExit('Issue with or missing config.ini!')
        self.url = f"https://{config['SERVER']['HOST']}" \
                   f"/api/v{config['API']['VERSION']}/show/settings/{config['CLIENT']['USERNAME']}"
        self.u = config['CLIENT']['USERNAME']
        self.p = config['CLIENT']['PASSWORD']
        self.current_ip = '0.0.0.0'
        self.config_ip = '0.0.0.0'
        self.headers = {
            'Accept': 'application/json'
        }

        try:
            response = requests.get(self.url, headers=self.headers, verify=False, auth=HTTPBasicAuth(self.u, self.p))
        except requests.exceptions.Timeout:
            raise SystemExit("Timed out...")
        except requests.exceptions.ConnectionError:
            raise SystemExit("URL Bad or host down?")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        try:
            json_data = response.json()
            if json_data['ok']:
                self.api_data = json_data['result'][0]
            else:
                raise SystemExit(json_data)
        except json.decoder.JSONDecodeError:
            raise SystemExit(f"No valid JSON data retrieved, callhomeserver error: {response.status_code}")

        self.config_ip = self.api_data['config_ip']
        self.current_ip = self.api_data['current_ip']

        # vpn_data key names are not to be changed as they are used in the jinja2 template
        self.vpn_data = {'crypto_map_id': self.api_data['id'],
                         'new_ip_address': self.api_data['current_ip'],
                         'old_ip_address': self.api_data['config_ip'],
                         'preshared_key': self.api_data['preshared'],
                         'description': self.api_data['description']}

    def get_current_ip(self):
        return self.current_ip

    def get_config_ip(self):
        return self.config_ip

    def ip_is_changed(self):
        if self.config_ip != self.current_ip:
            return True
        else:
            return False

    def run(self):
        # FIXME: This should be the automated part where it all comes together
        if self.ip_is_changed():
            print("going to fix it in a jiffy")
