import os
import json
import socket
import urllib2
import optparse

GOOGLE_DNS = "8.8.8.8"
OPEN_DNS = "208.67.222.222"
DNS_PORT = 53

def internet_accessible():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1)
	return_code = s.connect_ex((GOOGLE_DNS, DNS_PORT))

	if return_code > 0:
		return_code = s.connect_ex((OPEN_DNS, DNS_PORT))

	return return_code == 0

class NamecheapDDNS:
	getip_url = "http://dynamicdns.park-your-domain.com/getip"

	def __init__(self, domain, ddns_password, debug=False, cache_file=None):
		self.domain = domain.lower()
		self.ddns_password = ddns_password
		self.debug = debug
		self.cache_file = cache_file

		if not self.cache_file:
			self.cache_file = "/tmp/namecheap_ddns.cache"

	def get_request_url(self, host, ip):
		return "https://dynamicdns.park-your-domain.com/update?host={host}&domain={domain}&password={ddns_password}&ip={ip}".format(**{
			"host": host,
			"ip": ip,
			"domain": self.domain,
			"ddns_password": self.ddns_password
		})

	def get_records(self):
		records = {}
		if os.path.exists(self.cache_file):
			with open(self.cache_file, 'r') as f:
				records = json.loads(f.read() or "{}")
			f.close()

		return records

	def set_records(self, records=None):
		if not isinstance(records, dict):
			records = {}

		with open(self.cache_file, 'w') as f:
			f.write(json.dumps(records))

		f.close()

	def update(self, host, ip=None):
		host = host.lower()
		name = "{}.{}".format(host, self.domain)
		records = self.get_records()

		if not ip:
			self.printmsg("No ip provided. Looking up...")
			ip = urllib2.urlopen(self.getip_url).read()
			self.printmsg("Got ip {}".format(ip))

		if records.get(name) == ip:
			self.printmsg ("Host \"{}\" did not change ip. Skipped.".format(host))
			return None

		self.printmsg ("Setting ip \"{}\" for host \"{}\".".format(ip, host))

		records[name] = ip
		self.set_records(records)

		url = self.get_request_url(host, ip)
		self.printmsg ("Connecting {}".format(url))

		return urllib2.urlopen(url).read()

	def printmsg(self, msg):
		if self.debug:
			print (msg)

def main():
	parser = optparse.OptionParser(prog="namecheap_ddns", description="Cli for Namecheap Dynamic DNS class.")
	parser.add_option("", "--domain", help="Your domain name.")
	parser.add_option("", "--password", help="Dynamic DNS password.")
	parser.add_option("", "--host", help="Host name.")
	parser.add_option("", "--ip", help="Ip address to set to.")
	parser.add_option("", "--debug", help="Enable debug mode", default=False)

	(options, args) = parser.parse_args()

	if not options.domain or not options.password or not options.host:
		parser.error("Either domain, password and host are required.")

	if internet_accessible():
		n = NamecheapDDNS(options.domain, options.password, options.debug)
		n.update(options.host, options.ip)
	else:
		print ("You are offline.")

if __name__ == '__main__':
	main()
