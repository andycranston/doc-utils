#!/bin/bash
#
# @(!--#) @(#) Install.sh, version 003, 26-october-2023
#
# install the various python and shell scripts to $HOME/bin
#

set -u

PATH=/bin:/usr/bin
export PATH

progname=`basename $0`

username=`id | cut -d'(' -f2 | cut -d')' -f1`

if [ "$username" = "root" ]
then
  echo "$progname: do NOT run this script as root user!!!" 1>&2
  exit 2
fi

if [ ! -d $HOME/bin ]
then
  echo "$progname: directory \"$HOME/bin\" does not exist or is not a directory" 1>&2
  exit 2
fi

if [ ! -w $HOME/bin ]
then
  echo "$progname: directory \"$HOME/bin\" is not writable" 1>&2
  exit 2
fi

for script in *.sh *.py
do
  if [ "$script" != "$progname" ]
  then
    echo "copying script $script"
    cp -p $script $HOME/bin/$script
    chmod u=rwx,go=rx $HOME/bin/$script

    piececount=`echo $script | sed 's/\./ /g' | wc -w | awk '{ print $1 }'`

    if [ $piececount -ge 1 ]
    then
      suffix=`echo $script | sed 's/\./ /g' | awk '{ print $'$piececount' }'`

      b=`basename $script .${suffix}`

      rm -f $HOME/bin/$b

      ( cd $HOME/bin && ln -s $script $b )
    fi
  fi
done

exit 0
