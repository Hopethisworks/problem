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


MAIN_PAGE_FOOTER_TEMPLATE = """\
    <form action="/sign?%s" method="post">
      <div><textarea name="name" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Sign Guestbook"></div>
    </form>
    <hr>
    <form>Guestbook name:
      <input value="%s" name="guestbook_name">
      <input type="submit" value="switch">
    </form>
    <a href="%s">%s</a>
  </body>
</html>
"""

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


    #creating an object class, Link, to store each website link entry

class Link(ndb.Model):
    """A main model for representing an individual website link entry."""
    name = ndb.StringProperty(indexed=False)
    linkurl = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        links_query = Link.query(
            ancestor=guestbook_key(guestbook_name)).order(Link.date)
        links = links_query.fetch(10)

        # user = users.get_current_user()
        # if user:
        #     url = users.create_logout_url(self.request.uri)
        #     url_linktext = 'Logout'
        # else:
        #     url = users.create_login_url(self.request.uri)
        #     url_linktext = 'Login'

        template_values = {
            'links': links,
            'guestbook_name': urllib.quote_plus(guestbook_name),
        }
       
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

        # # Write the submission form and the footer of the page
        # sign_query_params = urllib.urlencode({'guestbook_name':
        #                                       guestbook_name})
        # self.response.write(MAIN_PAGE_FOOTER_TEMPLATE %
        #                     (sign_query_params, cgi.escape(guestbook_name),
        #                      url, url_linktext))

class Guestbook(webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        link = Link(parent=guestbook_key(guestbook_name))

        link.name = self.request.get('name')
        link.linkurl = self.request.get('linkurl')
        link.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
], debug=True)