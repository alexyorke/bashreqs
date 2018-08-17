# bashreqs
pipreqs for bash scripts. Not affiliated with pipreqs.

Run `python3 bashreqs.py path-to-bash-script` to generate a report containing all of the packages needed to run a bash script. This repo is still in beta, so weird things might happen.

`bashreqs` assumes that the script runs fine on your computer before it searches for packages (this app should be run on the developer's computer to generate the dependency requirements.) However, **finding requirements, even if the package is not installed on your local computer** would be an awesome feature to add to `bashreqs.`

Here's a report generated from https://github.com/topkecleon/telegram-bot-bash/blob/master/bashbot.sh (not affiliated with telegram-bot-bash):


```
klibc-utils==2.0.4-9 # because of /bin/cat
sed==4.4-1
tmux==2.3-4
less==481-2.1
bash==4.4-5 # because of /usr/bin/clear
grep==2.27-2 # because of /bin/egrep, 
curl==7.52.1-5+deb9u3
git==1:2.11.0-3+deb9u2
coreutils==8.26-3 # because of /usr/bin/wc, /bin/rm, /usr/bin/tail, /usr/bin/cut, /bin/echo, /usr/bin/mkfifo
```

## Roadmap

Detect if an executable contains any system calls to execl, execle, execlp, execv, execve, execvp, or vfork as the executable may run another program (for example, the executable strace can run another program.) If this condition is true, the executable will be investigated to determine if it actually runs another program, and what position the program must be in to run it in the command line arguments. This allows the program's command line argument(s) to be interpreted as a command, and so will be added to the bashreqs list (http://refspecs.linuxbase.org/LSB_1.3.0/PPC64/spec/baselib.html). The program `nm` can find all system calls.
