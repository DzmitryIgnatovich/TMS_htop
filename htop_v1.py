import psutil as ps
import time
import os

OUTPUT = {"cpu":{"cpu_loading":"{:<15}{:>27}%",
                 "core_count":"{:<15}{:>20} core(s)",
                 "cores_loading":"",
                 "cpu_freq":"{:<15}{:>24} MHz"},
          "mem":{"mem_all":"{:<12}{:>10} Gb",
                 "mem_free":"{:<12}{:>10} Gb",
                 "mem_used":"{:<12}{:>10} Gb",
                 "swap_used":"{:<12}{:>10} Gb"},
          "net":{"sent_bytes":"{:<20} {:>12} bytes",
                 "recieve_bytes":"{:<20} {:>12} bytes"},
          "sensore":{"bat":"{:<20} {:>17}%"},
          "process":{"pid":"{:-<8}",
                     "name":"{:->32}",
                     "username":"{:->26}|"}}

"""
def getCPU():
    while True:
        core_count = ps.cpu_count(logical=True)
        cpu_loading = ps.cpu_percent(interval=0.9, percpu=True)
        str_cpu = '{}{:>10}%'
        
        for i in range(0,len(cpu_loading)-1):
            str_cpu = str_cpu + '{:>6}%'
        
        print(str_cpu.format(core_count, *cpu_loading), end='\r')
"""

def finish():
    flag = True
    if keyboard.is_pressed("Esc"):
        flag = False
    return flag


def getCPU():
    res = {"core_count": ps.cpu_count(logical=True),
           "cpu_loading": ps.cpu_percent(interval=0.0, percpu=False),
           "cores_loading": ps.cpu_percent(interval=0.0, percpu=True),
           "cpu_freq": ps.cpu_freq()}
    return res


def getMEM():
    sys_mem = ps.virtual_memory()
    sys_swap = ps.swap_memory()
    
    res = {"mem_all": round(sys_mem[0]//1024//1024/1024, 3),
           "mem_free": round((sys_mem[1] + sys_mem[4])//1024//1024/1024, 3),
           "mem_used": round(sys_mem[3]//1024//1024/1024, 3),
           "swap_used": round(sys_swap[0]//1024//1024/1024, 3)}
    return res


def getNET():
    net = ps.net_io_counters()

    res = {"sent_bytes": net[0],
        "recieve_bytes": net[1]}
    return res


def getSENSORE():
    bat = ps.sensors_battery()

    res = {"bat": bat[0]}
    return res


def getPROC():
    res = {p.pid: p.info for p in ps.process_iter(['name', 'username'])}
    # res=[]
    # for proc in psutil.process_iter(['pid', 'name', 'username']):
    #     res.append(proc)

    return res


def show(*args,**kwargs):
    cpu_loading = kwargs["cpu"]["cpu_loading"]
    cores_loading = kwargs["cpu"]["cores_loading"]
    core_count = kwargs["cpu"]["core_count"]
    cpu_freq = kwargs["cpu"]["cpu_freq"]

    mem_all = kwargs["mem"]["mem_all"]
    mem_free = kwargs["mem"]["mem_free"]
    mem_used = kwargs["mem"]["mem_used"]
    swap_used = kwargs["mem"]["swap_used"]

    net_sent_bytes = kwargs["net"]["sent_bytes"]
    net_recieve_bytes = kwargs["net"]["recieve_bytes"]

    bat_charge = kwargs["sensore"]["bat"]

    process = kwargs["proc"]
    

    count = str(28//core_count - 1)
    str_core = "{:<15}"

    for i in range(0, core_count):
        str_core = str_core + '{:->' + count + '}%'

    OUTPUT["cpu"]["cores_loading"] = ''
    OUTPUT["cpu"]["cores_loading"] = OUTPUT["cpu"]["cores_loading"] + str_core
    
    os.system('clear')

    print(OUTPUT["cpu"]["core_count"].format('Core count', core_count),
          OUTPUT["mem"]["mem_all"].format("All memory", mem_all),
          OUTPUT["net"]["sent_bytes"].format("Sent to network",net_sent_bytes), sep=' | ')

    print(OUTPUT["cpu"]["cpu_loading"].format('CPU loading', cpu_loading),
          OUTPUT["mem"]["mem_free"].format("Free memory", mem_free),
          OUTPUT["net"]["recieve_bytes"].format("Recieve from network", net_recieve_bytes), sep=' | ')

    print(OUTPUT["cpu"]["cores_loading"].format("Cores loadind",*cores_loading),
          OUTPUT["mem"]["mem_used"].format("Used memory", mem_used),
          '---------------------------------------', sep=' | ')

    print(OUTPUT["cpu"]["cpu_freq"].format("CPU Frequency", int(cpu_freq[0])),
          OUTPUT["mem"]["swap_used"].format("Used Swap", swap_used),
          OUTPUT["sensore"]["bat"].format("Battery charge",bat_charge), 
          sep=' | ')
    
    separator_line = ''
    for i in range(113):
        separator_line = separator_line + '-'
    print(separator_line)


    print("{:<8}{:>35}{:>29}".format("PID", "Name", "Username"))


    for el in process:
        pid = el
        name = process[el]["name"]
        username = process[el]["username"]
        print(OUTPUT["process"]["pid"].format(str(pid)+" "),
              OUTPUT["process"]["name"].format(name[:20]),
              OUTPUT["process"]["username"].format(username), sep=" | ")


def main():
    while True:
        cpu_info = getCPU()
        mem_info = getMEM()
        net_info = getNET()
        sens_info = getSENSORE()
        proc_info = getPROC()

        show(cpu=cpu_info,
             mem=mem_info,
             net=net_info,
             sensore=sens_info,
             proc=proc_info
             )
        time.sleep(3.0)


if __name__ == '__main__':
    main()

