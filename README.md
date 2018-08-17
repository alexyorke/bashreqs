# bashreqs
pipreqs for bash scripts. Not affiliated with pipreqs.

Run `python3 bashreqs.py path-to-bash-script` to generate a report containing all of the packages needed to run a bash script. This repo is still in beta, so weird things might happen.

`bashreqs` assumes that the script runs fine on your computer before it searches for packages (this app should be run on the developer's computer to generate the dependency requirements.) However, **finding requirements, even if the package is not installed on your local computer** would be an awesome feature to add to `bashreqs.`

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

## Dependency-free executable

Head on over to https://github.com/Decagon/bashreqs/releases/tag/v0.1-alpha to find a Linux executable which is dependency-less (except for the shell commands which are probably pre-installed.) No Python needed.

## Roadmap

Using the flagged executables (warnings), check if they have the ability to call another program (e.g. strace can supervise another executable) so that requirements can be parsed more accurately.
