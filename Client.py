__author__ = 'Patrick O\'Brien'
''' COPYRIGHT 2014
    This file is part of restPy.

    restPy is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    restPy is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with restPy.  If not, see <http://www.gnu.org/licenses/>.
'''
import requests
import os
import pickle
from Request import Request, QueryParameter, UrlParameter


class Client:
    def __init__(self, base: str):
        self.base = base
        self.request = None
        self.url = ''
        self.warnings = []
        self.data = None

    def execute(self, request: Request) -> requests.Request:
        self.request = request
        url = self.base + self.request.method
        payload = {}
        for p in self.request.parameters:
            if isinstance(p, UrlParameter):
                url = url.replace('{{{0}}}'.format(p.name), p.value)  # .format() does not allow for partial formatting
            if isinstance(p, QueryParameter):
                payload[p.name] = p.value
        r = requests.get(url, params=payload)
        self.data = r.content
        return r

    def execute_with_return_struct(self, request: Request, write_struct_to_txt: bool=False, txt_filename: str='', txt_folder: str=''):
        r = self.execute(request)
        content_type = r.headers["content-type"]
        if 'json' in content_type:
            self.data = self.__json2object(r.json())
            if write_struct_to_txt:
                if txt_filename is '':
                    file_number = 0
                    txt_filename = 'struct{0}.txt'
                    while os.path.isfile(txt_folder + txt_filename.format(file_number)):
                        file_number += 1
                    txt_filename = txt_filename.format(file_number)
            if '.txt' not in txt_filename:
                txt_filename += '.txt'
            with open(txt_folder + txt_filename, 'wb') as f:
                pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)

        elif 'xml' in content_type:
            self.data = self.__xml2object(r.data)
        else:
            self.data = r.data
        return self.data

    def __json2object(self, json_data):
        s = Struct(**json_data)
        data_members = (d for d in s.__dir__() if '__' not in d)
        for data_member in data_members:
            if isinstance(getattr(s, data_member, None), dict):
                setattr(s, data_member, self.__json2object(getattr(s, data_member)))

        return s

    @staticmethod
    def __xml2object(content):
        return content


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)