# pkclient
A Python client for the pktriggercord server, allowing remote control of Pentax DSLR cameras.

![Screenshot from 2025-06-06 22-22-38](https://github.com/user-attachments/assets/ea16dd75-bd95-4abf-b697-9579dfe1d321)

I'm not a very good programmer, so if this breaks your camera it's not my fault. I've tried to put in some protections to stop you from doing anything really stupid (e.g. overflowing the camera's buffer).

This has only been tested with a [Pentax K-5 IIs](https://www.pentaxforums.com/camerareviews/pentax-k-5-iis.html), if you test another camera that [pktriggercord](https://github.com/asalamon74/pktriggercord?tab=readme-ov-file#cameras) supports then let let me know.

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

Plug your camera into a computer, switch the camera on, and run:

``` bash
pktriggercord-cli --servermode
```

### Client

On the either the same computer or on a seperate computer, run:

``` bash
python3 pkclient.py
```

> [!CAUTION]
> The camera's buffer can only hold 9 images at once.[^1]
> If you try to write more without deleting any buffers your camera will stop working until you perform a hard reset by pulling the battery.

[^1]: This is true of the K-5 IIs, a safe way to test if buffer `n` exists is by using `pk.delete_buffer(n)` and seeing if an error is reported server side

## Features

``` python
pk = pkclient("127.0.0.1", 8888)  # connect local or remote
pk.connect_server()
pk.connect_camera()
pk.get_camera_name()
pk.focus()
pk.set_aperture(2.8)
pk.set_shutter_speed("1/4")
pk.set_iso(800)
pk.delete_buffer(0)  # so you know your next photo will be in buffer 0
pk.get_buffer_type()
pk.set_buffer_type("DNG")  # can be DNG or PEF
pk.shutter()
pk.get_buffer(0, "photograph_0")  # save image to CWD
pk.stop_server()
```

## to-do

- [ ] more robust buffer protection
- [ ] test more
- [ ] better error detection
- [ ] quiet option
- [ ] no-frills version (no rich or nerd-fonts)
