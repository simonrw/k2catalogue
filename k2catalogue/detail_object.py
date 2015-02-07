class DetailObject(object):

    def __init__(self, epicid):
        self.epicid = epicid

    @property
    def url(self):
        return 'http://deneb.astro.warwick.ac.uk/phrlbj/k2varcat/objects/1.html'
