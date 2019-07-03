"""Basic Flask application for interacting with USB Energenie ENER011 via sispm"""

# Built In
import time

# Third Party
import sispm
from flask import Flask, jsonify
from werkzeug.routing import BaseConverter


def get_target_from_id(device_id):
    """Return target (If available) based on ID from list of devices"""
    devices = sispm.connect()
    for device in devices:
        if sispm.getid(device) == device_id:
            return device
    return None


def get_target_from_index(device_index):
    """Return target (If available) based on index from list of devices"""
    devices = sispm.connect()
    try:
        return devices[int(device_index) - 1]
    except IndexError:
        return None


def validate_port(device, port):
    """Verify port is available, return bool"""
    port_min = sispm.getminport(device)
    port_max = sispm.getmaxport(device)

    if port < port_min or port > port_max:
        return False

    return True


app = Flask("EnergenieInterface")


class RegexConverter(BaseConverter):
    """Thanks https://stackoverflow.com/a/5872904"""
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


@app.route("/devices")
def get_devices():
    """Return list of connected devices"""
    devices = sispm.connect()
    return jsonify({"devices": [sispm.getid(d) for d in devices]})


@app.route("/control/<regex('\w{2}:\w{2}:\w{2}:\w{2}:\w{2}|\d{1}'):device_id>/<int:port>/<int:state>")
def interact_with_device(device_id, port, state):
    """One stop endpoint to do it all"""

    if len(device_id) == 1:
        target = get_target_from_index(device_id)
        if target is None:
            return jsonify({"error": f"Index {device_id} not found in devices list"})

    else:
        target = get_target_from_id(device_id)
        if target is None:
            return jsonify({"error": f"Device with ID {device_id} not found"})

    if not validate_port(target, port):
        return jsonify({"error": "{} is out of range for device ({} - {})".format(
            port, sispm.getminport(target), sispm.getmaxport(target))})

    action = sispm.switchon if state == 1 else sispm.switchoff
    action(target, port)

    return jsonify("OK")


@app.route("/cycle/<regex('\w{2}:\w{2}:\w{2}:\w{2}:\w{2}|\d{1}'):device_id>/<int:port>")
@app.route("/cycle/<regex('\w{2}:\w{2}:\w{2}:\w{2}:\w{2}|\d{1}'):device_id>/<int:port>/<int:wait>")
def cycle_device_port(device_id, port, wait=2):
    """Cycle a port off then on"""

    if len(device_id) == 1:
        target = get_target_from_index(device_id)
        if target is None:
            return jsonify({"error": f"Index {device_id} not found in devices list"})

    else:
        target = get_target_from_id(device_id)
        if target is None:
            return jsonify({"error": f"Device with ID {device_id} not found"})

    if not validate_port(target, port):
        return jsonify({"error": "{} is out of range for device ({} - {})".format(
            port, sispm.getminport(target), sispm.getmaxport(target))})

    sispm.switchoff(target, port)
    time.sleep(wait)
    sispm.switchon(target, port)

    return jsonify("OK")


@app.route("/status")
@app.route("/status/<regex('\w{2}:\w{2}:\w{2}:\w{2}:\w{2}|\d{1}'):device_id>")
@app.route("/status/<regex('\w{2}:\w{2}:\w{2}:\w{2}:\w{2}|\d{1}'):device_id>/<int:port>")
def get_device_status(device_id=None, port=None):
    """Return dictionary of all device ports and status of each"""

    if device_id is not None:

        if len(device_id) == 1:
            target = get_target_from_index(device_id)
            if target is None:
                return jsonify({"error": f"Index {device_id} not found in devices list"})

        else:
            target = get_target_from_id(device_id)
            if target is None:
                return jsonify({"error": f"Device with ID {device_id} not found"})


        if port is None:
            retval = {"status": {}}
            for port in range(sispm.getminport(target), sispm.getmaxport(target) + 1):
                retval["status"][port] = sispm.getstatus(target, port)

        elif validate_port(target, port):
            retval = {"status": sispm.getstatus(target, port)}

        else:
            return jsonify({"error": "{} is out of range for device ({} - {})".format(
                port, sispm.getminport(target), sispm.getmaxport(target))})

    else:
        retval = {"status": {}}
        for device in sispm.connect():
            device_id = sispm.getid(device)

            retval["status"][device_id] = {}

            for port in range(sispm.getminport(device), sispm.getmaxport(device) + 1):
                retval["status"][device_id][port] = sispm.getstatus(device, port)

    return jsonify(retval)


if __name__ == "__main__":
    app.run()
