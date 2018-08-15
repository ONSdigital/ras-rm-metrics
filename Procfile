# workers has to be set to 1 so as not to interleave messages
web: gunicorn -b 0.0.0.0:$PORT --workers 1 --timeout 60 metrics:app
