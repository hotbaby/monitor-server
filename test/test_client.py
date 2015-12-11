import random
import json
import requests
import logging

logger = logging.getLogger('__main__')

class TestClientHandler(object):    
    url = 'http://localhost:9003/api/v1/clients/'

    def _generate_mac(self):
        mac = ''
        for i in range(6):
            if i == 5:
                mac = mac + str(random.randrange(10, 99, 2))
            else:
                mac = mac + str(random.randrange(10, 99, 2)) + ':'
        return mac
    
    def test_get(self):
        r = requests.get(url=self.url+self.identity)
        logger.info(r.content)
    
    def test_post(self):
        request_body = {
            'name': 'ngbit-office',
            'type': 1,
            'mac_addr': self._generate_mac(),
        }
        r = requests.post(url=self.url, data=json.dumps(request_body))
        logger.info(r.content)
        response_body_dict = json.loads(r.content)
        self.identity = response_body_dict['identity']
        logger.debug(self.identity)
    
    def test_put(self):
        r = requests.put(url=self.url+self.identity, )
        logger.info(r.content)
        

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_client = TestClientHandler()
    test_client.test_post()
    test_client.test_put()
    test_client.test_get()
