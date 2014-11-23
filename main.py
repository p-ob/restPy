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
from Client import Client
from Request import Request

c = Client('www.example.com')
r = Request('api/{test}')
r.add_url_parameter('tes', 'na')
r.add_query_parameter('test', 2)
r.add_query_parameter('a', 1)

u = c.execute(r)
print(u)