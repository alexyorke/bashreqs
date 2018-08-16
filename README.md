# bashreqs
pipreqs for bash scripts. Not affiliated with pipreqs.

Run `python3 bashreqs.py path-to-bash-script` to generate a report containing all of the packages needed to run a bash script. This repo is still in beta, so weird things might happen.

`bashreqs` assumes that the script runs fine on your computer before it searches for packages (this app should be run on the developer's computer to generate the dependency requirements.) However, **finding requirements, even if the package is not installed on your local computer** would be an awesome feature to add to `bashreqs.`

Here's a report generated from https://github.com/topkecleon/telegram-bot-bash/blob/master/bashbot.sh (not affiliated with telegram-bot-bash):


```
Installed via APT:
sed:
  Installed: 4.4-1
  Candidate: 4.4-1
  Version table:
 *** 4.4-1 500
        500 http://http.debian.net/debian stretch/main amd64 Packages
        100 /var/lib/dpkg/status

grep:
  Installed: 2.27-2
  Candidate: 2.27-2
  Version table:
 *** 2.27-2 500
        500 http://http.debian.net/debian stretch/main amd64 Packages
        100 /var/lib/dpkg/status

less:
  Installed: 481-2.1
  Candidate: 481-2.1
  Version table:
 *** 481-2.1 500
        500 http://http.debian.net/debian stretch/main amd64 Packages
        100 /var/lib/dpkg/status

tmux:
  Installed: 2.3-4
  Candidate: 2.3-4
  Version table:
 *** 2.3-4 500
        500 http://http.debian.net/debian stretch/main amd64 Packages
        100 /var/lib/dpkg/status

git:
  Installed: 1:2.11.0-3+deb9u2
  Candidate: 1:2.11.0-3+deb9u3
  Version table:
     1:2.11.0-3+deb9u3 500
        500 http://http.debian.net/debian stretch/main amd64 Packages
 *** 1:2.11.0-3+deb9u2 100
        100 /var/lib/dpkg/status

curl:
  Installed: 7.52.1-5+deb9u3
  Candidate: 7.52.1-5+deb9u6
  Version table:
     7.52.1-5+deb9u6 500
        500 http://http.debian.net/debian stretch/main amd64 Packages
 *** 7.52.1-5+deb9u3 100
        100 /var/lib/dpkg/status

Installed via other methods:
/bin/echo
/usr/bin/clear
/bin/egrep
/usr/bin/wc
/usr/bin/[
/bin/rm
/usr/bin/tail
/bin/cat
/usr/bin/cut
/usr/bin/mkfifo
```
