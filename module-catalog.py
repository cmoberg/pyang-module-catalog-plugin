"""YANG module catalog data generator
"""
from __future__ import print_function

import optparse
import sys
import string
import logging
import types
import StringIO
import json
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring

from pyang import plugin
from pyang import statements
from pyang import util

def pyang_plugin_init():
	plugin.register_plugin(ModuleCatalogPlugin())

class ModuleCatalogPlugin(plugin.PyangPlugin):

	def add_output_format(self, fmts):
		fmts['module-catalog'] = self

	def add_opts(self, optparser):
		optlist = [
			optparse.make_option('--module-catalog-format',
				type = 'choice',
				dest = 'outputFormat',
				choices=['xml', 'json'],
				default='json')
			]

		g = optparser.add_option_group("YANG Module Catalog-specific options")
		g.add_options(optlist)

	def setup_ctx(self, ctx):
		ctx.opts.stmts = None

	def setup_fmt(self, ctx):
		ctx.implicit_errors = False

	def print_json(self, data):
		js = { "module" : data }
		print(json.dumps(js))

	def print_xml(self, data):
		xml = dict_to_xml("module", data)
		print(tostring(xml))

	def emit(self, ctx, modules, fd):
		me = ModuleCatalogEmitter()
		result = me.emit(ctx, modules)
		if ctx.opts.outputFormat == 'json':
			self.print_json(result)
		else:
			# self.print_xml(result)
			print("XML not supported yet")

class ModuleCatalogEmitter(object):
	def emit(self, ctx, modules):
		res = {}
		for module in modules:
			res['revision'] = util.get_latest_revision(module)
			res['name'] = module.arg
			for statement in ['namespace', 'prefix', 'revision', 'module-version', 'import']:
				stmt = module.search_one(statement)
				if stmt:
					if statement == 'import':
						if 'dependencies' not in res:
							res['dependencies'] = {}
							res['dependencies']['required-module'] = []
						res['dependencies']['required-module'].append(stmt.arg)
					else:
						res[stmt.keyword] = stmt.arg
		return res
