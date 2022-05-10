#!/bin/bash

# https://github.com/json1c
# Copyright (C) 2021  json1c

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.
set -e


if  cat /etc/*release | grep ^NAME | grep CentOS || cat /etc/*release | grep ^NAME | grep Red || cat /etc/*release | grep ^NAME | grep Fedora; then 
    if [[ $(whoami) = 'root' ]]; then
        clear
        echo "Detected OS : $(cat /etc/*release | grep ^NAME)"
        echo "Packet Manager : Yum"
        echo "Installings packages for your system..."
        sleep 5
        yum install -y ffmpeg youtube-dl nodejs  git python python-pip python3-pip && pip3 install -r requirements.txt && pip3 install git+https://github.com/pytgcalls/pytgcalls -U
        clear
        echo "All packages installed!"
        sleep 2
        clear
        echo "Starting installing botnet..."
        sleep 2
        cd ~ && git clone https://github.com/json1c/telegram-raid-botnet.git && cd telegram-raid-botnet && python main.py
        else
            clear
            echo "Please launch autoinstall with root"
            exit 1;
    fi
elif [[ "$OSTYPE" =~ ^WSL2 ]]; then
    if [[ $(whoami) = 'root' ]]; then
        clear
        echo "Detected OS : $(cat /etc/*release | grep ^NAME)"
        echo "Packet Manager : Apt"
        echo "Installings packages for your system..."
        sleep 5
        apt install -y ffmpeg youtube-dl git python python-pip nodejs python3-pip && pip3 install -r requirements.txt && pip3 install git+https://github.com/pytgcalls/pytgcalls -U
        clear
        echo "All packages installed!"
        sleep 2
        clear
        echo "Starting installing botnet..."
        sleep 2
        cd ~ && git clone https://github.com/json1c/telegram-raid-botnet.git ~/telegram-raid-botnet && cd telegram-raid-botnet && python main.py
        else
            clear
            echo "Please launch autoinstall with root"
            exit 1;
fi
elif cat /etc/*release | grep ^NAME | grep -r Arch || cat /etc/*release | grep ^NAME | grep Artix || cat /etc/*release | grep ^NAME | grep Antix || cat /etc/*release | grep ^NAME | grep Manjaro || cat /etc/*release | grep ^NAME | grep Parabola; then
    if [[ $(whoami) = 'root' ]]; then
        clear
        echo "Detected OS : $(cat /etc/*release | grep ^NAME)"
        echo "Packet Manager : Pacman"
        echo "Installings packages for your system..."
        sleep 5
        yum install -y ffmpeg youtube-dl nodejs git python python-pip python3-pip && pip3 install -r requirements.txt && pip3 install git+https://github.com/pytgcalls/pytgcalls -U
        clear
        echo "All packages installed!"
        sleep 2
        clear
        echo "Starting installing botnet..."
        sleep 2
        cd ~ && git clone https://github.com/json1c/telegram-raid-botnet.git ~/telegram-raid-botnet && cd telegram-raid-botnet && python main.py
        else
            clear
            echo "Please launch autoinstall with root"
            exit 1;
    fi
elif  cat /etc/*release | grep ^NAME | grep Ubuntu || cat /etc/*release | grep ^NAME | grep Debian || cat /etc/*release | grep ^NAME | grep Mint || cat /etc/*release | grep ^NAME | grep Mint; then
    if [[ $(whoami) = 'root' ]]; then
        clear
        echo "Detected OS : $(cat /etc/*release | grep ^NAME)"
        echo "Packet Manager : Apt"
        echo "Installings packages for your system..."
        sleep 5
        apt-get update && apt-get install -y ffmpeg youtube-dl git nodejs  python python-pip python3-pip software-properties-common && sudo add-apt-repository ppa:deadsnakes/ppa && pip3 install -r requirements.txt && pip3 install git+https://github.com/pytgcalls/pytgcalls -U
        clear
        echo "All packages installed!"
        sleep 2
        clear
        echo "Starting installing botnet..."
        sleep 2
        cd ~ && git clone https://github.com/json1c/telegram-raid-botnet.git ~/telegram-raid-botnet && cd telegram-raid-botnet && python3.10 main.py
    else
        clear
        echo "Please launch autoinstall with root"        
        exit 1;
    fi
elif  [[ $(uname -o) = 'Android' ]]; then
    if echo $PREFIX | grep -o "com.termux"; then
        clear
        echo "Detected System : Android (termux)"
        echo "Package manager : pkg"
        echo "Installings packages for your system..."
        sleep 5
        pkg update && pkg upgrade && pkg install -y ffmpeg nodejs youtube-dl git python python-pip && pip3 install -r requirements.txt 
        clear
        echo "All packages installed!"
        sleep 2 
        clear
        echo "Starting installing botnet..."
        sleep 2
        cd ~ && git clone https://github.com/json1c/telegram-raid-botnet.git ~/telegram-raid-botnet && cd telegram-raid-botnet && python main.py
    else    
        clear
        echo "Something went wrong, try to install botnet from instruction"
        exit 1;    
    fi
else
    clear
    echo "OS NOT DETECTED, couldn't install packages for your system..."
    echo "Try to install botnet from instruction"
    exit 1;
fi

exit 0
