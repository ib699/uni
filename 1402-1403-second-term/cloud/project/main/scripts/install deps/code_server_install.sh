#!/usr/bin/env bash

curl -fsSL https://code-server.dev/install.sh | sh
sudo systemctl enable --now code-server@$USER

sudo echo "[Unit]
Description=code-server
After=network.target

[Service]
Type=exec
ExecStart=/usr/bin/code-server --bind-addr 0.0.0.0:8080
Restart=always
User=%i

[Install]
WantedBy=default.target" > /lib/systemd/system/code-server@.service

sudo systemctl daemon-reload
sudo systemctl status code-server@root.service
