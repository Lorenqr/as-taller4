#!/bin/sh
# wait-for-it.sh

host="$1"
shift
cmd="$@"

until nc -z ${host%:*} ${host#*:}; do
    echo "Esperando a $host..."
    sleep 2
done

exec $cmd