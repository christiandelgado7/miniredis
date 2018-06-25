import argparse
import sys

import console
from api_rest import RestServer
from miniredis import *

log = logging.getLogger(__name__)


def redis_set_to_list(dic):
    return [str(x) for _, x in sorted(zip(dic.values(), dic.keys()))]


class MiniRedisServer(object):

    def __init__(self, cmd=True, rest=True, port=None):
        print 'Starting MiniRedis Server...'
        super(MiniRedisServer, self).__init__()
        self.miniredis = MiniRedis()
        self.cmd = console.Console(self.miniredis)
        self.restServer = None
        if rest:
            print 'Starting MiniRedis API REST...'
            self.restServer = RestServer(cmd=self.cmd, port=port)
        if cmd:
            if self.restServer:
                th = threading.Thread(target=self.restServer.start_server)
                th.daemon = True
                th.start()
            try:
                self.cmd.cmdloop('Starting MiniRedis Console...')
            except (SystemExit, KeyboardInterrupt):
                if self.restServer:
                    self.restServer.stop_server()
                    self.restServer.miniredis = None
                print 'MiniRedis console closed'
                sys.exc_clear()
        else:
            if self.restServer:
                self.restServer.start_server()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=int, help="port for the REST API", default=8080)
    admin_arg = parser.add_mutually_exclusive_group(required=False)
    admin_arg.add_argument('--no-cmd', dest='cmd', action='store_false', help="don't open shell console")
    admin_arg.add_argument('--no-rest', dest='rest', action='store_false', help="don't start HTTP Server for REST API")
    parser.set_defaults(cmd=True, rest=True)
    args = parser.parse_args()
    server = MiniRedisServer(cmd=args.cmd, rest=args.rest, port=args.p)
