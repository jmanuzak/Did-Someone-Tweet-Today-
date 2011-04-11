import os
from time import gmtime, strptime
import twython.core as twython
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


class MainPage(webapp.RequestHandler):
    
    def isToday(self, timestamp):
        date_struct = strptime(timestamp, '%a %b %d %H:%M:%S +0000 %Y');
        current_time = gmtime();
        
        if date_struct[0] == current_time[0]:
            if date_struct[1] == current_time[1]:
                if date_struct[2] == current_time[2]:
                    return True;
                else:
                    if date_struct[2] == current_time[2] -1 and (date_struct[3] - current_time[3]) < 24 :
                        return True;
                    else:
                        return False;                
            else:
                return False;        
        else:
            return False;
        
    
    def getUpdateText(self):
        try:
            twitter = twython.setup();
            user_timeline = twitter.getUserTimeline(screen_name="conanobrien");
            date = user_timeline[0]['created_at'];
                        
            if self.isToday(timestamp=date):
                url_linktext = 'Yes';
            else:
                url_linktext = 'No';
        except:
            url_linktext = 'I have no idea';
        finally:
            return url_linktext
    
    def get(self):
        
        url = 'http://twitter.com/conanobrien';
        
        template_values = {
            'url': url,
            'url_linktext': self.getUpdateText(),
            }
        path = os.path.join(os.path.dirname(__file__), 'conan.html')
        self.response.out.write(template.render(path, template_values))
        
application = webapp.WSGIApplication([('/', MainPage)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
