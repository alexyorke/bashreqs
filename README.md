# bashreqs
pipreqs for bash scripts. Not affiliated with pipreqs.

After cloning, run `pip3 install -r requirement.txt` then `python3 bashreqs.py path-to-bash-script` to generate a report containing all of the Debian and Ubuntu-based packages needed to run a bash script. If the executables are not packages, then `bashreqs` will just list the path to the executable.

## Requirements

Needs `apt-get`, `aptitude`, `nm`, and `python3` to be installed.

`bashreqs` assumes that the script runs fine on your computer before it searches for packages (this app should be run on the developer's computer to generate the dependency requirements.) However, **finding requirements, even if the package is not installed on your local computer** would be an awesome feature to add to `bashreqs.` Having said that, `bashreqs` will notify you if the bash program contains a package which is obsolete (i.e. cannot be re-installed on another computer, because it was installed from a deb file, or is no longer available in the official repos.)

Here's a report generated from https://github.com/topkecleon/telegram-bot-bash/blob/master/bashbot.sh (not affiliated with telegram-bot-bash):


```
# warning: /usr/bin/tmux calls execv, execvp, execl which could cause missing req
# warning: /usr/bin/git calls execv, execvp, execl, execlp, execl which could cause missing req
coreutils==8.26-3 # because of /bin/rm, /bin/cat, /usr/bin/wc, /usr/bin/mkfifo, /usr/bin/cut, /usr/bin/tail, /bin/echo
curl==7.52.1-5+deb9u3
git==1:2.11.0-3+deb9u2
grep==2.27-2 # because of /bin/egrep,
less==481-2.1
ncurses-bin==6.0+20161126-1+deb9u1 # because of /usr/bin/clear
sed==4.4-1
tmux==2.3-4
```

`bashreqs` generates warnings for executables which contain a system call that could instantiate another program. This means that the command-line arguments to a program (e.g. `strace <command>`) might supervise another executable, or just a string (in which case `bashreq` may not be able to sufficiently determine the requirements.) For example, `strace echo hello` has two requirements: `strace` and `echo`, but `bashreq` only sees `strace`, and so generates a warning because `strace`'s executable contains an exec call (allowing it to run arbitrary programs, such as echo.)

## Report too bloated? Want to hide common utils like echo, bash, and sed for example?

No problem. `bashreqs` lets you hide the top x% of packages installed on Ubuntu computers. For example, `ncurses-base` is installed on 99.877% of computers (from the popcon data), so it's highly unlikely that a user will need to install it, as they probably already have it installed.

## Dependency-free executable

Head on over to https://github.com/Decagon/bashreqs/releases/tag/v0.1-alpha to find a Linux executable which is dependency-less (except for the shell commands which are probably pre-installed.) No Python needed.

## Roadmap

- using the flagged executables (warnings), check if they have the ability to call another program (e.g. strace can supervise another executable) so that requirements can be parsed more accurately.

- attempt to find dependencies inside of an executable that is not managed with a package manager

- add support for other package managers (e.g. rpm, yum, etc.)
