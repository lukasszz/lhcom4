docker run --rm --name postgres-lhcom4 \
  -e POSTGRES_PASSWORD=pass \
  -v /Users/Shared/docker_volumes/postgres:/var/lib/postgresql/data \
  -p 5435:5432 \
  postgres