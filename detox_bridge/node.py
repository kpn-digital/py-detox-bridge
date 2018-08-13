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
        self._error = error

    @property
    def message(self):
        return self._error.get("message")

    @property
    def stack(self):
        return self._error.get("stack")

    def __str__(self):
        lines = []
        for k, v in self._error.items():
            lines.append("{}:".format(k))
            for line in str(v).splitlines():
                lines.append("  {}".format(line))
        return "\n".join(lines)


def which():
    nvm_script = os.environ.get("NVM", "$NVM_DIR/nvm.sh")
    output_bytes = check_output(["bash", "-c", ". {} && nvm which".format(nvm_script)])
    output = output_bytes.decode("utf-8")
    return output.splitlines()[-1]


class Connection(object):
    def __init__(self, proc, default_timeout):
        self._proc = proc
        self.default_timeout = default_timeout

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self._proc.terminate()

    def send_thread(self, js):
        try:
            request = json.dumps({"eval": str(js)}) + "\n"
            logger.info("Request:{}\n".format(request))
            self._proc.stdin.write(request.encode("utf-8"))
            self._proc.stdin.flush()
            encoded_response = next(self._proc.stdout)
            logger.info("Response:{}\n".format(encoded_response))
            self._result = json.loads(encoded_response.decode("utf-8"))
            error = self._result.get("error")
            if error:
                raise NodeError(error)
            self._result = self._result.get("result", None)
        except: # NOQA:E722
            t, v, tb = sys.exc_info()
            self._result = v

    def __call__(self, js, *, timeout=None):
        if timeout is None:
            timeout = self.default_timeout

        thread = threading.Thread(target=lambda: self.send_thread(js))
        thread.daemon = True
        thread.start()
        thread.join(timeout=timeout)
        if thread.is_alive():
            raise TimeoutError()

        if isinstance(self._result, Exception):
            raise self._result
        return self._result


def start(default_timeout=1):
    executable = which()

    proc = Popen(
        [executable,
            os.path.join(os.path.dirname(__file__),
                         "bridge.js")],
        stdin=PIPE,
        stdout=PIPE)

    return Connection(proc, default_timeout)
