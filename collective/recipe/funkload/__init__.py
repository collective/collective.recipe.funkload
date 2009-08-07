# -*- coding: utf-8 -*-
from zc.recipe.egg import Scripts
from z3c.recipe.egg import Setup

SCRIPT_TEMPLATE = """"""

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

        self._recipes = []

        options_funkload = options.copy()
        if 'initialization' in options_funkload:
            del options_funkload['initialization']
        if 'python' in options_funkload:
            del options_funkload['python']
        options_funkload['eggs'] = 'docutils\nfunkload'
        self._recipes.append(Scripts(buildout,name,options_funkload))
            
        
        test_address = self.options.get('address')
        if not test_address:
            if 'instance' in self.buildout:
                test_address = self.buildout['instance'].get('http-address')
        if not test_address:
            raise KeyError, "You must specify an address to test"
                
        self.filename = self.options.get('filename','funkload')
                
    def install(self):
        """Installer"""
        result = []
        for recipe in self._recipes:
            result.extend(recipe.install())
        
        bin_dir = self.buildout["buildout"]["bin-directory"]
        
        
        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return tuple(result)

    def update(self):
        """Updater"""
        for recipe in self._recipes:
            recipe.update()
