#!/bin/bash
#cd
cd $1
if [ $2 == 'C++' ]
then
#	echo c++ is running
#	cmake -G "Unix Makefiles"
#	make
	./Abalone
elif [ $2 == 'py' ]
then
	echo python is running
	python3 client.py
elif [ $2 == 'java' ]
then
	echo java is running
	java -jar client.jar	
else
	echo type of code is wrong
fi
