#!/bin/sh


nohup python wayforpay.py &

if [ -z "$WEBHOOK_PATH" ]
then
      python app.py
else
      python webhook.py
fi