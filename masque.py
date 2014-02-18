#! /usr/bin/env python

import argparse, os, re, glob

class Masque:

	hosts 		= '/etc/hosts'
	ap2 		= '/etc/apache2/sites-available/'
	localhost 	= '127.0.0.1'

	def __init__(self):
		parser = argparse.ArgumentParser(description='Create, list and destroy virtual hosts on Apache2.')

		parser.add_argument('action', help='action you want to perform', choices=['rm', 'add', 'ls'], type=str)
		parser.add_argument('args', help='arguments to pass to your action', type=str, nargs='*')
		args = parser.parse_args()

		self.backup()

		if args.action == 'ls':
			self.list()
		elif args.action == 'add':
			self.add(args.args)	
		elif args.action == 'rm':
			self.rm(args.args)

	def backup(self):
		realdir = os.path.dirname( os.path.realpath(__file__) )
		backup 	= os.path.join(realdir, 'hosts')

		if os.path.exists(backup) == False:
			try: 
				hosts = open(self.hosts, 'r').read()
				open(backup, 'w').write(hosts)
			except:
				print 'Could not backup hosts file, aborting. Please check your read permissions for %s and your write permissions for %s.'%(self.hosts, backup)
				sys.exit(0)	

	def list(self):
		domains = glob.glob(self.ap2+"Masque.*")
		hosts 	= open(self.hosts, 'r').readlines() 
		ls 		= []

		if domains:
			for domain in domains:
				string 		= open(domain, 'r').read()
				domain 		= re.search('ServerName (.+?)\n', string).group(1)
				directory 	= re.search('DocumentRoot (.+?)\n', string).group(1)
				aliases 	= re.findall('ServerAlias (.+)\n', string, re.MULTILINE) if 'ServerAlias' in string else []

				print '\033[92m%s\033[0m-> %s %s'% (directory, domain, ' '.join(aliases))

		else:	
			print 'No domains found.'

	def _hosts(self, lines = None):
		if lines == None:
			hosts = open(self.hosts, 'r')
			lines = hosts.readlines()
			return lines
		else:
			try:
				hosts = open(self.hosts, 'w')
				hosts.write(''.join(lines))
			except IOError:
				print 'You do not have write permissions for %s.'%self.hosts
				return False

			return True	

	def removeDomainFromHosts(self, pattern):
		hosts = self._hosts()
		index = [i for i, domain in enumerate(hosts) if pattern in domain]
		hosts = [line for n, line in enumerate(hosts) if n not in index]
		self._hosts(hosts)

	def rm(self, domains):
		while domains:
			domain 		= domains.pop()
			filename 	= 'Masque.%s'%domain
			path 		= os.path.join(self.ap2, filename)

			if os.path.exists(path) == False:
				print 'File "%s" does not exist. Only domains can be deleted, not aliases. Use masque ls to list all domains. '%(path)
			else:
				try:
					os.system( 'rm %s && a2dissite %s && service apache2 reload'%(path, filename) )
					self.removeDomainFromHosts(domain)		

				except IOError:
					print 'Permission denied, are you sure you\'re running sudo?'

	def add(self, args):
		if len(args) < 2:
			print 'Invalid argument combo - masque add requires at least two arguments'
		else:
			path 	= os.path.abspath(args[0])
			domain 	= args[1]
			aliases = args[2:]

			filepath 	= '%sMasque.%s'%(self.ap2, domain) #Path to virtualhost file in sites-available
			hosts 		= '%s %s \n'%( self.localhost, ' '.join(args[1:]) ) #Line in hosts file
			commands 	= 'a2ensite Masque.%s && service apache2 reload'%domain #Reload apache2
			apache 		= """<VirtualHost *:80>
				ServerAdmin webmaster@example.com
				ServerName %(domain)s
				%(aliases)s
				DocumentRoot %(path)s 
				</VirtualHost>""".replace('\t', '')%{'path' : path.replace(' ', ''), 'domain' : domain, 'aliases' : '\n'.join('ServerAlias %s'% alias for alias in aliases)}

			try:
				self.removeDomainFromHosts(domain) #Removes duplicates		
				open(filepath, 'w').write(apache)

				if hosts not in open(self.hosts, 'r').read():
					open(self.hosts, 'a').write(hosts)

				os.system(commands)
			except IOError:
				print 'Permission denied, are you sure you\'re running sudo?'

Masque()		