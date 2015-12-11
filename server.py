import hmac
import datetime
import json
import logging
import tornado.web
import tornado.httpserver
from enum import Enum

from db import session
from db import ClientInfo, ClientUpdateHistory

logger = logging.getLogger('__main__')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', HomeHandle),
            (r'/api/v1/clients/*', ClientHandler),
        ]
        settings = dict(
            debug=True,
        )
        super(Application, self).__init__(handlers, settings)
        
        self.db_session = session


class BaseHander(tornado.web.RequestHandler):
    pass


class HomeHandle(BaseHander):
    def get(self):
        self.write('200 OK')


class ClientStatus(Enum):
    offline = 0
    online = 1


class ClientType(Enum):
    scanner = 1
    proxy = 2
    
    
class ClientHandler(BaseHander):
    HMAC_KEY = 'Identity'
    
    def get(self):
        session = self.application.db_session
        response = []
        for client in session.query(ClientInfo).all():
            client_info = {
                'identity': client.identity,
                'name': client.name,
                'type': client.type,
                'ip_addr': client.ip_addr,
                'mac_addr': client.mac_addr,
                'status': client.status,
                'update_time': str(client.update_time),
            }
            response.append(client_info)
        self.write(json.dumps(response))

    def post(self):
        body = self.request.body
        if body == None or body == '':
            response = { 'error': 'Request data error'}
            self.set_status(400)
            self.write(json.dumps(response))
            return
        try:
            body_dict = json.loads(body)
            name = body_dict['name']
            client_type = body_dict['type']
            mac_addr = body_dict['mac_addr']
        except Exception, e:
            logger.warn(e)
            response = { 'error': 'Request data error' }
            self.set_status(400)
            self.write(json.dumps(response))
            return
        
        session = self.application.db_session
        identity = hmac.new(self.HMAC_KEY, name+str(client_type)+mac_addr).hexdigest()
        client = session.query(ClientInfo).filter_by(identity=identity).first()
        if client != None:
            response = { 'result': 'client has existed'}
            self.write(json.dumps(response))
            return
        
        now = datetime.datetime.now()
        client = ClientInfo(identity=identity,
                                        name=name, 
                                        type=client_type,
                                        ip_addr=self.request.remote_ip,
                                        mac_addr=mac_addr,
                                        status=ClientStatus.online,
                                        update_time=now)
        client.client_update_history = [ ClientUpdateHistory(ip_addr=self.request.remote_ip, update_time=now) ] 
        session.add(client)
        session.commit()
        response = { 'result': 'create client successfully' }
        self.write(json.dumps(response))
        return
    
    def put(self):
        body = self.request.body
        if body == None or body == '':
            response = { 'error': 'Request data error'}
            self.set_status(400)
            self.write(json.dumps(response))
        try:
            body_dict = json.loads(body)
            identity = body_dict['identity']
        except Exception, e:
            logger.warn(e)
            response = { 'error': 'Request data error' }
            self.set_status(400)
            self.write(json.dumps(response))
            return

        session = self.application.db_session
        client = session.query(ClientInfo).filter_by(identity=identity).first()
        if client == None:
            response = { 'error': 'client does not exit' }
            self.set_status(400)
            self.write(json.dumps(response))
            return
        
        now = datetime.datetime.now()
        update_info = ClientUpdateHistory(ip_addr=self.request.remote_ip, update_time=now)
        client.client_update_history.append(update_info)
        session.commit()
        response = { 'result': 'update scuccessfully' }
        self.write(json.dumps(response))
        return


def main():
    SERVER_PORT = 9003
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(SERVER_PORT)
    logger.debug('Listening %d' % SERVER_PORT)
    tornado.ioloop.IOLoop.current().start()
    
if __name__ == '__main__':
    logging.basicConfig(level=True, format='%(asctime)s - [%(module)s:%(filename)s:%(lineno)d] - %(message)s')
    main()