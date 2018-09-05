#!/bin/bash
#cd
pwd > /home/moeb/Desktop/pwd.txt
echo $$ > /home/moeb/Desktop/$3.txt
echo $3
cd $1
if [ $2 == 'C++' ]
then
	echo c++ is running
#	cmake -G "Unix Makefiles"
#	make
#	./Abalone
	./Abalone 2>&1 > /dev/null
elif [ $2 == 'Python3' ]
then
	echo python is running
	python3 client.py 2>&1 > /dev/null
elif [ $2 == 'Java' ]
then
	echo java is running
	java -jar client.jar 2>&1 > /dev/null
else
	echo type of code is wrong
fi
