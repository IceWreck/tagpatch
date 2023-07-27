# tagpatch

CLI tool which applies common/repetitive patches to music tags.
You should use a GUI tool like [KDE's Kid3](https://kid3.kde.org/) for complicated patches.

```
[icewreck@zacian]$ tagpatch --help
Usage: tagpatch [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  artist-name  A patch which replaces the seperator in the `Artist` tag...
  embed-lrc
```

```
[icewreck@zacian]$ tagpatch artist-name --help
Usage: tagpatch artist-name [OPTIONS]

  A patch which replaces the seperator in the `Artist` tag with a new
  seperator.

Options:
  -s, --src PATH            [default: /home/icewreck/Development/tagpatch]
  -d, --dst PATH
  -y, --assume-yes
  -n, --nested
  --help                    Show this message and exit.
```
