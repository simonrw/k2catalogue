import webbrowser


class DetailObject(object):

    def __init__(self, epic_object):
        self.epic_object = epic_object
        self.root_url = ('http://deneb.astro.warwick.ac.uk/phrlbj/k2varcat/'
                         'objects/{epic_id}.html')

    @property
    def url(self):
        return self.root_url.format(epic_id=self.epic_id)

    @property
    def epic_id(self):
        return self.epic_object.epic_id

    def open(self):
        webbrowser.open(self.url)
