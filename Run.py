import platform, subprocess

def Subprocess_Call(command):
    subprocess.call(command)

if __name__ == '__main__':
    try:
        if platform.machine() == "aarch64":
            command = ["chmod", "+x", "aarch64"]
            Subprocess_Call(command)
            command = ["./aarch64"]
            Subprocess_Call(command)
        else:
            print(f"Perangkat {platform.machine()} bit, tidak dapat menjalankan aarch64!")
            exit()
    except (KeyboardInterrupt):
        if platform.machine() == "aarch64":
            command = ["./aarch64"]
            Subprocess_Call(command)
        else:
            print(f"Perangkat {platform.machine()} bit, tidak dapat menjalankan aarch64!")
            exit()
    except (Exception) as e:
        print(f"[Error] {str(e).capitalize()}!")
        exit()
