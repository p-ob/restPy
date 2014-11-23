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

c = Client("https://na.api.pvp.net/")
r = Request("api/lol/{region}/v1.4/summoner/by-name/{summonerNames}")
r.add_url_parameter('region', 'na')
r.add_url_parameter('summonerNames', 'drunk7irishman')
r.add_query_parameter('api_key', 'example')

u = c.execute(r)
print(u)