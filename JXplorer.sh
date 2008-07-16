#!/bin/sh

JX_OPTS=-Djxplorer.config="$HOME/.JXplorer"
JX_JAVADIR=/usr/share/java/JXplorer
JX_DATADIR=/usr/share/JXplorer

[ -r /etc/sysconfig/jxplorer ] && . /etc/sysconfig/jxplorer

JAVA_BIN="$JAVA_HOME/bin/java"

if ! [ -d "$HOME/.JXplorer" ]; then
  mkdir "$HOME/.JXplorer"
  cp /etc/JXplorer/connections.txt "$HOME/.JXplorer/connections.txt"
  ln -s /etc/JXplorer/log4j.xml "$HOME/.JXplorer/log4j.xml"
  ln -s /etc/JXplorer/jxconfig.txt "$HOME/.JXplorer/jxconfig.txt"
fi

echo "starting JXplorer..."
echo
FAIL=0
cd "$JX_DATADIR"
CLASSPATH=`build-classpath junit jhall`
CLASSPATH="$CLASSPATH:$JX_JAVADIR/jxplorer.jar:$JX_JAVADIR/help.jar"
export CLASSPATH
if [ "$1" = "console" ] ; then
    "$JAVA_BIN" $JX_OPTS com.ca.directory.jxplorer.JXplorer

    if [ "$?" != "0" ]; then
        FAIL=1
    fi
else
    echo "Use \"$0 console\" if you want logging to the console"
    "$JAVA_BIN" $JX_OPTS com.ca.directory.jxplorer.JXplorer  >/dev/null 2>&1

    if [ "$?" != "0" ]; then
        FAIL=1
    fi
fi

# Check for success
if [ $FAIL = 0 ]; then
    exit 0
fi

cat <<-!

=========================
JXplorer failed to start
=========================
Please ensure that you have appropriate "xhost" access to the machine you are
running this from. Make sure the DISPLAY environment variable is set correctly.
Otherwise, ask your Unix Systems Administrator for more information on running
X Windows applications.

If you require more information run "$0 console" and check the
error produced.
!

exit 1
