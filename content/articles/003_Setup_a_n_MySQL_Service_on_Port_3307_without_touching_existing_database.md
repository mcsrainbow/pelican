Title: Setup a new MySQL Service on Port 3307 without touching existing database
Date: 2014-09-25 18:18
Category: Linux$Unix
Tags: MySQL
Author: mcsrainbow
Summary:**1. Create directories for MySQL_3307** <p>`$ sudo mkdir -p /opt/mysql_3307/{data,tmp,run,binlogs,log}` <p>`$ sudo chown mysql:mysql /opt/mysql_3307/{data,tmp,run,binlogs,log}` <p>**2. Create configuration file for MySQL_3307** <p>`$ sudo vim /etc/my_3307.cnf` <p>...

**1. Create directories for MySQL_3307**

`$ sudo mkdir -p /opt/mysql_3307/{data,tmp,run,binlogs,log}`

`$ sudo chown mysql:mysql /opt/mysql_3307/{data,tmp,run,binlogs,log}`

**2. Create configuration file for MySQL_3307**

`$ sudo vim /etc/my_3307.cnf`

```
[mysqld]
# basic settings
datadir = /opt/mysql_3307/data
tmpdir = /opt/mysql_3307/tmp
socket = /opt/mysql_3307/run/mysqld.sock
port = 3307
pid-file = /opt/mysql_3307/run/mysqld.pid

# innodb settings
default-storage-engine = INNODB
innodb_file_per_table = 1
log-bin = /opt/mysql_3307/binlogs/bin-log-mysqld
log-bin-index = /opt/mysql_3307/binlogs/bin-log-mysqld.index
innodb_data_home_dir = /opt/mysql_3307/data
innodb_data_file_path = ibdata1:10M:autoextend
innodb_log_group_home_dir = /opt/mysql_3307/data

# server id
server-id=33071

# other settings
[mysqld_safe]
log-error = /opt/mysql_3307/log/mysqld.log
pid-file = /opt/mysql_3307/run/mysqld.pid
open-files-limit = 8192

[mysqlhotcopy]
interactive-timeout

[client]
port = 3307
socket = /opt/mysql_3307/run/mysqld.sock
default-character-set = utf8
```

**3. Initialize MySQL_3307**

`$ sudo -i`

`# su - mysql`

`$ mysql_install_db --user=mysql --datadir=/opt/mysql_3307/data/ --defaults-file=/etc/my_3307.cnf`

`$ exit`

`# exit`

**4. Start MySQL_3307**

`$ sudo mysqld_safe --defaults-file=/etc/my_3307.cnf --user=mysql >/dev/null 2>&1 &`

**5. Stop MySQL_3307**

`$ sudo pkill -kill -f "/etc/my_3307.cnf"`

**6. Connect to MySQL_3307**

Must use mysql_3307 to connect MySQL_3307 if you use mysql client on local.

Because `-P 3307` and `--port=3307` not work, mysql client will still connect the default port 3306.

Have to connect via socket file.

On other servers, it's ok. I searched on Google, this might be a bug.

`$ alias mysql_3307='mysql -S /opt/mysql_3307/run/mysqld.sock'`

`$ mysql_3307 -uroot -p`

**7. Create service script for MySQL_3307**

`$ sudo vim /etc/init.d/mysql_3307`

```
#!/bin/sh
#
# MySQL daemon on Port 3307 start/stop/status script.
# by Dong Guo at 2014-03-19
#
 
CONF="/etc/my_3307.cnf"
PIDFILE="/opt/mysql_3307/run/mysqld.pid"
 
function check_root(){
    if [ $EUID -ne 0 ]; then
        echo "This script must be run as root" 1>&2
        exit 1
    fi
}
 
status(){
  if test -s "${PIDFILE}"; then
    read mysqld_pid < "${PIDFILE}"
    if kill -0 ${mysqld_pid} 2>/dev/null ; then
      echo "MySQL (on Port 3307) running (${mysqld_pid})"
      exit 0
    else
      echo "MySQL (on Port 3307) is not running, but PID file exists"
      exit 1
    fi
  else
    echo "MySQL (on Port 3307) is not running"
    exit 2
  fi
}
 
start(){
  if test -s "${PIDFILE}"; then
    read mysqld_pid < "${PIDFILE}"
    if kill -0 ${mysqld_pid} 2>/dev/null ; then
      echo "MySQL (on Port 3307) is already running (${mysqld_pid})"
      exit 0
    else
      echo "MySQL (on Port 3307) is not running, but PID file exists"
      exit 1
    fi
  else
    echo "Starting MySQL (on Port 3307)"
    mysqld_safe --defaults-file=${CONF} --user=mysql >/dev/null 2>&1 &
  fi
}
 
stop(){
  if test -s "${PIDFILE}"; then
    read mysqld_pid < "${PIDFILE}"
    if kill -0 ${mysqld_pid} 2>/dev/null ; then
      echo "Stopping MySQL (on Port 3307)"
      if pkill -kill -f "${CONF}" ; then
        rm ${PIDFILE}
      fi
    else
      echo "MySQL (on Port 3307) is not running, but PID file exists"
      exit 1
    fi
  else
    echo "MySQL (on Port 3307) is not running"
    exit 2
  fi
}
 
check_root
case "$1" in
    start)
        start
        sleep 2
        status
        ;;
    stop)
        stop
        sleep 2
        status
        ;;
    status)
        status
        ;;
    *)
        echo $"Usage: $0 {start|stop|status}"
        exit 2
esac

```

`$ sudo chmod +x /etc/init.d/mysql_3307`

`$ sudo /etc/init.d/mysql_3307 status`
