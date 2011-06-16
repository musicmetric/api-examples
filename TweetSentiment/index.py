import os
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class BaseHandler(tornado.web.RequestHandler):
	pass
	

class IndexHandler(BaseHandler):    
    def get(self):
        self.title = "Tracking tweet sentiment"
        self.render(
            "home.html", 
            title=self.title 
        )


class TrackHandler(BaseHandler):
	def get(self):
		q = self.get_argument("q", None)
		self.render("track.html", title="Tracking sentiment for %s" % q, q=q)
	

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/track/?", TrackHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            static_path=os.path.join(os.path.dirname(__file__), "static")
        )
        
        tornado.web.Application.__init__(self, handlers, **settings)        

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()        
