pushd client
npm run build
popd
scp -r ./client/dist pi@192.168.4.55:~/services/client/