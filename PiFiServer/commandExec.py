import subprocess

def commandExec(command):
    try:
        out = subprocess.check_output(command, shell=True)
        return out.decode()
    except:
        return "error"
