
import time
import subprocess
import collections
import functools
import sys


class Monitor (object):

    def __init__(self, filename):
        self.filename = filename

    def procs(self):
        def ps_aux():
            return subprocess.getoutput("ps aux").strip().split("\n")[1:]
        homes = subprocess.getoutput("ls /home").split()
        for i in ps_aux():
            user, pid, *_ = i.split()
            if user in homes or user == "root":
                yield user, int(pid)

    def count(self):
        c = collections.Counter()
        for user, pid in self.procs():
            try:
                stat = open("/proc/{}/stat".format(pid)).read().strip()
            except IOError:
                continue
            stat = stat.split(")")[1].split()
            t = int(stat[11]) + int(stat[12]) + int(stat[13]) + int(stat[14])
            c[user] += t
        return c

    def observe_forever(self):
        while True:
            try:
                c = self.count()
                t = time.time()
                time.sleep(5)
                c = self.count() - c
                tx = time.time() - t
                for user in c:
                    cputime = int((c[user] / tx / 250) * 10000)
                    self.log(t, user, cputime)
            except Exception as e:
                print(repr(e))

    @functools.lru_cache(None)
    def get_user_id(self, username):
        return int(subprocess.getoutput("id -u " + username).strip())

    def log(self, t, user, cputime):
        with open(self.filename, "ab") as f:
            tod = int(time.time()).to_bytes(4, 'big')
            cpu = cputime.to_bytes(4, 'big')
            uid = self.get_user_id(user).to_bytes(4, 'big')
            f.write(tod + cpu + uid)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: {} FILENAME".format(sys.argv[0]), file=sys.stderr)
        exit(2)
    m = Monitor(sys.argv[1])
    m.observe_forever()
