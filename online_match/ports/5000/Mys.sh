#!/bin/bash
pwd
echo $1 $2 $3
cd $1
chmod 755 Server.sh
chmod 755 Client1.sh
chmod 755 Client2.sh
./Server.sh $1/server &
sleep 2
./Client1.sh $1/client1 $2 &
sleep 1
./Client2.sh $1/client2 $2 &

