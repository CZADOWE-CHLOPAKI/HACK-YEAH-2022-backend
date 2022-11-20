docker build . -t sendhybridgov-back:1.0

docker tag sendhybridgov-back:1.0 registry.digitalocean.com/sea/sendhybridgov-back:1.0
docker push registry.digitalocean.com/sea/sendhybridgov-back:1.0