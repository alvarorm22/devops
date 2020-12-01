#!/bin/bash

main() {
  setup_dependencies

  echo "SUCCESS:
  Done! Finished setting up Travis machine.
  "
}




setup_dependencies() {
  echo "INFO:
  Setting up dependencies.
  "

  sudo apt update -y
  sudo apt install realpath python python-pip -y
  sudo apt install --only-upgrade docker-ce -y

  sudo pip install docker-compose || true

  docker info
  docker-compose --version
}

main

