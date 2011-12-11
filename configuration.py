from config import Config
import sys

def get_config(filename):
	errors = []
	config = None
	try:
		config = Config(filename)
	except:
		errors.append('could not open config file: %s' % filename)
	else:
		if 'secret_key' not in config:
			errors.append('secret_key must be defined')
		
		if 'repos' not in config:
			errors.append('repos must be defined')
		elif len(config.repos)  < 1:
			errors.append('repos must contain at least one repository')
		else:
			for (i, repo) in enumerate(config.repos):
				if 'location' not in repo:
					errors.append('repos[%i] does not contain \'location\'' % i)
				if 'remote' not in repo:
					errors.append('repos[%i] does not contain \'remote\'' % i)
	
	if len(errors) > 0:
		print('Error reading config file:')
		for e in errors:
			print('\t%s' % e)
		sys.exit()
	else:
		return config