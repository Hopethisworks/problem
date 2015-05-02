import cgi 
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def learning_key(links):
    """Constructs a Datastore key for a learning entity.

    We use links as the key.
    """
    return ndb.Key('Learning', links)

class Link(ndb.Model):
    """A main model for representing an individual link entry."""
    name = ndb.StructuredProperty(indexed=False)
    url = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        links = self.request.get('learning',
                                          links)
        links_query = links.query(
            ancestor=learning_key(links)).order(Link.date)
        links = links_query.fetch(10)

        template_values = {
            'name': name,
            'url': url,
            'url_linktext': url_linktext,
        }
       
        template = JINJA_ENVIRONMENT.get_template('learning file4.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
], debug=True)