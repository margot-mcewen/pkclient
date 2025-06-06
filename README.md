# pkclient
Python client for pktriggercord server, remote control of Pentax cameras

![Screenshot from 2025-06-06 22-14-39](https://github.com/user-attachments/assets/d9f1a9f0-1cfd-4b37-b004-6d872ab3a868 | width=100)

I'm not a very good programmer, so if this breaks your camera it's not my fault. I've tried to put in some protections to stop you from doing anything really stupid (e.g. overflowing the camera's buffer).

## Install

**Dependencies**: [pktriggercord](https://github.com/asalamon74/pktriggercord) *(on server)*, [rich](https://github.com/Textualize/rich) *(on client)*, [nerd-fonts](https://github.com/ryanoasis/nerd-fonts) *(on client)*
``` bash
git clone https://github.com/asalamon74/pktriggercord.git
cd pktriggercord
make clean
make
sudo make install
```

``` bash
pip3 install rich
```

## Usage

### Server

- Plug your camera into your server, switch it on, and run:

  ``` bash
  pktriggercord-cli --servermode
  ```

### Client

- On the same computer, or a on seperate computer, run:

  ``` bash
  python3 pkclient.py
  ```
