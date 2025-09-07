#!/bin/sh
# wait-for-it.sh

host="$1"
shift

until nc -z ${host%:*} ${host#*:}; do
    echo "Esperando a $host..."
    sleep 2
done

exec "$@"