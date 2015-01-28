from __future__ import with_statement, print_function
import vcr
import requests
from bs4 import BeautifulSoup
import os


class BuildCampaignMapping(object):
    root_url = 'http://keplerscience.arc.nasa.gov/K2'

    def __init__(self, campaign):
        self.campaign = campaign

    @property
    def url(self):
        return os.path.join(self.root_url,
                            'GuestInvestigationsC{0:02d}.shtml'.format(
                                self.campaign))

    @property
    def response(self):
        with vcr.use_cassette(
                '.cassettes/proposals{0:02d}.yml'.format(self.campaign)):
            return requests.get(self.url)

    @property
    def soup(self):
        return BeautifulSoup(self.response.text)

    @property
    def table(self):
        return self.soup.find('table', attrs={'class': 'standard'})

    @property
    def table_rows(self):
        return self.table.find_all('tr')

    def extract_contents(self, row):
        entries = row.find_all('td')
        if len(entries):
            try:
                proposal_id = entries[0].string.strip()
                pi = entries[1].string.strip()
                title = entries[2].string.strip()
                pdf_url = os.path.join(self.root_url, entries[-1].a['href'])
                return (proposal_id, pi, title, pdf_url)
            except AttributeError:
                return None

    def create(self):
        mapping = {}
        for row in self.table_rows:
            try:
                proposal_id, pi, title, pdf_url = self.extract_contents(row)
            except TypeError:
                pass
            else:
                mapping[proposal_id] = {
                    'pi': pi,
                    'title': title,
                    'url': pdf_url,
                }

        return mapping
