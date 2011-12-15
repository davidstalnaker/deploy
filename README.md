# Deploy

A small server to automatically pull from GitHub when you push to that repository.  Additionally it can run a command afterwards (generally to restart a server).  It works by running a small web server that listens for POSTs from GitHub's [post-receive hooks](http://help.github.com/post-receive-hooks/).

## Installation

For now at least, just install the (python) dependencies and clone the repository.

	pip install Flask GitPython config
	git clone git://github.com/davidstalnaker/deploy.git

## Configuration

First, create a file deploy.conf file (or copy example.conf).  The following things need to be defined:

* secret_key - a long random string 
* repos - a list of dictionaries with options, one for each repository:
	* name - name of the repository (not actually used, just for organization)
	* location - the local location of the repository
	* remote - the location of the repository on github
	* reload_command - command to be run after pulling the repository
	* no_su (optional) - if true, will not change uid anywhere
	* git_user (optional) - specific user to run the git pull as (defaults to the the user who owns the root folder of the repository)

You will also need to add your server to GitHub's post-receive hooks.  To do this, go to Admin -> Service Hooks -> Post-Receive Urls and add <your url>/<secret key>.  This is also where you can test your server once it is running.

## Running

The simplest way to run it is simply 

	python deploy.py

If you need to be root to restart your server (eg using upstart or init.d), you will need to be root when you start the deploy server.  It will automatically "become" the user who owns the git repository when it pulls, so permissions aren't messed up, but the root user will still need to have ssh access to github.