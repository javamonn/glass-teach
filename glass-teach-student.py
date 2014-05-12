from subprocess import Popen

def glass_teach_student():
    # read shared file, structured as 'name'='value'
    # currently supported pairs: monitor={true, false}
    ipc_file = open('glass_teach.txt', r)
    # current state of this machine
    curr_state_map = {}
    # process that turns off the monitor
    monitor_proc = ''
    for line in ipc_file:
        name, value = line.split('=')
        # assume the first time we read the file it'll be in a starting config
        if name not in curr_state_map:
            curr_state_map[name] = value
        # whether we need to change the current state of this machine
        if curr_state_map[name] != value:
            # monitor on/off
            if name == 'monitor':
                if value:
                    # turn on monitor, ie end process
                    monitor_proc = Popen(['monitorOff.exe'])
                else:
                    # turn off monitor, ie start process
                    monitor_proc.terminate()

if __name__ == '__main__':
    glass_teach_student()
