from netweaver.core_classes.config_object import ConfigObject
import unittest
from netweaver.server_config_loader import get_server_config
from importlib.machinery import SourceFileLoader
from .errors import *




class Appliance(ConfigObject):

	def __init__(self, name, appliance_dict):
		self.name = name
		self.config = appliance_dict
		self.fabric = None
		self.role = None
		self.plugin = None

		self.dtree = None

	def _not_implemented(self):
		return "Not implemented"

	def load_plugin(self):
		'''
		:return: plugin initialized with self.config, error otherwise (e.g. incompatible with config, plugin not found..).
		'''
		path = self.get_plugin_path()
		package = SourceFileLoader('package', '{}/{}'.format(path, '__init__.py')).load_module()
		module = SourceFileLoader('module', '{}/{}'.format(path, package.information['module_name'])).load_module()
		plugin = getattr(module, package.information['class_name'])
		# return plugin(self.config)
		self.plugin = plugin(self.config, self.fabric.config)
		self._build_dispatch_tree()
		self.plugin.appliance = self

	def _build_dispatch_tree(self):
		self.dtree = {
			'state': {
				'apply': self.plugin.push_state,
				'get': self.plugin.cstate,
			},
			'hostname': {
				'set': self.plugin.set_hostname,
				'get': self.plugin.get_hostname,
			},
			'protocols': {
				'ntp': {
					'client':
						{
							'timezone':{
								'get': self.plugin.cstate['protocols']['ntp']['client']['timezone'],
								'set': self.plugin.set_ntp_client_timezone
							},
							'servers':{
								'add': self.plugin.add_ntp_client_server,
								'get': self.plugin.cstate['protocols']['ntp']['client']['servers'],
								'del': self.plugin.rm_ntp_client_server,
								'set': self.plugin.set_ntp_client_servers
							},
							'get': self.plugin.cstate['protocols']['ntp']['client'],
						}
				},
				'vlans':{
					'get': self.plugin.cstate['vlans'],
					'set': self.plugin.set_vlans,
					'add': self.plugin.add_vlan
				},
				'dns': {
					'get': self.plugin.cstate['protocols']['dns'],
					'nameservers': {
						'get': self.plugin.cstate['protocols']['dns']['nameservers'],
						'set': self.plugin.set_dns_nameservers,
						'add': self.plugin.add_dns_nameserver,
						'del': self.plugin.rm_dns_nameserver
					}
				}
			},
			'interface': {
				'1g': {
					'get': self._not_implemented,
					'set': self._not_implemented,
				}
			}
		}

	def get_plugin_path(self):
		try:
			return '{}/{}'.format(get_server_config()['plugin_path'], self.config['plugin_package'])
		except KeyError:
			raise NonExistantPlugin()

	def __repr__(self):
		return '<Appliance: {}>'.format(self.name)

	def run_individual_command(self, func, value):
		# if func == 'get.hostname':
		# 	return self.plugin.get_hostname()
		# if func == 'set.hostname':
		# 	return self.plugin.set_hostname(value)
		sfunc = func.split('.')
		"""
		Iterate through each level of the config and stop when you get to a command (get, set, etc.)
		"""
		level = self.dtree
		for com in sfunc:
			if com == 'get' or com == 'apply':
				# TODO: Make this cleaner, the TypeError check on type-ing a string shouldn't be necesarry
				# try:
					if type(level[com]) is dict:
						return level[com]
					else:
						return level[com]()
				# except TypeError:
				# 	return level[com]
			elif com == 'set' or com == 'add':
				return level[com](value)
			else:
				level = level[com]


class TestPluginLoader(unittest.TestCase):
	def test_plugin_loader(self):
		mock = {
					'hostname': '10.0.0.1',
					'role': 'spine1',
					'plugin_package': 'cumulus'
				}
		appl = Appliance("00-00-00-00-00-00",  mock)
		inst = appl.load_plugin()
		self.assertEqual(inst.is_plugin(), True)


if __name__ == '__main__':
	unittest.main()