# Discord Bot
A discord bot that can play music.

## Run locally
Install Python requirements
```
pip install -r requirements.txt
```

Install ffmpeg and ensure environment variable is set. 

Run the main file on cmd
```
python3 main.py
```


## Run locally with docker
Build the docker image
```
docker build --tag music_bot .
```

Run the docker image
```
docker run -e TOKEN=<YOUR_BOT_TOKEN_HERE> -d music_bot
```

## Deploy on Heroku
Run the bot locally on docker

Check the container is running
```
docker ps
```

Login to your Heroku account
```
heroku login
```

Login to your Container Registry
```
heroku container:login
```

Push the Docker-based app
```
heroku container:push worker --app <YOUR_APP_NAME>
```

Deploy the changes
```
heroku container:release worker --app <YOUR_APP_NAME>
```



