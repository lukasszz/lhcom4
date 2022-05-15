docker run --rm --name postgresql -e POSTRES_PASSWORD=pass -d -p 5432:5432 -v /Users/lukasz/docker_volumes/postgres:/var/lib/postgresql/data:z postgres 
