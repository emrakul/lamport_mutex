def parse(filename):
	pids = []
	ports = []
	with open(filename, 'r') as file:
		for line in file:
			pid, port = line.split()
			pids.append(pid)
			ports.append(port)
	return pids, ports

