from flask import *
from git import *
from subprocess import call
from config import Config
import json
import re
import os

app = Flask(__name__)
config = Config('deploy.conf')

@app.route('/%s' % config.secret_key, methods=['POST'])
def reload():
	
	payload = json.loads(request.form['payload'])
	url = payload['repository']['url']
	
	for repo in config.repos:
		if urls_are_equal(url, repo.remote):
			pull_and_reload(repo.location, repo.reload_command)
	return ""
	
def pull_and_reload(repo_location, reload_command):
	stat = os.stat(repo_location)
	uid = stat.st_uid
	gid = stat.st_gid
	os.setegid(gid)
	os.seteuid(uid)
	
	r = Repo(repo_location)
	try:
		info = r.remotes.origin.pull()[0]
		os.seteuid(0)
		os.setegid(0)
		if info.flags & info.REJECTED:
			print('error: merge failed')
		elif info.flags & info.HEAD_UPTODATE:
			print('head already up to date')
			call(reload_command, shell=True)
		else:
			call(reload_command, shell=True)
	except Exception as e:
		raise(e)
		print('error: merge failed')
		
	
	
	
	
def urls_are_equal(first, second):
	first = re.split('://', first)[-1]
	second = re.split('://', second)[-1]
	return first == second

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=9001, debug=True)
	