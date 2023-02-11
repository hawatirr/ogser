#!/bin/bash

# Check the status of JupyterHub
status=$(docker-compose ps | grep Exit | wc -l)

# If there are any nodes in a "Exit" state, restart JupyterHub
if [ $status -ne 0 ]; then
  echo "JupyterHub nodes in an error state, restarting JupyterHub..."
  docker-compose down
  docker-compose up -d
else
  echo "JupyterHub is running normally."
fi

#!/bin/bash

# Start a worker for the user
jupyterhub-singleuser \
  --port=8888 \
  --ip=0.0.0.0 \
  --user=$JPY_USER \
  --cookie-name=$JPY_COOKIE_NAME \
  --base-url=$JPY_BASE_URL \
  --hub-prefix=$JPY_HUB_PREFIX \
  --hub-api-url=$JPY_HUB_API_URL &

# Wait for the worker to start
sleep 30

# Connect to the worker
exec socat TCP4-LISTEN:$JPY_PORT,fork UNIX-CLIENT:\"$JPY_CONTROL_SOCKET\"

# JupyterHub configuration
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.container_image = 'jupyter/datascience-notebook:latest'
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.start_singleuser = '/path/to/start_single_user.sh'

c.JupyterHub.services = [
    {
        'name': 'spawner',
        'admin': True,
        'command': ['python3', '-m', 'dockerspawner.spawner', '--min-workers=X', '--max-workers=Y'],
    }
]

c.JupyterHub.authenticator_class = 'oauthenticator.GoogleOAuthenticator'
c.GoogleOAuthenticator.client_id = 'YOUR_CLIENT_ID'
c.GoogleOAuthenticator.client_secret = 'YOUR_CLIENT_SECRET'
c.GoogleOAuthenticator.oauth_callback_url = 'YOUR_CALLBACK_URL'
