docker run -p 53:53/udp -p 53:53/tcp --rm --env-file .env --network dns --name server %1
