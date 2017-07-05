import json
import logging
import os
import sys
import threading
from subprocess import PIPE, Popen, check_output

logger = logging.getLogger('detox-bridge-node')


class TimeoutError(RuntimeError):
    def __init__(self):
        super().__init__("Timeout")


class NodeError(RuntimeError):
    def __init__(self, error):
        self.__dict__.update(**error)


def which():
    nvm_script = os.environ.get("NVM", "$NVM_DIR/nvm.sh")
    output_bytes = check_output(["bash", "-c", ". {} && nvm which".format(nvm_script)])
    output = output_bytes.decode("utf-8")
    return output.splitlines()[-1]


class Connection(object):
    def __init__(self, proc):
        self._proc = proc

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self._proc.terminate()

    def send_thread(self, js):
        try:
            request = json.dumps({"eval": js}) + "\n"
            logger.info("Request:{}\n".format(request))
            self._proc.stdin.write(request.encode("utf-8"))
            self._proc.stdin.flush()
            encoded_response = next(self._proc.stdout)
            logger.info("Response:{}\n".format(encoded_response))
            self._result = json.loads(encoded_response.decode("utf-8"))
            error = self._result.get("error")
            if error:
                raise NodeError(error)
        except:
            t, v, tb = sys.exc_info()
            self._result = v

    def send(self, js, *, timeout):
        thread = threading.Thread(target=lambda: self.send_thread(js))
        thread.daemon = True
        thread.start()
        thread.join(timeout=timeout)
        if thread.is_alive():
            raise TimeoutError()

        if isinstance(self._result, Exception):
            raise self._result
        return self._result


def start():
    executable = which()

    proc = Popen(
        [executable,
            os.path.join(os.path.dirname(__file__),
                         "bridge.js")],
        stdin=PIPE,
        stdout=PIPE)

    return Connection(proc)