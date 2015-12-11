import json
import requests
import logging

logger = logging.getLogger('__main__')

class TestClientHandler(object):
    
    url = 'http://localhost:9003/api/v1/clients/'
    
    def test_get(self):
        r = requests.get(url=self.url)
        logger.info(r.content)
    
    def test_post(self):
        request_body = {
            'name': 'ngbit-office',
            'type': 1,
            'mac_addr': '98:90:96:b8:5a:05',
        } 
        r = requests.post(url=self.url, data=json.dumps(request_body))
        logger.info(r.content)
    
    def test_put(self):
        request_body = { 'identity': '999498adf775ebe2d0e90dbfe68acb07', }
        r = requests.put(url=self.url, data=json.dumps(request_body))
        logger.info(r.content)
        

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_client = TestClientHandler()
    test_client.test_post()
    test_client.test_put()
    test_client.test_get()
