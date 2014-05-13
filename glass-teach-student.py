# C:\Python27\python.exe glass-teach-student.py

from subprocess import Popen
import time 

def glass_teach_student():
	curr_state_map = {}
	# process that turns off the monitor
	monitor_proc = ''

	while True:
		# read shared file, structured as 'name'='value'
		# currently supported pairs: monitor={true, false}
		ipc_file = open('glass-teach-config.txt', 'r')
		# current state of this machine
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
						monitor_proc = Popen(['glass-teach.exe'])
					else:
						# turn off monitor, ie start process
						monitor_proc.terminate()
				curr_state_map[state] = value
		# TODO: check if monitor is actually off if we read the state as off, this prevents people
		# from ctrl-alt-deleting and exiting the window. This will break debug.
		time.sleep(.5)

# confirms functionality of monitor on/off
def monitorTest():
	monitor_proc = Popen(['glass-teach.exe'])
	time.sleep(1)
	monitor_proc.terminate()
		
if __name__ == '__main__':
    glass_teach_student()
	#monitorTest()
