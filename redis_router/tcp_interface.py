import logging
import sys
import os


try:
    from gevent.server import StreamServer
except ImportError:
    raise Exception('gevent library is not installed.')

from router import Router


class RouterServer(object):

    CONFIG_FILE = '/etc/redis_router/servers.config'

    def __init__(self, host, port):
        self.server = StreamServer((host, port), self.main)
        self.init_router()

    def main(self, socket, address):
        logging.debug('New connection from %s:%s' % address)
        fileobj = socket.makefile()
        while True:
            client_call = fileobj.readline().replace("\n", "")

            if not client_call:
                logging.debug("client disconnected")
                break

            if client_call.strip() == '\quit':
                logging.debug("client quit")
                sys.exit(0)
            elif len(client_call) > 2:
                splitted_query = client_call.strip().split(" ")
                method, args = splitted_query[0], splitted_query[1:]

                response = getattr(self.r, method)(*args)
                fileobj.write(response)

            fileobj.flush()

    def init_router(self):
        if not os.path.exists(self.CONFIG_FILE):
            raise IOError('config file could not found. {0}'.format(self.CONFIG_FILE))

        self.r = Router(self.CONFIG_FILE)
        return self.r

    def run(self):
        self.server.serve_forever()


