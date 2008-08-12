#!/bin/sh

[ -r /usr/share/java-utils/java-functions ] || exit 1

. /usr/share/java-utils/java-functions 

OPTIONS=-Djxplorer.config="$HOME/.JXplorer"
JX_JAVADIR=/usr/share/java/JXplorer
JX_DATADIR=/usr/share/JXplorer

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
CLASSPATH=`build-classpath junit jhall JXplorer`

if [ "$#" == "0" ]; then
    run com.ca.directory.jxplorer.JXplorer < /dev/null > /dev/null 2>&1 &
  else if [ "$1" = "console" ] ; then
    run com.ca.directory.jxplorer.JXplorer
  else
    echo "Usage: $0 [console|help]"
  fi
fi
