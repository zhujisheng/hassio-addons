#!/usr/bin/with-contenv bashio

CONFIG_PATH=/data/options.json

HOST=$(jq --raw-output ".frp_server" $CONFIG_PATH)
PORT=$(jq --raw-output ".frp_server_port" $CONFIG_PATH)
TOKEN=$(jq --raw-output ".frp_token" $CONFIG_PATH)
SERVER_LOCAL=$(jq --raw-output ".local_host" $CONFIG_PATH)
PORT_LOCAL=$(jq --raw-output ".local_port" $CONFIG_PATH)
TYPE=$(jq --raw-output ".tunnel_type" $CONFIG_PATH)

HTTP_DOMAIN=$(jq --raw-output ".http_domain" $CONFIG_PATH)
HTTP_SUBDOMAIN_HOST=$(jq --raw-output ".http_subdomain_host" $CONFIG_PATH)
TCP_PORT_REMOTE=$(jq --raw-output ".tcp_remote_port" $CONFIG_PATH)

if [[ "$HTTP_SUBDOMAIN_HOST" == "null" ]]; then
    HTTP_SUBDOMAIN_HOST=$(cat /proc/sys/kernel/random/uuid)
fi

if [[ ${TYPE} == "http" ]]; then

    URL=http://${HTTP_SUBDOMAIN_HOST}.${HTTP_DOMAIN}

    echo You can visit from Internet at the URL: ${URL}

    /frpc http -s ${HOST}:${PORT} --sd ${HTTP_SUBDOMAIN_HOST} -i ${SERVER_LOCAL} -l ${PORT_LOCAL} -t ${TOKEN} -n hachina_${HTTP_SUBDOMAIN_HOST} --locations /

fi

if [[ ${TYPE} == "tcp" ]]; then

    URL=http://${HOST}:${TCP_PORT_REMOTE}

    echo You can visit from Internet at the URL: ${URL}

    /frpc tcp -s ${HOST}:${PORT} -i ${SERVER_LOCAL} -l ${PORT_LOCAL} -t ${TOKEN} -r ${TCP_PORT_REMOTE} -n hachina_${HTTP_SUBDOMAIN_HOST}

fi
