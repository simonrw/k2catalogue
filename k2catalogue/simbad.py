from __future__ import with_statement, print_function
import requests
import webbrowser
import tempfile
import os

session = requests.Session()


class Simbad(object):

    URL = 'http://simbad.u-strasbg.fr/simbad/sim-coo'

    def __init__(self, epic):
        self.epic = epic

    def form_data(self, radius):
        return {
            'Coord': '{0:.2f} {1:.2f}'.format(self.epic.ra, self.epic.dec),
            'CooFrame': 'ICRS',
            'CooEpoch': '2000',
            'CooEqui': '2000',
            'CooDefinedFrames': 'none',
            'Radius': str(radius),
        }

    def send_request(self, radius=5.):
        return session.post(self.URL, data=self.form_data(radius))

    def open(self, radius=5.):
        response = self.send_request(radius)
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tfile:
            tfile.write(response.text.encode('utf-8'))
            tfile.seek(0)
            url = 'file://{0}'.format(os.path.realpath(tfile.name))
            webbrowser.open(url)
