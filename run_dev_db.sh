podman run --rm --name postgres12 -e POSTGRES_PASSWORD=docker -d -p 5432:5432 -v $HOME/podman/volumes/postgres12:/var/lib/postgresql/data:z postgres:12
