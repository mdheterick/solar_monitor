git pull --rebase
cp monitor.py ../services
cp server.py ../services
systemctl --user restart monitor.service
systemctl --user restart solar_server.service