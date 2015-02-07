import webbrowser


class DetailObject(object):

    def __init__(self, epic_object):
        self.epic_object = epic_object
        self.root_url = ('http://deneb.astro.warwick.ac.uk/phrlbj/k2varcat/'
                         'objects/{epicid}.html')

    @property
    def url(self):
        return self.root_url.format(epicid=self.epicid)

    @property
    def epicid(self):
        return self.epic_object.epicid

    def open(self):
        webbrowser.open(self.url)
