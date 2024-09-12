#!/usr/bin/python3

# ~ function for new users added
def newusers(data):
	for line in data:
		if 'new user' in line:
			# ~ breaks the line into separate items in a list
			parts = line.split()
			# ~ indicates the index of timestamp
			timestamp = parts[0]
			# ~ searches for 'new' in items in the list(parts)
			if 'new' in parts:
			# ~ stores the index of [3] where 'new' is
				user_index = parts.index('new')
				# ~ locates user which is 2 index after 'new', removes ',' and 'name='
				userlesscomma = parts[user_index + 2].strip(',')
				user=userlesscomma.strip('name=')

				# ~ Check for 'UID'
				for item in parts:
					# ~ Find the item that starts with 'UID='
					if item.startswith('UID='):
						UID = item.split('=')[1].strip(',')
						# ~ Exit loop once 'UID' found
						break

				# ~ Check for 'GID'
				for item in parts:
					if item.startswith('GID='):
						GID = item.split('=')[1].strip(',')
						# ~ Exit loop once 'GID' found
						break

				# ~ Check for 'home'
				for item in parts:
					if item.startswith('home='):
						home_directory = item.split('=')[1].strip(',')
						# ~ Exit loop once 'home' found
						break

				# ~ Check for 'process ID'
				for item in parts:
					if item.startswith('useradd['):
						processid = item.strip(':')
				print('New user added:', user)
				print('Time:', timestamp)
				print('UID:', UID)
				print('GID:', GID)
				print('Home directory:', home_directory)
				# ~ Prints an empty line for readability
				print('Process ID:', processid)
				print('')

			else:
				print('No new user added')

# ~ function for deleted users
def delusers(data):
	for line in data:
		if 'delete user' in line:
			# ~ breaks the line into separate items in a list
			parts = line.split()
			# ~ indicates the index of timestamp
			timestamp=parts[0]
			if 'user' in parts:
				# ~ stores the index of [5] where 'user' is
				user_index = parts.index('user')
				# ~ locates user which is 1 index after 'new', removes "'"
				user = parts[user_index + 1].strip("'")
			# ~ locates the process id and removes ':'
			for item in parts:
				if item.startswith('userdel['):
					processid = item.strip(':')
			print('User deleted:', user)
			print('Time:', timestamp)
			print('Process ID:', processid)
			print('')

# ~ function for changed password
def passwdchanged(data):
	for line in data:
		if 'password changed' in line:
			# ~ breaks the line into separate items in a list
			parts = line.split()
			# ~ indicates the index of timestamp
			timestamp = parts[0]
			# ~ locates user which the last element of the list and assigns it to user
			user = parts[-1]
			# ~ locates processid and assigns it to processid with ':' removed
			processid=parts[2].strip(':')
			
			print('Password changed for:', user)
			print('Time:', timestamp)
			print('Process ID:', processid)
			print('')

# ~ function for switched users
def switchuser(data):
	for line in data:
		if 'su:session' in line:
			# ~ breaks the line into separate items in a list
			parts = line.split()
			# ~ indicates the index of timestamp
			timestamp = parts[0]
			# ~ locates users and assign them to their respective variables
			newuser = parts[-3]
			olduser = parts[-1]
			# ~ locates processid and assigns it to processid with ':' removed
			processid = parts[2].strip(':')
			print(olduser, 'switched to', newuser)
			print('Time:', timestamp)
			print('Process ID:', processid)
			print('')
			
		elif 'authentication failure' and 'su:' in line:
			# ~ breaks the line into separate items in a list
			parts = line.split()
			# ~ indicates the index of timestamp
			timestamp = parts[0]
			# ~ locates users and assign them to their respective variables
			ruser = parts[-3]
			user = parts[-1]
			print('Authentication failure occurred')
			print(ruser, 'attempted to switch to user', user)
			print('Time:', timestamp)
			print('')

# ~ function for use of sudo
def sudo(data):
	for line in data:
		if 'USER=' and 'COMMAND' in line:
			# ~ breaks the line into separate items in a list
			parts=line.split()
			# ~ indicates the index of timestamp
			timestamp = parts[0]
			# ~ locates user and stores it in variable
			user=parts[3]
			# ~ Calculate index where the command starts
			command_index = line.index('COMMAND=')+len('COMMAND=')
			# ~ Extract the command from the line
			command=line[command_index:]
			# ~ Split the command by '/'
			command_parts=command.split('/')
			# ~ Rejoin the command parts
			command='/'.join(command_parts[0:])
			print('Time:', timestamp)
			print('User:', user)
			print('Command used:', command)
			print('')
			
# ~ function for failed use of sudo
def failedsudo(data):
	for line in data:
		if 'incorrect' in line:
			# ~ breaks the line into separate items in a list
			parts=line.split()
			# ~ indicates the index of timestamp
			timestamp = parts[0]
			# ~ locates user and stores it in variable
			user=parts[3]
			# ~ Calculate index where the command starts
			command_index = line.index('COMMAND=')+len('COMMAND=')
			# ~ Extract the command from the line
			command=line[command_index:]
			# ~ Split the command by '/'
			command_parts=command.split('/')
			# ~ Rejoin the command parts
			command='/'.join(command_parts[0:])
			# ~ display the below 'ALERT!' message more prominently
			print('*' * 30)
			print('*           ALERT!             *')
			print('* FAILED SUDO ATTEMPT DETECTED *')
			print('*' * 30)
			print('Timestamp:', timestamp)
			print('User:', user)
			print('Command:', command)
			print('')

# ~ Open the auth.log file in readlines mode
with open('/var/log/auth.log', 'r') as file:
	# Read all lines from the file
	data = file.readlines()
	
# ~ Creating a new list to store the new cleaned data
cleandata=[]

print('Below are the commands used:')
print('')

# ~ Stripping the newline characters
for eachline in data:
	cleanentry = eachline.strip('\n')
	cleandata.append(cleanentry)
	
# ~ Identifying the lines with 'COMMAND' and processing them
for eachline in cleandata:
	if 'COMMAND' in eachline:
		# ~ breaks the line into separate items in a list
		parts = eachline.split()
		# ~ indicates the index of timestamp
		timestamp = parts[0]
		# ~ locates user and stores it in variable
		user=parts[3]
		# ~ Calculate index where the command starts
		command_index = eachline.index('COMMAND=')+len('COMMAND=')
		# ~ Extract the command from the line
		command=eachline[command_index:]
		# ~ Split the command by '/'
		command_parts=command.split('/')
		# ~ Rejoin the command parts
		command='/'.join(command_parts[0:])
		print('The command used is', command, 'and it was ran at ', timestamp, 'by', user)

# ~ Calling the functions
print('')
print('Newly added users:')
print('')
newusers(cleandata)

print('')
print('Deleted users:')
print('')
delusers(cleandata)

print('')
print('Passwords changed:')
print('')
passwdchanged(cleandata)

print('')
print('Switched users:')
print('')
switchuser(cleandata)

print('')
print('Sudo used:')
print('')
sudo(cleandata)

print('')
print('Failed sudo use:')
print('')
failedsudo(cleandata)
