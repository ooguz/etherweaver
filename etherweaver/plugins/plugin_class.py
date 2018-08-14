from paramiko import SSHClient, WarningPolicy
from enum import IntEnum
from etherweaver.plugins.plugin_class_errors import *

class NWConnType(IntEnum):
	Telnet = 1
	SSH = 2
	RS232 = 3


class NetWeaverPlugin:
	protocol = None
	hostname = None
	commands = []

	def _ssh_request(self):
		"""Make an ssh request and parse returncode"""

	def add_command(self, commands):
		if type(commands) == list:
			for com in commands:
				self.commands.append(com)
		elif commands is None:
			return
		else:
			self.commands.append(commands)

	def build_ssh_session(self):
		self.conn_type = NWConnType
		self.ssh = self._build_ssh_client(
			hostname=self.appliance.dstate['connections']['ssh']['hostname'],
			username=self.appliance.dstate['connections']['ssh']['username'],
			password=self.appliance.dstate['connections']['ssh']['password'],
			port=self.port
		)

	def _build_ssh_client(self, hostname=None, accept_untrusted=False, username=None, password=None, port=22):
		"""Returns a paramiko ssh client object"""
		ssh = SSHClient()
		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(WarningPolicy)
		ssh.connect(hostname=hostname, port=port, username=username, password=password)
		return ssh

	def _ssh_command(self, command):
		stdin, stdout, stderr = self.ssh.exec_command(command)
		if stderr.read():
			raise SSHCommandError("While running command {} on appliance {}, got error {} {}".format(command, self.hostname, stderr.read(), stdout.read())) #TODO For some reason this line returns empty on error when run from a child instance
		return stdout.read().decode('utf-8')

	def _generic_command(self, command):
		if self.protocol == 2:
			return self._ssh_command(command)

	def _not_supported(self, feature):
		raise FeatureNotSupported(self.__repr__(), feature)

	def _not_implemented(self):
		raise FeatureNotImplemented

	def define_port_layout(self):
		self._not_supported('port_layout')

	def pre_push(self):
		self._not_implemented()
	"""Override these functions to enable each feature"""

	def get_hostname(self):
		self._not_supported('get_hostname')

	def set_hostname(self, hostname, execute=True):
		self._not_supported('set_hostname')

	def get_current_config(self):
		self._not_supported('get_current_config')

	def get_interface(self, speed, interface):
		self._not_supported('get_interface')

	def get_dns(self):
		self._not_supported('get_dns')

	def get_dns_nameservers(self):
		self._not_supported('get_dns_nameservers')

	def set_dns_nameservers(self, nameserverlist, execute=True):
		self._not_supported('set_dns_nameservers')

	def add_dns_nameserver(self, ip, execute=True):
		self._not_supported('add_dns_nameserver')

	def rm_dns_nameserver(self, ip, execute=True):
		self._not_supported('rm_dns_nameserver')

	def pull_state(self):
		self._not_supported('pull_state')

	def push_state(self, execute=True):
		self._not_supported('push_state')

	def set_ntp_client_timezone(self, timezone, execute=True):
		self._not_supported('set_ntp_client_timezone')

	def add_ntp_client_server(self, ntpserver, execute=True):
		self._not_supported('add_ntp_client_server')

	def rm_ntp_client_server(self, ntpserver, execute=True):
		self._not_supported('rm_ntp_client_server')

	def set_ntp_client_servers(self, ntpserverlist, execute=True):
		self._not_supported('set_ntp_client_servers')

	def set_interface_config(self, interfaces, profile=None, execute=True):
		self._not_supported('set_interface_config')

	def set_vlans(self, vlans, execute=True):
		self._not_supported('set_vlans')

	def add_vlan(self, vlan, execute=True):
		self._not_supported('add_vlan')

	def rm_vlan(self, vlan, execute=True):
		self._not_supported('rm_vlan')

	def set_interface_tagged_vlans(self, interface, vlans, execute=True):
		self._not_supported('set_interface_tagged_vlans')

	def add_interface_tagged_vlan(self, interface, vlan, execute=True):
		self._not_supported('add_interface_tagged_vlan')

	def rm_interface_tagged_vlan(self, interface, vlan, execute=True):
		self._not_supported('rm_interface_tagged_vlan')

	def set_interface_untagged_vlan(self, interface, vlan, execute=True):
		self._not_supported('set_interface_untagged_vlan')

	def rm_interface_untagged_vlan(self, interface, execute=True):
		self._not_supported('rm_interface_untagged_vlan')