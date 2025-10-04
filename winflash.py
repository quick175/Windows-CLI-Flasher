from tkinter import filedialog
import tkinter
import subprocess   
import time
import shutil
import webbrowser
import platform
#installer===>


def open_winget_page():
    url = "https://aka.ms/getwinget"
    webbrowser.open(url)
    print(f"Opened browser to {url}")

def open_terminal_instructions():
    system = platform.system()

    instructions = (
        "Winget is missing.\n"
        "To install winget, please visit the opened browser page.\n"
        "Alternatively, you can install Chocolatey:\n\n"
        "1) Open PowerShell as Administrator.\n"
        "2) Run:\n"
        '   Set-ExecutionPolicy Bypass -Scope Process -Force\n'
        '   iex ((New-Object System.Net.WebClient).DownloadString("https://community.chocolatey.org/install.ps1"))\n'
        "3) Then run this script again."
    )

    if system == "Windows":
        try:
            subprocess.Popen([
                "wt", "powershell", "-NoExit", "-Command", f'Write-Host "{instructions}"'
            ])
        except FileNotFoundError:
            subprocess.Popen([
                "cmd", "/k", f'echo {instructions}'
            ])
    else:
        print("Manual instructions:")
        print(instructions)

def qemu_ins():
    winget_exists = shutil.which("winget") is not None
    choco_exists = shutil.which("choco") is not None

    if winget_exists:
        print("Installing QEMU and USBImager via winget...")
        subprocess.run([
            "winget", "install", "--id=QEMU.QEMU", "-e"
        ], check=True)
        subprocess.run([
            "winget", "install", "--id=bztsrc.usbimager", "-e"
        ], check=True)

    elif choco_exists:
        print("Installing QEMU via Chocolatey and USBImager via winget...")
        subprocess.run([
            "choco", "install", "qemu", "-y"
        ], check=True)
        # USBImager via winget since choco package unknown or missing
        subprocess.run([
            "winget", "install", "--id=bztsrc.usbimager", "-e"
        ], check=True)

    else:
        print("Neither winget nor Chocolatey found. Opening browser and instructions...")
        open_winget_page()
        time.sleep(2)
        open_terminal_instructions()

qemu_ins()
print("Supported file formats- .iso,.bin,.img,.bin,.dmg")
img_path=None
def converter():
    subprocess.run(f'qemu-img convert -o raw {img_path} {img_path}.img')    


def flash_W():
    subprocess.run("Get-Disk")
    time.sleep(2)
    drive=input("Insert your Drive Name  (Probably Starts with E: or F:)---> ")
    print("Flashing an image into a drive wipes all data on a disk.")
    print("Please Double Check Disk Name before proceeding")
    k=input("Proceed [Y/N] ===> ")
    if k == "Y":
        subprocess.run(f"usbimager {img_path} {drive}")
    else:
        exit()


def filetype(filepath):
    filename = filepath.replace('\\', '/').split('/')[-1]
    parts = filename.split('.')
    if '.' not in filename:
        return None    
    if len(parts) > 1:
        return parts[-1].lower()
    return ''
    if ext in ('iso','bin', 'raw','img'):
         flash_W() 
    
    if ext in ('dmg'):
         converter()
         flash_W
    
img_path=tkinter.filedialog.askopenfilename()
ext=filetype(img_path)