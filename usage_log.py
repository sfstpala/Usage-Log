
import json
import time
import random
import subprocess

def log(filename):
    with open(filename, "a") as f:
        _, ps = subprocess.getstatusoutput("ps aux")
        x = [i.split() for i in ps.split("\n")[1:]]
        x = [i[:4] for i in x]
        result = {}
        t_cpu, t_mem = 0, 0
        for user, pid, cpu, mem  in x:
            t_cpu += float(cpu)
            t_mem += float(mem)
            if user in result:
                result[user]["cpu"] += float(cpu)
                result[user]["mem"] += float(mem)
            else:
                result[user] = {"cpu": float(cpu), "mem": float(mem)}
        t = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())
        f.write(json.dumps({t: result}) + "\n")
        return t_cpu, t_mem

if __name__ == '__main__':
    log_n_times_per_day = 1000
    interval = (24 * 60 * 60) / log_n_times_per_day 
    d = time.strftime("%Y-%m-%dZ", time.gmtime())
    t = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())
    while True:       
        t_cpu, t_mem = log("usage-%s.log" % d)
        try:
            print(t, "    cpu: %6.2f" % t_cpu, "    mem: %6.2f" % t_mem)
        except IOError:
            pass
        time.sleep(interval * (random.random() * 2))
