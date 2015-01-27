#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import argparse
import requests
from sqlalchemy import func
import vcr
import csv
import IPython
from functools import partial

from .models import (create_database,
                     create_session,
                     Proposal,
                     Campaign,
                     EPIC)
from .proposal_urls import BuildCampaignMapping
from .k2logging import get_logger

logger = get_logger(__name__)

# Disable third party logging information
get_logger('vcr.stubs').setLevel('WARNING')
get_logger('requests.packages.urllib3.connectionpool').setLevel(
    'WARNING')


requests_session = requests.Session()

COLUMN_NAMES = ['epicid', 'ra', 'dec', 'mag', 'investigation_ids']
FIELD_0_COLUMN_NAMES = ['epicid', 'ra', 'dec', 'mag', 'cadence',
                        'investigation_ids']


def fetch_csv(campaign):
    logger.info('Querying for information from campaign %s', campaign)
    url = ('http://keplerscience.arc.nasa.gov/'
           'K2/docs/Campaigns/C{campaign}/'
           'K2Campaign{campaign}targets.csv')
    with vcr.use_cassette('.cassettes/campaign{campaign}.yml'.format(
            campaign=campaign)):
        response = requests_session.get(url.format(campaign=campaign))
        csv_content = response.text.replace('\n', '\r').split('\r')

    reader = csv.DictReader(csv_content, delimiter=',',
                            fieldnames=FIELD_0_COLUMN_NAMES if campaign == 0
                            else COLUMN_NAMES)
    # Remove the header row
    next(reader)
    all_data = list(reader)
    proposals = set([
        item for sublist in
        [map(lambda s: s.strip(),
             row['investigation_ids'].split('|')) for row in all_data]
        for item in sublist])

    logger.info('Found %s objects and %s proposals',
                len(all_data), len(proposals))
    return (all_data, proposals)


def setup():
    create_database()
    session = create_session()
    for campaign in 0, 1, 2:
        c = Campaign(id=campaign)
        proposal_url_builder = BuildCampaignMapping(campaign=campaign)
        session.add(c)
        data = fetch_csv(campaign=campaign)
        proposals = Proposal.create(data[1], c, proposal_url_builder.create())
        session.add_all(proposals)
        epics = EPIC.create(data[0], c, {
            proposal.proposal_id: proposal for proposal in proposals
        })
        session.add_all(epics)
        session.commit()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--setup', action='store_true')
    return parser.parse_args()

# Top level api for the user


def get_by_epicid(epicid, session):
    return session.query(EPIC).filter(EPIC.epic_id == epicid).first()


def get_by_proposal(proposal_id, session):
    return session.query(Proposal).filter(
        Proposal.proposal_id == proposal_id).first()


def main():
    args = parse_args()
    if args.setup:
        setup()

    session = create_session()

    IPython.start_ipython(user_ns={
        'session': session,
        'get_by_epicid': partial(get_by_epicid, session=session),
        'get_by_proposal': partial(get_by_proposal, session=session),
        'func': func,
        'count': func.count,
        'Proposal': Proposal,
        'Campaign': Campaign,
        'EPIC': EPIC,
        'get_logger': get_logger,
    }, argv=[])
