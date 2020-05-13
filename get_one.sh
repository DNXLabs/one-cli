#!/bin/sh

if [[ "$OSTYPE" == "linux-gnu"* ]]
then
    sudo curl -L https://github.com/DNXLabs/one-cli/releases/latest/download/one_linux_amd64 -o /usr/local/bin/one
elif [[ "$OSTYPE" == "darwin"* ]]
then
    sudo curl -L https://github.com/DNXLabs/one-cli/releases/latest/download/one_macos_amd64 -o /usr/local/bin/one
else
    echo 'No support for this platform'
fi

sudo chmod +x /usr/local/bin/one