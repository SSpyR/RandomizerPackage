#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2019-2020 Christopher J. Kucera
# <cj@apocalyptech.com>
# <http://apocalyptech.com/contact.php>
#
# Borderlands 3 Data Library is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# Borderlands 3 Data Library is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Borderlands 3 Data Library.  If not, see
# <https://www.gnu.org/licenses/>.

# Adjusted and stripped down version of original file by SSpyR

import os
import re
import json
import glob
import appdirs
#import pymysql
#pymysql.install_as_MySQLdb()
#import MySQLdb
import subprocess
#import configparser

from bl3hotfixmod import BVC

class BL3Data(object):
     # Data serialization version requirements
    data_version = 7

    # Hardcoded BVA values
    bva_values = {
            }

    # Hardcoded part-category values
    cats_shields = [
            'BODY',
            'RARITY',
            'LEGENDARY AUG',
            'AUGMENT',
            'ELEMENT',
            'MATERIAL',
            ]

    cats_grenades = [
            'MANUFACTURER',
            'ELEMENT',
            'RARITY',
            'AUGMENT',
            'BEHAVIOR',
            'MATERIAL',
            ]

    cats_coms = [
            'CHARACTER',
            'MODTYPE',
            'RARITY',
            'PRIMARY',
            'SECONDARY',
            'SKILLS',
            '(unknown)',
            ]

    cats_artifacts = [
            'RARITY',
            'LEGENDARY ABILITY',
            'ABILITY',
            'PRIMARY',
            'SECONDARY',
            ]

    def __init__(self):
        """
        Initialize a BL3Data object.  Will create a sample config file if one
        is not already found.  Will require that the "filesystem" section be
        properly filled in, or we'll raise an exception.
        """

        # config_dir = appdirs.user_config_dir('bl3data')

        # # Create the config dir if it doesn't exist
        # if not os.path.exists(config_dir):
        #     os.makedirs(config_dir, exist_ok=True)

        # # Create a sample INI file it if doesn't exist
        # self.config_file = os.path.join(config_dir, 'bl3data.ini')
        # if not os.path.exists(self.config_file):
        #     dir=os.path.dirname(__file__)
        #     config = configparser.ConfigParser()
        #     config['filesystem'] = {
        #             'data_dir': os.path.join(dir, '/utils'),
        #             'ueserialize_path': os.path.join(dir, '/utils/john-wick-parse.exe'),
        #             }
        #     with open(self.config_file, 'w') as odf:
        #         config.write(odf)
        #     print('Created sample config file {}'.format(self.config_file))

        # # Read in the config file and at least make sure we have filesystem
        # # data available
        # self.config = configparser.ConfigParser()
        # self.config.read(self.config_file)
        # self._enforce_config_section('filesystem')

        # Convenience var
        dir=os.path.dirname(__file__)
        self.data_dir = os.path.join(dir, '/utils')
        self.ueserialize_path = os.path.join(dir, '/utils/john-wick-parse.exe')

        # Now the rest of the vars we'll use
        self.cache = {}
        self.balance_to_extra_anoints = None
        self.db = None
        self.curs = None
    
    def get_data(self, obj_name):
        """
        Returns a JSON-serialized version of the object `obj_name`, if possible.
        May return None, either due to the object not existing, or if JohnWickParse
        can't actually produce a serialization for the object.  Results will be
        cached, so requesting the same object more than once will not result in
        re-parsing JSON content.
        """
        if obj_name not in self.cache:

            dir=os.path.dirname(__file__)
            base_path = '{}{}'.format(dir, '/utils'+str.rstrip(obj_name))
            json_file = '{}.json'.format(base_path)
            print(json_file)
            if not os.path.exists(json_file):
                # PyPy3 is still on 3.6, which doesn't have capture_output
                #subprocess.run([self.config['filesystem']['ueserialize_path'], base_path], encoding='utf-8', capture_output=True)
                subprocess.run([self.ueserialize_path, base_path], encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if os.path.exists(json_file):
                with open(json_file) as df:
                    self.cache[obj_name] = json.load(df)
                if len(self.cache[obj_name]) > 0:
                    if '_apoc_data_ver' not in self.cache[obj_name][0] or self.cache[obj_name][0]['_apoc_data_ver'] < BL3Data.data_version:
                        # Regenerate if we have an old serialization
                        subprocess.run([self.ueserialize_path, base_path], encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        with open(json_file) as df:
                            self.cache[obj_name] = json.load(df)
            else:
                self.cache[obj_name] = None

        return self.cache[obj_name]

    def get_exports(self, obj_name, export_type):
        """
        Given an object `obj_name`, return a list of serialized exports which match
        the type `export_type`.
        """
        exports = []
        data = self.get_data(obj_name)
        if data:
            for export in data:
                if export['export_type'] == export_type:
                    exports.append(export)
        return exports