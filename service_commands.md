systemctl --user enable monitor.service
systemctl --user start monitor.service
systemctl --user stop monitor.service
journalctl --user-unit monitor.service