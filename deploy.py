from flask import *
from git import *
from subprocess import call
import json
import re
app = Flask(__name__)

repos = [
	{
		'name': 'pushlink',
		'location': '/var/www/pushlink',
		'remote': 'http://github.com/davidstalnaker/pushlink-server',
		'reload_command': 'service pushlink restart'
	}
]

key = 'giuyoa2woe8iuyi6jienlUsplusoeyoa'

@app.route('/%s' % key, methods=['POST'])
def reload():
	
	payload = json.loads(request.form['payload'])
	url = payload['repository']['url']
	
	for repo in repos:
		if urls_are_equal(url, repo['remote']):
			pull_and_reload(repo['location'], repo['reload_command'])
	return ""
	
def pull_and_reload(repo_location, reload_command):
	r = Repo(repo_location)
	try:
		info = r.remotes.origin.pull()[0]
		if info.flags & info.REJECTED:
			print('error: merge failed')
		elif info.flags & info.HEAD_UPTODATE:
			print('head already up to date')
			call(reload_command, shell=True)
		else:
			call(reload_command, shell=True)
	except:
		print('error: merge failed')
	
	
def urls_are_equal(first, second):
	first = re.split('://', first)[-1]
	second = re.split('://', second)[-1]
	return first == second

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=9001, debug=True)
