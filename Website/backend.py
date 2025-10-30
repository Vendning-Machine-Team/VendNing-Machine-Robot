import os
from datetime import timedelta
from flask import Flask, request, session, jsonify
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Configure secret key for signing session cookies. Set in environment in production.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_change_me')
app.permanent_session_lifetime = timedelta(hours=2)

# Admin credentials (prefer: set ADMIN_USERNAME and ADMIN_HASH in environment)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_HASH = os.environ.get('ADMIN_HASH')
# Optional developer fallback (not for production): plain password in env
FALLBACK_PLAIN = os.environ.get('ADMIN_PASSWORD')


@app.route('/api/admin/login', methods=['POST'])
def admin_login():
	data = request.get_json(silent=True) or {}
	username = data.get('username')
	password = data.get('password')

	if not username or not password:
		return jsonify({'error': 'Missing username or password'}), 400

	if username != ADMIN_USERNAME:
		return jsonify({'error': 'Invalid credentials'}), 401

	# If an ADMIN_HASH is provided, validate using werkzeug's check_password_hash
	if ADMIN_HASH:
		if not check_password_hash(ADMIN_HASH, password):
			return jsonify({'error': 'Invalid credentials'}), 401
	else:
		# fallback: plain text comparison only for local/dev testing
		if FALLBACK_PLAIN is None or password != FALLBACK_PLAIN:
			return jsonify({'error': 'Invalid credentials'}), 401

	# Create a session cookie
	session.permanent = True
	session['admin'] = username
	return jsonify({'ok': True})


@app.route('/api/admin/me', methods=['GET'])
def admin_me():
	if 'admin' in session:
		return jsonify({'username': session['admin']})
	return jsonify({'error': 'Unauthorized'}), 401


@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
	session.pop('admin', None)
	return jsonify({'ok': True})


if __name__ == '__main__':
	# Run for local development. In production use a WSGI server and set proper env vars.
	app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)