#!/bin/bash

DBPASS=$1

podman pod stop lhcom4
podman pod rm lhcom4

echo "Creating the pod..."
podman pod create --name lhcom4 -p 5432:5432 -p 9306:9306

echo "Running postgres..."
podman run --name postgres12 --pod lhcom4 -e POSTGRES_PASSWORD=$DBPASS -d \
      -v ~/podman/volumes/postgres12:/var/lib/postgresql/data:z postgres:12

echo "Preparing SphinxSearch..."
mkdir -p ~/podman/volumes/sphinxsearch/index
#cp install/sphinxsearch/sphinx.conf ~/podman/volumes/sphinxsearch

read -n1 -srp $'Now edit ~/podman/sphinxsearch/sphinx.conf, and press enter when done\n' key
echo "Generating 1st index"
podman run --pod lhcom4 -v ~/podman/volumes/sphinxsearch/index/:/opt/sphinx/index:z \
	-v ~/podman/volumes/sphinxsearch/sphinx.conf:/opt/sphinx/conf/sphinx.conf:z \
	--rm macbre/sphinxsearch indexer --all --config /opt/sphinx/conf/sphinx.conf 

echo "Running sphinxsearch..."
podman run --name sphinxsearch --pod lhcom4 -d \
	-v ~/podman/volumes/sphinxsearch/index/:/opt/sphinx/index:z \
	-v ~/podman/volumes/sphinxsearch/sphinx.conf:/opt/sphinx/conf/sphinx.conf:z \
	macbre/sphinxsearch

echo "Status: "
podman logs sphinxsearch



