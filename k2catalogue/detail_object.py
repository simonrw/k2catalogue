import webbrowser


class DetailObject(object):

    def __init__(self, epic_object):
        self.epic_object = epic_object

    @property
    def url(self):
        return 'http://deneb.astro.warwick.ac.uk/phrlbj/k2varcat/objects/1.html'

    @property
    def epicid(self):
        return self.epic_object.epicid

    def open(self):
        webbrowser.open(self.url)
