import os
import json
from datetime import datetime, timedelta
from flask import Flask, request, session, jsonify, send_from_directory, redirect
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)  # Enable CORS for frontend communication

# Configure secret key for signing session cookies
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_change_me')
app.permanent_session_lifetime = timedelta(hours=2)

# File paths for JSON data storage
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, 'users.json')
INVENTORY_FILE = os.path.join(BASE_DIR, 'inventory.json')
ISSUES_FILE = os.path.join(BASE_DIR, 'issues.json')
AUDIT_LOG_FILE = os.path.join(BASE_DIR, 'audit_log.json')

# Helper functions for JSON file operations
def read_json_file(filepath):
	"""Read and return JSON data from file"""
	try:
		with open(filepath, 'r') as f:
			return json.load(f)
	except FileNotFoundError:
		return None
	except json.JSONDecodeError:
		return None

def write_json_file(filepath, data):
	"""Write data to JSON file"""
	with open(filepath, 'w') as f:
		json.dump(data, f, indent=2)

def log_audit(action, details):
	"""Add entry to audit log"""
	audit_data = read_json_file(AUDIT_LOG_FILE) or {'logs': []}
	audit_data['logs'].append({
		'timestamp': datetime.now().isoformat(),
		'action': action,
		'details': details,
		'user': session.get('admin', 'anonymous')
	})
	write_json_file(AUDIT_LOG_FILE, audit_data)

# Static file routes
@app.route('/')
def index():
	"""Redirect to start page"""
	return redirect('/Startpage/Startpage.html')

@app.route('/<path:path>')
def serve_static(path):
	"""Serve static files (HTML, JS, CSS)"""
	return send_from_directory('.', path)

# Authentication endpoints
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
	data = request.get_json(silent=True) or {}
	username = data.get('username')
	password = data.get('password')

	if not username or not password:
		return jsonify({'error': 'Missing username or password'}), 400

	# Read users from JSON file
	users_data = read_json_file(USERS_FILE)
	if not users_data or 'users' not in users_data:
		return jsonify({'error': 'Users database not found'}), 500

	# Check credentials
	user_found = False
	for user in users_data['users']:
		if user['username'] == username and user['password'] == password:
			user_found = True
			break

	if not user_found:
		log_audit('login_failed', f'Failed login attempt for username: {username}')
		return jsonify({'error': 'Invalid credentials'}), 401

	# Create session
	session.permanent = True
	session['admin'] = username
	log_audit('login_success', f'User {username} logged in successfully')
	return jsonify({'ok': True, 'username': username})


@app.route('/api/admin/me', methods=['GET'])
def admin_me():
	if 'admin' in session:
		return jsonify({'username': session['admin']})
	return jsonify({'error': 'Unauthorized'}), 401


@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
	username = session.get('admin', 'unknown')
	session.pop('admin', None)
	log_audit('logout', f'User {username} logged out')
	return jsonify({'ok': True})


# Inventory management endpoints
@app.route('/api/inventory', methods=['GET'])
def get_inventory():
	"""Get all inventory items"""
	inventory_data = read_json_file(INVENTORY_FILE)
	if not inventory_data:
		return jsonify({'error': 'Inventory not found'}), 404
	return jsonify(inventory_data)


@app.route('/api/inventory/<int:item_id>', methods=['GET'])
def get_inventory_item(item_id):
	"""Get a specific inventory item"""
	inventory_data = read_json_file(INVENTORY_FILE)
	if not inventory_data:
		return jsonify({'error': 'Inventory not found'}), 404

	for item in inventory_data['items']:
		if item['id'] == item_id:
			return jsonify(item)

	return jsonify({'error': 'Item not found'}), 404


@app.route('/api/inventory', methods=['POST'])
def add_inventory_item():
	"""Add a new inventory item"""
	if 'admin' not in session:
		return jsonify({'error': 'Unauthorized'}), 401

	data = request.get_json(silent=True) or {}
	name = data.get('name')
	price = data.get('price')
	quantity = data.get('quantity')

	if not name or price is None or quantity is None:
		return jsonify({'error': 'Missing required fields: name, price, quantity'}), 400

	inventory_data = read_json_file(INVENTORY_FILE) or {'items': []}

	# Generate new ID
	new_id = max([item['id'] for item in inventory_data['items']], default=0) + 1

	new_item = {
		'id': new_id,
		'name': name,
		'price': float(price),
		'quantity': int(quantity)
	}

	inventory_data['items'].append(new_item)
	write_json_file(INVENTORY_FILE, inventory_data)
	log_audit('inventory_add', f'Added item: {name}')

	return jsonify(new_item), 201


@app.route('/api/inventory/<int:item_id>', methods=['PUT'])
def update_inventory_item(item_id):
	"""Update an existing inventory item"""
	if 'admin' not in session:
		return jsonify({'error': 'Unauthorized'}), 401

	data = request.get_json(silent=True) or {}
	inventory_data = read_json_file(INVENTORY_FILE)

	if not inventory_data:
		return jsonify({'error': 'Inventory not found'}), 404

	for item in inventory_data['items']:
		if item['id'] == item_id:
			if 'name' in data:
				item['name'] = data['name']
			if 'price' in data:
				item['price'] = float(data['price'])
			if 'quantity' in data:
				item['quantity'] = int(data['quantity'])

			write_json_file(INVENTORY_FILE, inventory_data)
			log_audit('inventory_update', f'Updated item ID {item_id}: {item["name"]}')
			return jsonify(item)

	return jsonify({'error': 'Item not found'}), 404


@app.route('/api/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
	"""Delete an inventory item"""
	if 'admin' not in session:
		return jsonify({'error': 'Unauthorized'}), 401

	inventory_data = read_json_file(INVENTORY_FILE)

	if not inventory_data:
		return jsonify({'error': 'Inventory not found'}), 404

	for i, item in enumerate(inventory_data['items']):
		if item['id'] == item_id:
			deleted_item = inventory_data['items'].pop(i)
			write_json_file(INVENTORY_FILE, inventory_data)
			log_audit('inventory_delete', f'Deleted item: {deleted_item["name"]}')
			return jsonify({'ok': True, 'deleted': deleted_item})

	return jsonify({'error': 'Item not found'}), 404


# Issue reporting endpoints
@app.route('/api/issues', methods=['GET'])
def get_issues():
	"""Get all reported issues"""
	if 'admin' not in session:
		return jsonify({'error': 'Unauthorized'}), 401

	issues_data = read_json_file(ISSUES_FILE) or {'issues': []}
	return jsonify(issues_data)


@app.route('/api/issues', methods=['POST'])
def report_issue():
	"""Submit a new issue report"""
	data = request.get_json(silent=True) or {}
	issue_text = data.get('issue')

	if not issue_text:
		return jsonify({'error': 'Issue text is required'}), 400

	issues_data = read_json_file(ISSUES_FILE) or {'issues': []}

	new_issue = {
		'id': len(issues_data['issues']) + 1,
		'issue': issue_text,
		'timestamp': datetime.now().isoformat(),
		'status': 'open'
	}

	issues_data['issues'].append(new_issue)
	write_json_file(ISSUES_FILE, issues_data)
	log_audit('issue_reported', f'New issue reported: {issue_text[:50]}...')

	return jsonify(new_issue), 201


@app.route('/api/issues/<int:issue_id>', methods=['PUT'])
def update_issue(issue_id):
	"""Update an issue status"""
	if 'admin' not in session:
		return jsonify({'error': 'Unauthorized'}), 401

	data = request.get_json(silent=True) or {}
	issues_data = read_json_file(ISSUES_FILE)

	if not issues_data:
		return jsonify({'error': 'Issues not found'}), 404

	for issue in issues_data['issues']:
		if issue['id'] == issue_id:
			if 'status' in data:
				issue['status'] = data['status']
			write_json_file(ISSUES_FILE, issues_data)
			log_audit('issue_updated', f'Updated issue ID {issue_id}')
			return jsonify(issue)

	return jsonify({'error': 'Issue not found'}), 404


# Audit log endpoint
@app.route('/api/audit', methods=['GET'])
def get_audit_log():
	"""Get audit log entries"""
	if 'admin' not in session:
		return jsonify({'error': 'Unauthorized'}), 401

	audit_data = read_json_file(AUDIT_LOG_FILE) or {'logs': []}
	return jsonify(audit_data)


# Payment tracking endpoint
@app.route('/api/payment', methods=['POST'])
def process_payment():
	"""Log a payment transaction"""
	data = request.get_json(silent=True) or {}
	amount = data.get('amount')
	item_id = data.get('item_id')

	if amount is None or item_id is None:
		return jsonify({'error': 'Missing required fields: amount, item_id'}), 400

	log_audit('payment_processed', f'Payment of ${amount} for item ID {item_id}')

	# Update inventory quantity
	inventory_data = read_json_file(INVENTORY_FILE)
	if inventory_data:
		for item in inventory_data['items']:
			if item['id'] == item_id:
				item['quantity'] = max(0, item['quantity'] - 1)
				write_json_file(INVENTORY_FILE, inventory_data)
				break

	return jsonify({
		'ok': True,
		'transaction_id': datetime.now().strftime('%Y%m%d%H%M%S'),
		'amount': amount,
		'timestamp': datetime.now().isoformat()
	})


if __name__ == '__main__':
	# Run for local development
	app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)