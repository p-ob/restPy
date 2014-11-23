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


class Request:
    def __init__(self, method: str):
        self.method = method
        self.parameters = []

    def add_url_parameter(self, name: str, value):
        self.parameters.append(UrlParameter(name, value))

    def add_query_parameter(self, name: str, value):
        self.parameters.append(QueryParameter(name, value))


class Parameter:
    def __init__(self, name, value):
        self.name = name
        self.value = str(value)


class UrlParameter(Parameter):
    def __init__(self, name: str, value):
        super().__init__(name, value)


class QueryParameter(Parameter):
    def __init__(self, name, value):
        super().__init__(name, value)

