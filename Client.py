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
from .METHOD import METHOD


class ClientException(Exception):
    pass


class Client:
    def __init__(self, base: str):
        self.base = base
        self.request = None
        self.url = ''
        self.warnings = []
        self.data = None

    def execute(self, request: Request) -> requests.Request:
        self.request = request
        url = self.base + self.request.resource
        payload = {}
        for p in self.request.parameters:
            if isinstance(p, UrlParameter):
                url = url.replace('{{{0}}}'.format(p.name), p.value)  # .format() does not allow for partial formatting
            elif isinstance(p, QueryParameter):
                payload[p.name] = p.value
        if request.method == METHOD.GET:
            r = requests.get(url, params=payload)
            self.data = r.content
        elif request.method == METHOD.PUT:
            r = requests.put(url, params=payload)
            self.data = r.content
        elif request.method == METHOD.POST:
            r = requests.post(url, params=payload)
            self.data = r.content
        elif request.method == METHOD.DELETE:
            r = requests.delete(url, params=payload)
            self.data = r.content
        elif request.method == METHOD.HEAD:
            r = requests.head(url, params=payload)
            self.data = r.content
        elif request.method == METHOD.OPTIONS:
            r = requests.options(url, params=payload)
            self.data = r.content
        else:
            raise ClientException("No valid method given for request.")

        r.raise_for_status()
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
            return self.data, self.data.get_data_members()
        return self.data

    def __dict2object(self, json_data):
        s = Struct(**json_data)
        data_members = [d for d in s.__dir__() if '__' not in d]
        for data_member in data_members:
            if isinstance(getattr(s, data_member, None), dict):
                setattr(s, data_member, self.__dict2object(getattr(s, data_member)))
            elif isinstance(getattr(s, data_member, None), list):
                for i in range(0, len(getattr(s, data_member, None))):
                    if isinstance(getattr(s, data_member, None)[i], dict):
                        getattr(s, data_member)[i] = self.__dict2object(getattr(s, data_member)[i])

        return s


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __repr__(self):
        data_members = self.get_data_members()
        return str([(data_member, getattr(self, data_member, None)) for data_member in data_members])

    def get_data_members(self):
        data_members = [d for d in self.__dir__() if '__' not in d and d != 'get_data_members']
        '''
        # commented out code below would yield ALL data_members for all Structs contained by this Struct
        for i in range(0, len(data_members)):
            if isinstance(getattr(self, data_members[i], None), Struct):
                data_members[i] = {data_members[i]: getattr(self, data_members[i]).get_data_members()}
        '''
        return data_members
