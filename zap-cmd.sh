mkdir /zap/wrk
zap-api-scan.py -t https://payapi-staging.shore.com/api/account -f openapi --hook=hook.py -r report.html
