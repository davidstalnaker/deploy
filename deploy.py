from flask import *
from configuration import get_config
import git
import subprocess
import json
import re
import os
import pwd

app = Flask(__name__)
config = get_config('deploy.conf')

@app.route('/%s' % config.secret_key, methods=['POST'])
def reload():
	
	payload = json.loads(request.form['payload'])
	url = payload['repository']['url']
	
	for repo in config.repos:
		if urls_are_equal(url, repo.remote):
			success = pull(repo)
			if success and 'reload_command' in repo:
				subprocess.call(repo.reload_command, shell=True)
	return ""
	
def pull(repo):
	try:
		if 'git_user' in repo:
			uid, gid = ids_for_user(repo.git_user)
		else:
			uid, gid = ids_for_file(repo.location)
		become_user(uid, gid)
		
		r = git.Repo(repo.location)
		info = r.remotes.origin.pull()[0]
				
		if info.flags & info.REJECTED:
			print('Error: merge failed')
			return False
		elif info.flags & info.HEAD_UPTODATE:
			print('Head already up to date')
			return True
		else:
			return True
		
	except OSError:
		print('Insufficient permissions to change uid/gid')
		return False
	except ValueError:
		print('Insufficient permissions to pull repository')
		return False
	except AssertionError as e:
		if 'overwritten by merge' in e.message:
			print('Error: merge conflict')
		else:
			print('Error: %s' % e.message)
		return False
	finally:
		become_root();
		

	
		
def ids_for_user(username):
	pw = pwd.getpwnam('max')
	return (pw.pw_uid, pw.pw_gid)
		
def ids_for_file(filename):
	st = os.stat(filename)
	return (st.st_uid, st.st_gid)	
	
def become_user(uid, gid):
	os.setegid(gid)
	os.seteuid(uid)
	
def become_root():
	os.seteuid(0)
	os.setegid(0)
	
def urls_are_equal(first, second):
	first = re.split('://', first)[-1]
	second = re.split('://', second)[-1]
	return first == second

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=9001, debug=True)
	