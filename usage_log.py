
import json
import time
import random
import subprocess
import configparser
import os.path


def usagelog_config():
    config = configparser.ConfigParser()
    config.read('usagelog.cfg')
    return config


def log(filename):
    c = usagelog_config()
    _, ps = subprocess.getstatusoutput("ps aux")
    x = [i.split() for i in ps.split("\n")[1:]]
    x = [i[:4] + [i[9]] + [' '.join(i[10:])] for i in x]
    result = {}
    t_cpu, t_mem = 0, 0
    for user, pid, cpu, mem, duration, cmd  in x:
        t_cpu += float(cpu)
        t_mem += float(mem)
        if user in result:
            result[user]["cpu"] += float(cpu)
            result[user]["mem"] += float(mem)
            result[user]["exec"].append({"duration": duration, "command": cmd})
        else:
            result[user] = {"cpu": float(cpu), "mem": float(mem)}
            result[user]["exec"] = [{"duration": duration, "command": cmd}]
    t = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())
    with open(filename, "a") as f:
        f.write(json.dumps({t: result}) + "\n")
    return t_cpu, t_mem


if __name__ == '__main__':
    log_n_times_per_day = 1000
    interval = (24 * 60 * 60) / log_n_times_per_day
    d = time.strftime("%Y-%m-%dZ", time.gmtime())
    t = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())
    c = usagelog_config()
    while True:
        t_cpu, t_mem = log(os.path.join(c.get('general', 'log_dir'),
            "usage-%s.log" % d))
        try:
            print(t, "    cpu: %6.2f" % t_cpu, "    mem: %6.2f" % t_mem)
        except IOError:
            pass
        time.sleep(interval * (random.random() * 2))
