# tagpatch

CLI tool which automatically applies common/repetitive patches to music tags.
You should use a GUI tool like [KDE's Kid3](https://kid3.kde.org/) for complicated patches.

## Install

**From GitHub**

```shell
sudo wget https://github.com/IceWreck/tagpatch/releases/download/v0.1.3/tagpatch-v0.1.3 \
  -O /usr/local/bin/tagpatch && sudo chmod +x /usr/local/bin/tagpatch
```


**Using pip**

```
pip install tagpatch
```

It's recommended to install this with `--user` or inside a venv. You can also use `pipx` or `uvx`.

## Example

```shell
tagpatch embed-lrc -n -s ~/Music
```
The changes will be highlighted in red. Confirm to continue.

![scrot](files/scrot1.png)


## Usage

```
$ tagpatch
 Usage: tagpatch [OPTIONS] COMMAND [ARGS]...

 CLI tool which applies common patches to music tags.

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ artist-name    A patch which replaces existing delimiters in the `Artist`    │
│                tag with the `/` separator.                                   │
│ embed-lrc      A patch which embeds .lrc files of the same name into the     │
│                track file.                                                   │
│ download-lrc   A patch which downloads .lrc files from lrclib.net if not     │
│                present.                                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

```
$ tagpatch embed-lrc --help
 Usage: tagpatch embed-lrc [OPTIONS]

 A patch which embeds .lrc files of the same name into the track file.

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --src         -s      PATH  [default: /home/icewreck/Development/tagpatch]   │
│ --dst         -d      PATH                                                   │
│ --assume-yes  -y                                                             │
│ --nested      -n                                                             │
│ --help                      Show this message and exit.                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

```
$ tagpatch artist-name --help
 Usage: tagpatch artist-name [OPTIONS]

 A patch which replaces existing delimiters in the `Artist` tag with the `/`
 separator.

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --src         -s      PATH  [default: /home/icewreck/Development/tagpatch]   │
│ --dst         -d      PATH                                                   │
│ --assume-yes  -y                                                             │
│ --nested      -n                                                             │
│ --help                      Show this message and exit.                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

```
$ tagpatch download-lrc --help
 Usage: tagpatch download-lrc [OPTIONS]

 A patch which downloads .lrc files from lrclib.net if not present.

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --src         -s      PATH  [default: /home/icewreck/Development/tagpatch]   │
│ --assume-yes  -y                                                             │
│ --nested      -n                                                             │
│ --help                      Show this message and exit.                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```
