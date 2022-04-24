from flask import Flask, render_template, jsonify, request, session

application = Flask(__name__)

application.secret_key = 'whatever'

# Delivers the main page.
@application.route('/')
def hello_world():
	if not 'member_data' in session:
		session['member_data'] = []
	if not 'logs' in session:
		session['logs'] = []
	return render_template('main.html')

# Functions that manage members (units, enemies, players, etc.)
@application.route('/add_member')
def add_member():
	member_name = request.args.get('name', 'default_name', type=str)
	initiative = request.args.get('initiative', -1, type=int)
	max_hp = current_hp = request.args.get('max_hp', -1, type=int)
	max_mp = current_mp = request.args.get('max_mp', -1, type=int)
	armor_class = request.args.get('armor_class', -1, type=int)
	members = session['member_data']
	member = {'id': len(members), 
						'name': member_name,
						'initiative': initiative,
						'current_hp': current_hp,
						'max_hp': max_hp,
						'current_mp': current_mp,
						'max_mp': max_mp,
						'armor_class': armor_class}
	members.append(member)
	session['member_data']=members
	return jsonify(result='success')

@application.route('/remove_member')
def remove_member():
	member_id = request.args.get('id', -1, type=int)
	members = session['member_data']
	if member_id == -1 or not members:
		return jsonify(result={'id':-1, 'name':'N/A'})
	members.pop(member_id)
	for i in range(len(members)):
		members[i]['id'] = i
	session['member_data']=members
	if member_id == 0 and not members:
		return jsonify(result={'id':-1, 'name':'N/A'})
	elif member_id >= len(members):
		return jsonify(result={'id':member_id-1, 'name':members[member_id-1]['name']})
	else:
		return jsonify(result={'id':member_id, 'name':members[member_id]['name']})

@application.route('/next_member')
def next_member():
	member_id = request.args.get('id', -1, type=int)
	members = session['member_data']
	if not members:
		return jsonify(result={'id':-1, 'name':'N/A'})
	elif member_id >= len(members)-1:
		return jsonify(result={'id':0, 'name':members[0]['name']})
	else:
		return jsonify(result={'id':member_id+1, 'name':members[member_id+1]['name']})

@application.route('/show_members')
def show_members():
	members = session['member_data']
	return jsonify(result=members)

# Functions that manage individual actions. do_action and do_action_to_target are the prototpyes.
@application.route('/do_action')
def do_action():
	member_id = request.args.get('id', -1, type=int)
	if member_id == -1:
		return jsonify(result='failure')
	logs = session['logs']
	members = session['member_data']
	new_log = {'text': members[member_id]['name'] + ' did a thing.'}
	logs.append(new_log)
	session['logs'] = logs
	return jsonify(result='success')

@application.route('/do_action_to_target')
def do_action_to_target():
	member_id = request.args.get('id', -1, type=int)
	target_id = request.args.get('target', -1, type=int)
	if member_id == -1:
		return jsonify(result='failure')
	logs = session['logs']
	members = session['member_data']
	new_log = {'text': members[member_id]['name'] + ' did a thing to ' + members[target_id]['name'] + '.'}
	logs.append(new_log)
	session['logs'] = logs
	return jsonify(result='success')

@application.route('/attack')
def attack():
	member_id = request.args.get('id', -1, type=int)
	target_id = request.args.get('target', -1, type=int)
	damage = request.args.get('damage', 0, type=int)
	weapon = request.args.get('weapon', 'default_weapon', type=str)
	if member_id == -1:
		return jsonify(result='failure')
	logs = session['logs']
	members = session['member_data']
	members[target_id]['current_hp'] = max(members[target_id]['current_hp']-damage,0)
	new_log = {'text': members[member_id]['name'] + ' did ' + str(damage) + ' damage to ' + members[target_id]['name'] + ' using a(n) ' + weapon + '.'}
	logs.append(new_log)
	session['logs'] = logs
	session['member_data'] = members
	return jsonify(result='success')

@application.route('/move')
def move():
	member_id = request.args.get('id', -1, type=int)
	distance = request.args.get('distance', 0, type=int)
	if member_id == -1:
		return jsonify(result='failure')
	logs = session['logs']
	members = session['member_data']
	new_log = {'text': members[member_id]['name'] + ' moved ' + str(distance) + 'ft.'}
	logs.append(new_log)
	session['logs'] = logs
	return jsonify(result='success')

@application.route('/ready')
def ready():
	member_id = request.args.get('id', -1, type=int)
	action = request.args.get('action', 0, type=str)
	if member_id == -1:
		return jsonify(result='failure')
	logs = session['logs']
	members = session['member_data']
	new_log = {'text': members[member_id]['name'] + ' readied the action "' + action + '" for later.'}
	logs.append(new_log)
	session['logs'] = logs
	return jsonify(result='success')

@application.route('/reaction')
def reaction():
	member_id = request.args.get('id', -1, type=int)
	target_id = request.args.get('target', -1, type=int)
	damage = request.args.get('damage', 0, type=int)
	if member_id == -1:
		return jsonify(result='failure')
	logs = session['logs']
	members = session['member_data']
	members[target_id]['current_hp'] = max(members[target_id]['current_hp']-damage,0)
	new_log = {'text': members[member_id]['name'] + ' dealt ' + str(damage) + ' reaction damage to ' + members[target_id]['name'] + '.'}
	logs.append(new_log)
	session['logs'] = logs
	session['member_data'] = members
	return jsonify(result='success')

@application.route('/bonus_action')
def bonus_action():
	member_id = request.args.get('id', -1, type=int)
	action = request.args.get('action', 0, type=str)
	if member_id == -1:
		return jsonify(result='failure')
	logs = session['logs']
	members = session['member_data']
	new_log = {'text': members[member_id]['name'] + ' took the action "' + action + '" as a bonus action.'}
	logs.append(new_log)
	session['logs'] = logs
	return jsonify(result='success')

@application.route('/bonus_attack')
def bonus_attack():
	member_id = request.args.get('id', -1, type=int)
	target_id = request.args.get('target', -1, type=int)
	damage = request.args.get('damage', 0, type=int)
	weapon = request.args.get('weapon', 'default_weapon', type=str)
	if member_id == -1:
		return jsonify(result='failure')
	logs = session['logs']
	members = session['member_data']
	members[target_id]['current_hp'] = max(members[target_id]['current_hp']-damage,0)
	new_log = {'text': members[member_id]['name'] + ' did ' + str(damage) + ' damage to ' + members[target_id]['name'] + ' using a(n) ' + weapon + ' as a bonus action.'}
	logs.append(new_log)
	session['logs'] = logs
	session['member_data'] = members
	return jsonify(result='success')

# Functions to manage the logs.
@application.route('/clear_logs')
def clear_logs():
	session['logs'] = []
	return jsonify(result='success')

@application.route('/show_logs')
def show_logs():
	logs = session['logs']
	return jsonify(result=logs)

if __name__ == '__main__':
	application.run(host='0.0.0.0', port='80')
