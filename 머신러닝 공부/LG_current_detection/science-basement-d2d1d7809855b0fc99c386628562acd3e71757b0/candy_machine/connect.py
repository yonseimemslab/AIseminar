import paramiko
server = "192.168.2.3"
username = "robot"
password = "maker"
ssh = paramiko.SSHClient()
cmd_to_execute = "python3 /home/robot/motor_movement/angle_example.py"
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(server, username=username, password=password)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)

