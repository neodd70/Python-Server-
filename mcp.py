from flask import Flask, request
app = Flask(__name__)
import sys
sys.path.append('.')
import lights.occupancy
import daemon

MASTER_BATH = lights.occupancy.Occupancy("192.168.1.130", 180)

@app.route('/master_bath')
def master_bath():
	try:
		pir_state = int(request.args.get("pir_state", 0))
		button_pressed = int(request.args.get("button_pressed", 0))
		print "pir_state:", pir_state
		print "button_pressed:", button_pressed
		print "_button_override:", MASTER_BATH._button_override
		if pir_state: 
			MASTER_BATH.trigger(pir_state)
		if button_pressed:
			MASTER_BATH.button(button_pressed)	
	except Exception, error:
		print error
		return error
	return "What has happened - PIR is {0} Button Pressed is {1} Button Override is {2}".format(pir_state, button_pressed, MASTER_BATH._button_override)

if __name__ == '__main__':
	with daemon.DaemonContext():
		app.run(host="0.0.0.0")
