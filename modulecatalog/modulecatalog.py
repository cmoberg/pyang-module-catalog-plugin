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
import xml
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
        self.multiple_modules = True

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
        print(json.dumps(js, indent=4, sort_keys=True))

    def print_xml(self, data):
        print("XML not implemented yet")
        # xmldata = xml.dict_to_xml("module", data)
        # print(tostring(xmldata))

    def emit(self, ctx, modules, fd):
        me = ModuleCatalogEmitter()
        result = me.emit(ctx, modules)
        if ctx.opts.outputFormat == 'xml':
            self.print_xml(result)
        else:
            self.print_json(result)

class ModuleCatalogEmitter(object):
    def module_revision(self, module_name, modules):
        for module in modules:
            if module_name != module.arg:
                continue
            stmt = module.search_one('revision')
            #if stmt and stmt.arg:
            if stmt:
                return stmt.arg
            break
        return None

    def emit(self, ctx, modules):
        module_output = {}
        for module in modules:
            res = {}
            res['revision'] = util.get_latest_revision(module)
            res['name'] = module.arg
            for statement in ['namespace', 'prefix', 'revision', 'module-version']:
                stmt = module.search_one(statement)
                if stmt:
                    res[stmt.keyword] = stmt.arg

            istmts = module.search('import')
            if istmts:
                if 'dependencies' not in res:
                    res['dependencies'] = {}
                    res['dependencies']['required-module'] = []
                    for istmt in istmts:
                        # res['dependencies']['required-module'].append(istmt.arg)
                        # TODO: Need to ask draft authors to add revision-date to YANG
                        revision = self.module_revision(istmt.arg, modules)
                        if revision is None:
                            r = istmt.search_one('revision-date')
                            if r is not None:
                              revision = r.arg
                        if revision is None:
                            revision = 'unknown'
                        res['dependencies']['required-module'].append({'module-name': istmt.arg,'module-revision': revision})

            if module.keyword == 'submodule':
                if 'module-hierarchy' not in res:
                    res['module-hierarchy'] = {}
                    res['module-hierarchy']['module-hierarchy-level'] = 2
                    belongs = module.search_one('belongs-to')
                    res['module-hierarchy']['module-parent'] = belongs.arg

            module_output[module.arg] = res

        return module_output

