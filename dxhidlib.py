import socket

# Split command because of 41 character length limit


def chunk_string(command, length):
	return (command[0 + i:length + i] for i in range(0, len(command), length))


def print_error(msg):
	print("\033[1m\033[31m[-]\033[0m {0}".format(msg))


def print_status(msg):
	print("\033[1m\033[34m[*]\033[0m {0}".format(msg))


def print_good(msg):
	print("\033[1m\033[32m[+]\033[0m {0}".format(msg))


def print_warn(msg):
	print("\033[1m\033[33m[!]\033[0m {0}".format(msg))

# Send commands to VertX controller
def send_command(ip, command, payload):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.settimeout(5)

	if ip == '255.255.255.255':
		s.bind(('', 0))
		s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	if payload:
		payload_buffer = "{0}{1}".format(command, payload)
	else:
		payload_buffer = command

	try:
		s.sendto(payload_buffer, (ip, 4070))
		response = s.recvfrom(1024)
		s.close()
	except socket.timeout:
		payload_response = None
	else:
		if payload and response[0].split(';')[0] == 'ack':
			payload_response = True
		elif response[0].split(';')[0] == 'discover':
			payload_response = False
		else:
			payload_response = response

	s.close()
	return payload_response


def fingerprint(ip, action):
	data = send_command(ip, 'discover;013;', None)
	if data:
		response_data = data[0].split(';')
		name = response_data[3]
		model = response_data[6]
		version = response_data[7]
		date = response_data[8]
		internal_ip = response_data[4]
		external_ip = data[1][0]
		mac = response_data[2]

		if action == 'fingerprint':
			print_good("VertX Controller Information")
			print("RAW: {0}".format(data))
			print("Name: {0}".format(name))
			print("Model: {0}".format(model))
			print("Version: {0} - ({1})".format(version, date))
			print("Internal IP Address: {0}".format(internal_ip))
			print("External IP Address: {0}".format(external_ip))
			print("MAC Address: {0}".format(mac))

		return external_ip, mac, model

	else:
		if action == 'fingerprint':
			print_warn('VertX controller did not responded to the discovery request')
		elif action == 'discover':
			return False
