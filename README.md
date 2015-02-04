# k2catalogue
[![Build Status](https://travis-ci.org/mindriot101/k2catalogue.svg)](https://travis-ci.org/mindriot101/k2catalogue)[![Code Health](https://landscape.io/github/mindriot101/k2catalogue/master/landscape.svg)](https://landscape.io/github/mindriot101/k2catalogue/master)[![Documentation Status](https://readthedocs.org/projects/k2catalogue/badge/?version=latest)](https://readthedocs.org/projects/k2catalogue/?badge=latest)[![Latest Version](https://pypip.in/version/k2catalogue/badge.svg)](https://pypi.python.org/pypi/k2catalogue/)

Simple interactive query api for the K2 proposals list, based on the IPython console.

## Features

* Open a simbad search around the EPIC object
* Get the proposals for an EPIC object
* Get the objects contained in a single proposal
* Get the objects observed during a campaign
* Visit the proposals page for a campaign
* View the proposal title and PI
* View the proposal pdf for a proposal
* Get the EPIC object magnitude, ra and dec if available

## Installation

`pip install git+https://github.com/mindriot101/k2catalogue`

### Requirements:

*all from pip*

* requests
* sqlalchemy
* ipython
* vcrpy
* beautifulsoup4

The first run may fail with "table missing" type errors. In this case the initial database must be created, with the `-s` flag: `k2cat-search -s`. This will create `database.sqlite` in the current directory. Subsequent runs do not need the `-s` flag unless you want to rebuild the database.

## Examples

Fire up the interpreter with `k2cat-search` and try these:

```python
# Get an object by epic id (using WASP-85 b as an example)
e = get_by_epicid(201862715)
print(e) # => <EPIC: 201862715>

# Open the simbad page for a radius of 5 arcmin around the target
e.simbad_query(radius=5.0)
# ... default browser opens, showing the SIMBAD details

# Show the proposals containing that object
print(e.proposals)
# => [<Proposal GO1041_SC: Hellier - "Kepler K2 observatio...">, <Proposal GO1032_SC: Van Grootel - "K2 Observations of S...">, <Proposal GO1054_LC: Sanchis-Ojeda - "Using K2 to understa...">, <Proposal GO1059_LC: Stello - "Galactic Archaeology...">, <Proposal GO1005_LC: Wang - "Searching For Hot Ju...">]

# Let's look at proposal GO1041_SC
p = e.proposals[0] # This may have a different index for you
print(p) # => <Proposal GO1041_SC: Hellier - "Kepler K2 observatio...">

# Where is the proposal pdf?
print(p.pdf_url) # => http://keplerscience.arc.nasa.gov/K2/docs/Campaigns/C1/GO1041_Hellier.pdf

# Let's open that pdf in a web browser
p.open_proposal()
# ... default browser opens, showing the proposal pdf

# Where are the proposal pdfs kept?
p.open_proposals_page()
# ... default browser opens, showing the list of proposals

# Let's look at the proposal details
print('Proposal PI: {pi} and title: {title}'.format(
      pi=p.pi, title=p.title))
# => Proposal PI: Hellier and title: Kepler K2 observations of the hot Jupiter WASP-85b

# What other objects are in the same proposal?
print(p.objects)
# => [<EPIC: 201862715>] Ah just the one then.

# Which campaign is the proposal (or object) in?
print('Object campaign: {}, proposal campaign: {}'.format(e.campaign, p.campaign))
# => Object campaign: <Campaign: 1>, proposal campaign: <Campaign: 1>

# What about the object magnitude and coordinates?
print('WASP-85 b is located here: {ra} {dec} and is magnitude {mag}'.format(
      ra=e.ra, dec=e.dec, mag=e.mag))
# => WASP-85 b is located here: 175.90838 6.563726 and is magnitude 10.247
```

## Advanced usage

The package uses SQLAlchemy for all of the database interactions, and the `session` object along with the database models `Campaign`, `EPIC` and `Proposal` are available to the user for more advanced queries.
For example the first example above (`get_by_epicid`) can be performed with the SQLAlchemy api:

```python
epicid = 201862715
e = session.query(EPIC).filter(EPIC.epic_id == epicid).first()
```
