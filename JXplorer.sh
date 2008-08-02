#!/bin/sh

JX_OPTS=-Djxplorer.config="$HOME/.JXplorer"
JX_JAVADIR=/usr/share/java/JXplorer
JX_DATADIR=/usr/share/JXplorer

# Get config.
[ -f /etc/sysconfig/jxplorer ] && . /etc/sysconfig/jxplorer

JAVA_BIN="$JAVA_HOME/bin/java"

if ! [ -d "$HOME/.JXplorer" ]; then
  mkdir "$HOME/.JXplorer"
  cp /etc/JXplorer/connections.txt "$HOME/.JXplorer/connections.txt"
  ln -s /etc/JXplorer/log4j.xml "$HOME/.JXplorer/log4j.xml"
  cp /etc/JXplorer/jxconfig.txt "$HOME/.JXplorer/jxconfig.txt"
  ln -s $JX_DATADIR/templates "$HOME/.JXplorer/templates"
  ln -s $JX_DATADIR/security "$HOME/.JXplorer/security"
fi

cd "$HOME/.JXplorer"
CLASSPATH=`build-classpath junit jhall`
CLASSPATH="$CLASSPATH:$JX_JAVADIR/jxplorer.jar:$JX_JAVADIR/help.jar"
export CLASSPATH

if [ "$#" == "0" ]; then
    exec "$JAVA_BIN" $JX_OPTS com.ca.directory.jxplorer.JXplorer < /dev/null > /dev/null 2>&1 &
  else if [ "$1" = "console" ] ; then
    exec "$JAVA_BIN" $JX_OPTS com.ca.directory.jxplorer.JXplorer
  else
    echo "Usage: $0 [console|help]"
  fi
fi
