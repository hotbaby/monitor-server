import logging
import json
import gevent
import requests
import netifaces

logger = logging.getLogger('__main__')


def register_client_timer(timeout=300):
    url = 'http://ngbit.info:9003/api/v1/clients/'
    mac_addr = netifaces.ifaddresses('eth0')[netifaces.AF_LINK][0]['addr'] #BUG if the eth0 interface is not exist.
    identity = ''
    def register():                
        logger.debug('Register')
        request = {
            'name': 'ngbit-office',
            'type': 1,
            'mac_addr': mac_addr,
        }
        response = requests.post(url=url, data=json.dumps(request))
        logger.info(response.content)
        body_dict = json.loads(response.content)
        global identity
        identity = body_dict['identity']
        logger.debug(identity)
        
    def update():
        logger.debug('Update')
        global identity
        assert(identity != '')
        put_url = url + identity
        response = requests.put(url=put_url)
        logger.info(response.content)
    
    register()
    while True:
        update()
        gevent.sleep(timeout)
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    gevent.spawn(register_client_timer).join()
