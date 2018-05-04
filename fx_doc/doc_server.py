from subprocess import Popen


def serve_doc(dest, port=8080):
    cmd = ['python', '-m', 'http.server', str(port)]
    ret = Popen(cmd, cwd=dest).wait()
    sys.exit(ret)
