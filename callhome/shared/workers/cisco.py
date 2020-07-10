import json
import requests
from requests.auth import HTTPBasicAuth
from callhome import config
from jinja2 import Environment, FileSystemLoader


def cisco_asa(conf=None):
    """
    A function to execute commands on a Cisco ASA appliance.
    Commands can be added in the config.ini section 'CISCOASA', as a list.
    Otherwise, a dictionary with preset key names and there values retrieved
    from your source (the Callhome Server API for instance).

    :param conf: dict
    :return: None
    """
    if not conf:
        cmds = json.loads(config.get("CISCOASA", "COMMANDS"))
    else:
        env = Environment(loader=FileSystemLoader('shared/templates'))
        template = env.get_template('ciscoasa.j2')
        cmds = template.render(conf).split('\n')

    data = {"commands": cmds}
    try:
        response = requests.post(f"https://{config['LOCAL']['HOST']}/api/cli", verify=False,
                                 auth=HTTPBasicAuth(config['LOCAL']['USERNAME'], config['LOCAL']['PASSWORD']),
                                 json=data)
    except requests.exceptions.Timeout:
        raise SystemExit("Timed out...")
    except requests.exceptions.ConnectionError:
        raise SystemExit("URL Bad or host down?")
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    else:
        if response.status_code != 200:
            try:
                raise SystemExit(f"Broken: {response.json()['messages'][0]['details']}")
            except (KeyError, TypeError):
                try:
                    raise SystemExit(f"Broken: {response.json()['messages']}")
                except KeyError:
                    raise SystemExit(f"Invalid input/command: {response.json()['response']}")
            except json.decoder.JSONDecodeError:
                SystemExit(f"No valid JSON data retrieved, callhomeserver error: {response.status_code}")
        else:
            try:
                r = response.json()['response']
            except json.decoder.JSONDecodeError:
                SystemExit(f"No valid JSON data retrieved, callhomeserver error: {response.status_code}")
            else:
                for msg in r:
                    if msg:
                        print(msg)
