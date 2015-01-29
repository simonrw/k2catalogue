from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    create_engine,
)
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import logging
import webbrowser
import sys

from .simbad import Simbad
from .k2logging import get_logger

logger = get_logger(__name__)

engine = create_engine('sqlite:///database.sqlite')
Base = declarative_base()
Session = sessionmaker(bind=engine)

epic_proposals = Table(
    'epic_proposals', Base.metadata,
    Column('proposal_id', Integer, ForeignKey('proposals.id')),
    Column('epic_id', Integer, ForeignKey('epics.id')))

INVALID_PROPOSALS = set('G')


def safe_float(value):
    try:
        return float(value)
    except ValueError:
        return None


class Proposal(Base):
    __tablename__ = 'proposals'

    id = Column(Integer, primary_key=True)
    proposal_id = Column(String, nullable=False, unique=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    campaign = relationship('Campaign', backref=backref('proposals',
                                                        order_by=id))
    pi = Column(String)
    title = Column(String)
    pdf_url = Column(String)

    max_title_length = 20

    def __repr__(self):
        return '<Proposal {pid}: {pi} - "{title}">'.format(
            pid=self.proposal_id, pi=self.pi, title=self.short_title)

    @property
    def short_title(self):
        if len(self.title) > self.max_title_length:
            return self.title[:self.max_title_length] + '...'
        else:
            return self.title

    @classmethod
    def create(cls, proposals, campaign, proposal_mapping):
        out = []
        for proposal in proposals:
            if cls.valid_proposal(proposal):
                try:
                    map_data = proposal_mapping[proposal.split('_')[0]]
                except KeyError:
                    logger.warning('No proposal metadata for %s', proposal)
                else:
                    out.append(cls(proposal_id=proposal, campaign=campaign,
                                   pi=map_data['pi'], title=map_data['title'],
                                   pdf_url=map_data['url']))
        return out

    def open_proposals_page(self):
        self.campaign.open_proposals_page()

    def open_proposal(self):
        if self.pdf_url:
            webbrowser.open(self.pdf_url)

    @staticmethod
    def valid_proposal(proposal):
        if proposal in INVALID_PROPOSALS:
            return False
        if '_TILE' in proposal:
            return False
        return True


class EPIC(Base):
    __tablename__ = 'epics'

    id = Column(Integer, primary_key=True)
    epic_id = Column(Integer, nullable=False)
    ra = Column(Float)
    dec = Column(Float)
    mag = Column(Float)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    campaign = relationship('Campaign', backref=backref('objects',
                                                        order_by=id))

    proposals = relationship('Proposal', secondary=epic_proposals,
                             backref='objects')

    def __repr__(self):
        return '<EPIC: {0}>'.format(self.epic_id)

    def simbad_query(self, radius=5.):
        return Simbad(self).open(radius=radius)

    @classmethod
    def create(cls, epics, campaign, proposal_map):
        out = []
        for epic in epics:
            proposal_ids = [proposal
                            for proposal in epic['investigation_ids'].split('|')
                            if Proposal.valid_proposal(proposal)]
            proposals = [proposal_map[i] for i in proposal_ids
                         if i in proposal_map]

            self = cls(epic_id=int(epic['epicid']),
                       ra=safe_float(epic['ra']),
                       dec=safe_float(epic['dec']),
                       mag=safe_float(epic['mag']),
                       proposals=proposals,
                       campaign=campaign)
            out.append(self)
        return out


class Campaign(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True)

    @property
    def proposals_page(self):
        base_url = ('http://keplerscience.arc.nasa.gov/K2/'
                    'GuestInvestigationsC{campaign:02d}.shtml')
        return base_url.format(campaign=self.id)

    def open_proposals_page(self):
        webbrowser.open(self.proposals_page)

    def __repr__(self):
        return '<Campaign: {0}>'.format(self.id)


def create_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def create_session():
    return Session()
