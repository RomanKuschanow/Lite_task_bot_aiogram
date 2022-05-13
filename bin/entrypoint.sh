#!/bin/sh

pw_migrate migrate --database $(python _get_database_url.py) --directory ./migrations

nohup python api.py &

if [ -z "$WEBHOOK_PATH" ]
then
      python app.py
else
      python webhook.py
fi