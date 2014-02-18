#Masque
Masque is a command line tool that gives your localhost projects custom domain names such as myproject.com or awesomeapp.local.

###Installation
Download the script and create a symlink in your `~/bin` directory. You'll need root permissions to add and remove hosts. The script creates a backup of your /etc/hosts file the first time it is run so make sure you have the appropriate permissions.

###Usage
List all masque hosts:

	masque ls

Add a host:

	sudo masque add /dir/to/project/ sampleurl.com samplealias.org samplealias.net

Remove a host

	sudo masque rm sample.url

###Support
Masque was tested on Ubuntu 12.04. and Apache 2.2.22. Other configurations should also work, but have not been tested. You can manually change the localhost ip, hosts file path and apache2 sites-available path by editing the source code.

###License
MIT
