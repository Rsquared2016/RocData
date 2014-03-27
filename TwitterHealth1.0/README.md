# Fountin

## Backend Data Collection 
The backend daemon runs automatically after reboot.

(see `crontab -l` for explanation of what happens).

It is safe to log-off after the deamon is running, as we are using nohup.
The status of the backend can be checked with: `backend/check_status.sh`

## Frontend Web Interface
To compile and run the frontend: 
1) you need to install maven, Java 1.6+

```bash 
cd TwitterHealth/frontend
./dev_run_webapp.sh 

#-------------------------------------------------------------------------
# OPTIONAL --- You shouldn't need this for development.
# You can optionally redirect port 80 to 8080 on your local machine
# This is what we did for public facing servers.
#-------------------------------------------------------------------------

# on gnu/linux:
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080

# on mac:
ipfw add 100 fwd 127.0.0.1,8080 tcp from any to any 80 in
```

go to http://localhost:8080


