# cat-herder

Simple online scheduler for weekly events.

## License

[MIT](/LICENSE)

## Getting Started

### Install dependencies
- python 2.7
- pip
- `[sudo] pip install virtualenv`

### Load it up!

```
git clone https://github.com/mpaulweeks/cat-herder.git
cd cat-herder
./install/setup.sh
```

and then you're done! All of the helper scripts setup and use virtualenv in the background for you.

### Helper scripts

All scripts must be run from the top-level directory: `cat-herder/`
- `./bash/run_server.py` starts up the server on port 5800 in your current shell. Shutdown with `Ctrl+C`
- `./bash/background.py` starts up the server in the background.
- `./bash/kill_server.py` kills the current server process, regardless of foreground/background.