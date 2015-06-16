from flask import Flask, request
app = Flask(__name__)
import sys
sys.path.append('.')
import lights.occupancy
import daemon

MASTER_BATH = lights.occupancy.Occupancy("192.168.1.105", 10)

@app.route('/master_bath')
def master_bath():
	pir_state = int(request.args.get("pir_state", 0))
	MASTER_BATH.trigger(pir_state)
	return "Master Bath Method worked"


@app.route('/lights_mb')
def lights_mb():
	pir_state=request.args.get("pir_state", 0)
	MASTER_BATH.trigger(pir_state)
	return "lights_mb"

if __name__ == '__main__':
	with daemon.DaemonContext():
		app.run(host="0.0.0.0")
