#!/usr/bin/env python3
# Author: Alex Culp

from views import app
import sys

if __name__ == "__main__":
	secret = sys.argv[-1]
	# attempt to run "python3 run.py" without key provided
	if secret == __file__:
		raise SyntaxError("Syntax for execution: python3 run.py <secret_key>")
	app.config['SECRET_KEY'] = secret
	app.run(host = '0.0.0.0', port = 8000, debug = True)
