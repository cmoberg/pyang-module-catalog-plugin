"""YANG module catalog data generator
"""
from __future__ import print_function

import optparse
import sys
import re
import string
import logging

import types
import StringIO

import json

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
            	default='xml',
            	help = 'Swagger debug'),
            ]

        g = optparser.add_option_group("YANG Module Schema-specific options")
        g.add_options(optlist)

    def setup_ctx(self, ctx):
        ctx.opts.stmts = None

    def setup_fmt(self, ctx):
        ctx.implicit_errors = False

    def print_json(self, data):
        print(json.dumps(data))

    def print_xml(self, data):
        pass

    def emit(self, ctx, modules, fd):
		me = ModuleCatalogEmitter()
		result = me.emit(ctx, modules)
		# print(result)
		if ctx.opts.outputFormat == 'json':
			self.print_json(result)
		else:
			print_xml(result)

class ModuleCatalogEmitter(object):
	def emit(self, ctx, modules):
		res = {}
		for module in modules:

		# Here are the top-level leafs from the draft:
		# +--rw name                string -> is the 'module' statement
		# +--rw namespace?          string DONE
		# +--rw prefix?             string DONE
		# +--rw revision?           string DONE
		# +--rw summary?            string -> Can't be inferred from module
		# +--rw module-version?     string -> Can't be inferred from module

			res['name'] = module.arg
			for statement in ['namespace', 'prefix', 'revision', 'module-version']:
				stmt = module.search_one(statement)
				if stmt:
					if statement == 'module':
						res['name'] = stmt.arg
					else:
						res[stmt.keyword] = stmt.arg
			return res

