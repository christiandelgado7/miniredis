import logging
import warnings

from flask import Flask, request

log = logging.getLogger(__name__)
warnings.filterwarnings("ignore")
logging.getLogger('werkzeug').setLevel(logging.ERROR)


class RestServer(object):
    def __init__(self, cmd, host='0.0.0.0', port=8080):
        self.cmd = cmd
        self.host = host
        self.port = port
        self.app = None

    def route(self):
        self.app.add_url_rule('/', methods=["GET"], view_func=self.exe_cmd)

    def start_server(self):
        log.info('Starting Rest Server.')
        self.app = Flask(__name__)
        self.route()
        self.app.run(host=self.host, port=self.port, debug=False)

    def stop_server(self):
        try:
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()
        except:
            return
        finally:
            print('Stopping MiniRedis API REST....')

    def exe_cmd(self):
        try:
            cmd = request.args.get('cmd')
            if cmd is not None and cmd != 'exit':
                return str(self.cmd.exec_cmd(cmd))
            else:
                request.status = 400
                return "invalid 'cmd' param"
        except (KeyboardInterrupt, SystemExit, MemoryError):
            raise
        except Exception as e:
            log.error(e)
            request.status = 500
            return 'Error: {}'.format(e)
