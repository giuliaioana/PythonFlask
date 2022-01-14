Start docker swarm:
sudo docker swarm init --advertise-addr $INSTANCE_ID
Check nodes:
docker node ls
Leave swarm at the begining:
sudo docker swarm leave --force
Deploy compose in stack:
docker stack deploy --compose-file docker-compose.yml stackdemo
Check docker compose status:
docker stack services stackdemo
Remove docker stack:
docker stack rm stackdemo
Add docker stack label:
docker node update --label-add app=true ip-10-0-1-21
docker node update --label-add app=true ip-10-0-1-159
# Install grafana worldmap panel
#sudo docker exec -i grafana bash  -c \"grafana-cli plugins install grafana-worldmap-panel\"