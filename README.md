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

### Deploy

Push changes to `origin/master`

SSH into server, then run these commands:
```
./bash/kill_server.sh
git checkout master
git pull
./bash/bg_cat.sh
```

### Helper scripts

All scripts must be run from the top-level directory: `cat-herder/`

- Start up the server on port 5800 in your current shell, and stores the process ID in `temp/server.pid`
```
./bash/server_cat.sh
```

- Start up the server, but in the background.
```
./bash/bg_cat.sh
```

- Kill the current server process, regardless of foreground/background.
```
./bash/kill_server.sh
```
