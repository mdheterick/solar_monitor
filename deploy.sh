pushd client
npm run build
popd
scp -r ./client/dist pi@192.168.4.55:~/services/client/
scp server.py pi@192.168.4.55:~/services/
ssh pi@192.168.4.55 "sed -i 's/\r$//' services/server.py"
scp monitor.py pi@192.168.4.55:~/services/
ssh pi@192.168.4.55 "sed -i 's/\r$//' services/monitor.py"