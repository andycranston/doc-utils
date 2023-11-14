#!/bin/bash
#
# @(!--#) @(#) update-notes.sh, sversion 0.1.0, fversion 002, 14-november-2023
#
# update the index.html files in all directories in the notes directory structure
#

#
# Main
#

PATH=/bin:/usr/bin:$HOME/bin
export PATH

progname=`basename $0`

cd $HOME/www/html
retcode=$?

if [ $retcode -ne 0 ]
then
	echo "$progname: unable to change into web server directory" 1>&2
	exit 1
fi

dirlist=`find notes -type d -print | sort`

if [ "$dirlist" == "" ]
then
	echo "$progname: no notes directory or sub-directories" 1>&2
	exit 1
fi

for dir in $dirlist
do
	(
		echo $dir

		cd $dir
		retcode=$?

		if [ $retcode -ne 0 ]
		then
			echo "$progname: unable to change to sub-diectory \"$dir\"" 1>&2
		else
			if [ ! -r index.title ]
			then
				echo "$progname: INFO: no $dir/index.title file" 1>&2
			fi

			ls *.md > /dev/null 2>&1
			retcode=$?

			if [ $retcode -ne 0 ]
			then
				/bin/true
				# echo "$progname: INFO: no markdown files in $dir" 1>&2
			else
				for markdown in *.md
				do
					htmldoc=`basename $markdown .md`.html
					md2html $markdown > $htmldoc
				done
			fi

			mkindex
		fi
	)
done

exit 0
