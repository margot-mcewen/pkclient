# pkclient
Python client for pktriggercord server, remote control of Pentax cameras

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
