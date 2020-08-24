import json
import re
import requests
from jinja2 import Environment, FileSystemLoader
from requests.auth import HTTPBasicAuth
from callhome import config, basedir


class CiscoAsa:
    """
    A class to verify and execute commands on a Cisco ASA appliance.
    Commands can be added in the config.ini section 'CISCOASA', as a list.
    Otherwise, a dictionary with preset key names and there values retrieved
    from your source (the Callhome Server API for instance).

    :param peer_data: dict
    :return: none

    peer_data structure:
        {'crypto_map_id': int,
        'new_ip_address': str,
        'old_ip_address': str,
        'preshared_key': str,
        'description': str}
    """

    def __init__(self, peer_data=None, change=False):
        self.env = Environment(loader=FileSystemLoader(f"{basedir}/shared/templates"))
        self.template = None
        self.data = None
        self.current_config = None
        self.verified = False
        self.change = change
        if not peer_data:
            self.cmds = json.loads(config.get("CISCOASA", "COMMANDS"))
            self.data = {"commands": self.cmds}
            self.call_asa()
        else:
            self.conf = peer_data

        print("Getting running config")
        self.get()
        print("Verify running config with the previous registered address")
        self.verify(self.conf['old_ip_address'])

        if self.verified and self.change:
            print("Going to make changes to the Cisco ASA...")
            self.set()

            print("Getting a fresh running config")
            self.get()
            print("Verify running config with the new registered address")
            self.verify(self.conf['new_ip_address'])
            if self.verified:
                print("Change successfull!")

        elif self.verified and not self.change:
            print("Verified, but NOT going to make changes to the Cisco ASA")
        elif not self.verified and self.change:
            print("NOT verified; mismatch, previous change failed? NOT going to make a change")
        else:
            print("Something bad may be happend")

    def verify(self, ip):
        peer_ok = False
        tunnel_ok = False
        # The traling whitespace is from Cisco but comes in handy
        # Make sure of the '$' as last match, as multiple peer addresses can exist on 1 line (whitespace divided)
        peer_rgx = re.compile('^.*set\\speer\\s(\\d.*)\\s$')
        tunnel_rgx = re.compile('^tunnel-group\\s(\\d.*)\\stype\\sipsec-l2l$')
        for msg in self.current_config:
            lines = msg.split('\n')
            for line in lines:
                if not peer_ok:
                    peer_m = peer_rgx.match(line)
                    if peer_m:
                        if peer_m.group(1) == ip:
                            peer_ok = True
                if not tunnel_ok:
                    tunnel_m = tunnel_rgx.match(line)
                    if tunnel_m:
                        if tunnel_m.group(1) == ip:
                            tunnel_ok = True
        if peer_ok and tunnel_ok:
            print(f"Verification OK. Running config has: {ip}")
            self.verified = True

    def get(self):
        self.template = self.env.get_template('ciscoasa_get.j2')
        self.data = {"commands": self.template.render(self.conf).split('\n')}
        self.current_config = self.call_asa()
        print("Done")

    def set(self):
        self.verified = False
        self.template = self.env.get_template('ciscoasa_set.j2')
        self.data = {"commands": self.template.render(self.conf).split('\n')}
        self.call_asa()
        print("Done")

    def call_asa(self):
        try:
            response = requests.post(f"https://{config['LOCAL']['HOST']}/api/cli", verify=False,
                                     auth=HTTPBasicAuth(config['LOCAL']['USERNAME'], config['LOCAL']['PASSWORD']),
                                     json=self.data, headers={"User-Agent": "REST API Agent"})
        except requests.exceptions.Timeout:
            raise SystemExit("Timed out...")
        except requests.exceptions.ConnectionError:
            raise SystemExit("URL Bad or host down?")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        if response.status_code != 200:
            try:
                raise SystemExit(f"Broken: {response.json()['messages'][0]['details']}")
            except (KeyError, TypeError):
                try:
                    raise SystemExit(f"Broken: {response.json()['messages']}")
                except KeyError:
                    import pprint
                    pprint.pprint(response.text)
                    raise SystemExit(f"Invalid input/command: {response.json()['response']}")
            except json.decoder.JSONDecodeError:
                raise SystemExit(f"Callhome client error: {response.status_code}\n"
                                 f"No valid JSON data retrieved: {response.text}")
        else:
            try:
                r = response.json()['response']
            except json.decoder.JSONDecodeError:
                SystemExit(f"Callhome client error: {response.status_code}\n"
                           f"No valid JSON data retrieved: {response.text}")
            else:
                return r
