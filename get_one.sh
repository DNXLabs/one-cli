#!/bin/bash

os=${OSTYPE//[0-9.-]*/}

case "$os" in
  darwin)
    sudo curl -L https://github.com/DNXLabs/one-cli/releases/latest/download/one_macos_amd64 -o /usr/local/bin/one
    ;;

  msys)
    echo 'No support for Windows platform'
    ;;

  linux)
    sudo curl -L https://github.com/DNXLabs/one-cli/releases/latest/download/one_linux_amd64 -o /usr/local/bin/one
    ;;
  *)

  echo "Unknown Operating system $OSTYPE"
  exit 1
esac

sudo chmod +x /usr/local/bin/one