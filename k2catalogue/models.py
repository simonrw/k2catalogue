from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import logging

from .simbad import Simbad

logger = logging.getLogger('models')

engine = create_engine('sqlite:///database.sqlite')
Base = declarative_base()
Session = sessionmaker(bind=engine)

epic_proposals = Table(
    'epic_proposals', Base.metadata,
    Column('proposal_id', Integer, ForeignKey('proposals.id')),
    Column('epic_id', Integer, ForeignKey('epics.id')))


def safe_float(value):
    try:
        return float(value)
    except ValueError:
        return None


class Proposal(Base):
    __tablename__ = 'proposals'

    id = Column(Integer, primary_key=True)
    proposal_id = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return '<Proposal: {}>'.format(self.proposal_id)

    @classmethod
    def create(cls, proposals):
        out = []
        for proposal in proposals:
            out.append(cls(proposal_id=proposal))
        return out


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

    __table_args__ = (
        # UniqueConstraint('epic_id', 'campaign_id'),
    )

    def __init__(self, **kwargs):
        logger.debug('kwargs: %s', kwargs)
        super(EPIC, self).__init__(**kwargs)

    def __repr__(self):
        return '<EPIC: {}>'.format(self.epic_id)

    def simbad_query(self, radius=5.):
        return Simbad(self).query(radius=radius)

    @classmethod
    def create(cls, epics, campaign, proposal_map):
        out = []
        for epic in epics:
            proposal_ids = epic['investigation_ids'].split('|')
            proposals = [proposal_map[i] for i in proposal_ids]

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

    def __repr__(self):
        return '<Campaign: {}>'.format(self.id)


def create_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def create_session():
    return Session()
