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
import xmltodict
from .Request import Request, QueryParameter, UrlParameter


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
        if r.status_code != 200:
            raise Exception("Error in making API call.")
        return r

    def execute_with_return_struct(self, request: Request, write_struct_to_txt: bool=False, txt_filename: str='',
                                   txt_folder: str='', return_data_members: bool=False):
        r = self.execute(request)
        content_type = r.headers["content-type"]
        if 'json' in content_type:
            self.data = self.__dict2object(r.json())
        elif 'xml' in content_type:
            self.data = self.__dict2object(xmltodict.parse(r.data))
        else:
            self.data = r.data

        if write_struct_to_txt and isinstance(self.data, Struct):
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

        if return_data_members and isinstance(self.data, Struct):
            return self.data, self.__get_data_members(self.data)
        return self.data

    def __dict2object(self, json_data):
        s = Struct(**json_data)
        data_members = (d for d in s.__dir__() if '__' not in d)
        for data_member in data_members:
            if isinstance(getattr(s, data_member, None), dict):
                setattr(s, data_member, self.__dict2object(getattr(s, data_member)))

        return s

    def __get_data_members(self, struct):
        data_members = [d for d in struct.__dir__() if '__' not in d]
        for i in range(0, len(data_members)):
            if isinstance(getattr(struct, data_members[i], None), Struct):
                data_members[i] = {data_members[i]: self.__get_data_members(getattr(struct, data_members[i]))}
        return data_members


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)