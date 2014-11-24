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
import requests, types
from Request import Request, QueryParameter, UrlParameter


class Client:
    def __init__(self, base: str):
        self.base = base
        self.request = None
        self.url = ''
        self.warnings = []

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
        return r

    def execute_with_return_type(self, request: Request, class_type):
        class TemplateClass:
            pass
        if not isinstance(class_type, type(TemplateClass)):
            raise Exception("Not a valid input for class_type. See documentation.")
        r = self.execute(request)


