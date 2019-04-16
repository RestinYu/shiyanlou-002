#-*- coding:utf-8 -*-
from http.server import BaseHTTPRequestHandler,HTTPServer
import sys,os
import subprocess

#def run_cgi(self,full_path):
#    data= subprocess.check_output(["python3",full_path],shell=False)

class ServerException(Exception):
    '''fuwuqineibucuowu'''
    pass

#class RequestHandler(BaseHTTPRequestHandler):
#    '''chuliqingqiubingfanhuiyemian'''

class case_no_file(object):
    '''gailujinbucunzai'''

    def test(self,handler):
        return not os.path.exists(handler.full_path)

    def act(self,handler):
        raise ServerException("'{0}' not found".format(handler.path))

class case_existing_file(object):
    '''gailujinshiwenjian'''

    def test(self,handler):
        return os.path.isfile(handler.full_path)

    def act(self,handler):
        handler.handle_file(handler.full_path)

class case_directory_index_file(object):

    def index_path(self,handler):
        return os.path.join(handler.full_path,'index.hetl')

#   panduan mubiao lujin shifou shi mulu &&muluxiashifouyou index.html
    def test(self,handler):
        return os.path.isdir(handler.full_path) and \
                os.path.isfile(self.index_path(handler))

#   xiangying  index.html  de neirong
    def act(self,handler):
        handler.handle_file(self.index_path(handler))


class case_always_fail(object):
    '''suoyouqingkuangdoubufuheshidemorenchulilei'''

    def test(self,handler):
        return True

    def act(self,handler):
        raise ServerException("Unknown object '{0}'".format(handler.path))


    # yemianmokuai
    #Page = '''\
    #    <html>
    #    <body>
    #    <p>Hello,web!</p>
    #    </body>
    #    </html>
    #'''

    #Page = '''\
    #<html>
    #<body>
    #<table>
    #<tr>  <td>Header</td>         <td>Value</td>          </tr>
    #<tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
    #<tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
    #<tr>  <td>Client port</td>    <td>{client_port}</td> </tr>
    #<tr>  <td>Command</td>        <td>{command}</td>      </tr>
    #<tr>  <td>Path</td>           <td>{path}</td>         </tr>
    #</table>
    #</body>
    #</html>'''

class case_cgi_file(object):
    '''jiaobenwenjianchuli'''

    def test(self,handler):
        return os.path.isfile(handler.full_path) and \
                handler.full_path.endswith('.py')

    def act(self,handler):
        ##yunxingjiaobenwenjian
        handler.run_cgi(handler.full_path)




class RequestHandler(BaseHTTPRequestHandler):

    #suoyoukenengdeqingkuang
    Cases = [case_no_file(),
            case_cgi_file(),
            case_existing_file(),
            case_directory_index_file(),
            case_always_fail()]


    #cuowu yemian moban
    Error_Page = """\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
        """
    def run_cgi(self,full_path):
        data= subprocess.check_output(["python3",full_path],shell=False)
        self.send_content(data)

    def do_GET(self):
        try:

            #wenjianwanzhenglujin
            self.full_path = os.getcwd() + self.path

            #bianlisuoyoukenneg de qingkuang
            for case in self.Cases:
                #ruguomanzu kenneg de qingkuang
                if case.test(self):
                #diaoyong xianying de act hanshu
                    case.act(self)
                    break

        #chuliyichang
        except Exception as msg:
            self.handle_error(msg)

    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content.encode('utf-8'),404)

   #def do_GET(self):
   #      Page = self.create_Page()
   #      self.send_content(Page)

    #def do_GET(self):
    #    try:

            # wenjianwanzhenglujin
    #        full_path = os.getcwd() + self.path

            # ruguogailujinbucunzai...
    #        if not os.path.exists(full_path):                                               #paochuyichang:wenjianweizhaodao
    #           raise ServerException("'{0}' not found".format(self.path))

            # ruguogailujinshiyigewenjian
    #       elif os.path.isfile(full_path):
                #diaoyong handler_file chuligaiwenjian
    #            self.handle_file(full_path)

            # ruguogailujinbushiyigewenjian
    #        else:
                #paochuyichang:gailujinweibuzhimingduixiang
    #            raise ServerException("Unknown object '{0}'".format(self.path))
        #chuliyichang
    #    except Exception as msg:
    #        self.handle_error(msg)

    #fasong shuju dao kefudan
    def send_content(self,content, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def handle_file(self, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            self.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(self.path, msg)
            self.handle_error(msg)

    #def create_Page(self):
    #    values = {
    #        'date_time'   : self.date_time_string(),
    #        'client_host' : self.client_address[0],
    #        'client_port' : self.client_address[1],
    #        'command'     : self.command,
    #        'path'        : self.path                                                    }
    #    Page = self.Page.format(**values)
    #    return Page

    #def do_GET(self):
    #    self.send_response(200)
    #    self.send_header("Content-Type","text/html")
    #    self.send_header("Content-Length",str(len(self.Page)))
    #    self.end_headers()
    #    self.wfile.write(self.Page.encode('utf-8'))

if __name__ == '__main__':
    serverAddress = ('',8080)
    server = HTTPServer(serverAddress,RequestHandler)
    server.serve_forever()
