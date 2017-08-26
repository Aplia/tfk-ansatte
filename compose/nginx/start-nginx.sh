#!/usr/bin/env bash
set -e

if [ "${USE_AWS-no}" = "yes" ]; then
    export HOST_IP=`curl http://169.254.169.254/latest/meta-data/local-ipv4 2>/dev/null`
fi
if [ -z $DOMAIN_SPACE_LIST ]; then
    export DOMAIN_SPACE_LIST="tfk-ansatte.aplia.no"
fi
if [ -n $WEB_PORT ]; then
    echo "Web service accessible from port $WEB_PORT"
fi
/usr/local/bin/ep /etc/nginx/nginx.conf -- /usr/sbin/nginx -g "daemon off;"
