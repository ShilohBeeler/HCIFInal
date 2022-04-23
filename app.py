from flask import Flask, render_template, jsonify, request, session
import json

application = Flask(__name__)

application.secret_key = "whatever"

@application.route('/')
def hello_world():
	if not 'member_data' in session:
		session['member_data'] = []
	return render_template('main.html')

@application.route('/add_member')
def add_member():
	member_name = request.args.get('name', 'NAME_FETCH_ERROR', type=str)
	members = session['member_data']
	member = {'id': len(members), 'name': member_name}
	members.append(member)
	session['member_data']=members
	return jsonify(result='success')

@application.route('/remove_member')
def remove_member():
	member_id = request.args.get('id', -1, type=int)
	members = session['member_data']
	if member_id == -1 or not members:
		return jsonify(result=-1)
	members.pop(member_id)
	for i in range(len(members)):
		members[i]['id'] = i
	session['member_data']=members
	if member_id >= len(members):
		return jsonify(result=member_id-1)
	elif member_id == 0 and not members:
		return jsonify(result=-1)
	else:
		return jsonify(result=member_id)

@application.route('/next_member')
def next_member():
	member_id = request.args.get('id', -1, type=int)
	members = session['member_data']
	if not members:
		return jsonify(result=-1)
	elif member_id >= len(members)-1:
		return jsonify(result=0)
	else:
		return jsonify(result=member_id+1)

@application.route('/show_members')
def show_members():
	members = session['member_data']
	return jsonify(result=members)

if __name__ == '__main__':
	application.run(host='0.0.0.0', port='80')
