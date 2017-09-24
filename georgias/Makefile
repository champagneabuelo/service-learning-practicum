syncdb:
	@echo Downloading the DB from the course server...
	@ssh georgias@pegasus.cs.virginia.edu 'mysqldump slp_georgias_test | gzip -9c -' | gzip -dc | mysql slp_georgias_test

publish:
	rsync -C --exclude 'georgias/settings.py' --del --progress -a ./ georgias@pegasus.cs.virginia.edu:~/georgias/
