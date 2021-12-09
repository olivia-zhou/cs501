### Server2 
#### how to use
```
#download RabbitMQ 
docker run -dit --name Myrabbitmq -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin -p 15672:15672 -p 5672:5672 rabbitmq:management

#run server 
python3 run server.py
```
#### Archetecture 
- app/api  views function
- app/config all config files
- app/libs   all libs(include rabbitmq)
- app/models interacting with the database
- app/validtors the back-end validate


### Client 
#### how to use
```
# create a user 
mysql > insert into client (username,password) values ("rick","sunshine1");
# run client
bash > go build 
bash > ./controllerEnd -u <username>
#enter password
>>> help
>>> agents 
>>> select_agent
>>> send <cmd>
```
