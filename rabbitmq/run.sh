#!/bin/bash
echo "Setting up rabbitmq"

RABBITMQ_PASSWORD=${RABBITMQ_PASSWORD:-"password"}
RABBITMQ_USER=${RABBITMQ_USER:-"guest"}

service rabbitmq-server restart >/dev/null 2>&1
echo "Create user ${RABBITMQ_USER}"
rabbitmqctl delete_user guest
rabbitmqctl add_user ${RABBITMQ_USER} ${RABBITMQ_PASSWORD}
rabbitmqctl set_user_tags ${RABBITMQ_USER} administrator
rabbitmqctl set_permissions -p / ${RABBITMQ_USER} ".*" ".*" ".*"

#cat > /etc/rabbitmq/rabbitmq.config <<EOF
#[
#	{rabbit, [{default_user, <<"${RABBITMQ_USER}">>},{default_pass, <<"${RABBITMQ_PASSWORD}">>},{tcp_listeners, [{"0.0.0.0", 5672}]}]}
#].
#EOF
#echo "Done!"



echo "Stopping rabbitmq"
service rabbitmq-server  stop >/dev/null 2>&1

echo "Starting rabbitmq using supervisord..."
exec /usr/bin/supervisord -n
