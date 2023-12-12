import platform, subprocess

def Subprocess_Call(command):
    subprocess.call(command)

if __name__ == '__main__':
    if platform.machine() == "aarch64":
        command = ["chmod", "+x", "aarch64"]
        Subprocess_Call(command)
        command = ["./aarch64"]
        Subprocess_Call(command)
    elif platform.machine() == "x86_64":
        command = ["chmod", "+x", "x86_64"]
        Subprocess_Call(command)
        command = ["./x86_64"]
        Subprocess_Call(command)
    else:
        print(f"Perangkat {platform.machine()} bit, tidak dapat menjalankan aarch64 atau x86_64!")
        exit()