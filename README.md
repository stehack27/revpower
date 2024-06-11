<div align="center" width="100%">
    <img src="https://i.imgur.com/Gyw1nBr.png" width="70%" align="center"/>
</div>

## Description
Revpower is a reverse shell written in Powershell, served with a python TCP and HTTP server.\
In the `server` folder, you can find anything related to python and the server, while in the `reverse_shell` one, there are some script to launch the RS.
The file `rubber_ducky.cpp` is an Arduino Script to launch your reverse shell by plugging a HID in a computer.

## Configuration
You can find some examples to use with your configuration in this repo. Be careful to obfuscate the reverse shell before running it or Windows Defender will mark it as a virus. \
Here some useful references to do so: [Obfuscation-Bible](https://github.com/t3l3machus/PowerShell-Obfuscation-Bible) \
I've wrote a startup file to launch with the rubber ducky `reverse_shell\startup.ps1`, it creates a shortcut in `shell:startup` that runs Revpower every time the user turns on the computer.\
Before running the server, please, setup your own configuration in `server\settings.py`.

## Server
In order to run:
```sh
python3 revpower.py
```

## Commands
#### Revpower
`screenshot` -> Capure a screenshot and sends it to the attacker server \
`upload file.txt` -> Upload a file to the victim machine \
`download /path/file.txt` -> Download a file from the victim machine and send it to the attacker server \

#### Server
`session` -> List opened connections \
`session <id>` -> Switch to an opened session \
`exit` -> Exit current session \
`close` -> Close current connection 
