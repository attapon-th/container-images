#!/bin/bash

ROOT_DIR=/opt/cronicle
CONF_DIR=$ROOT_DIR/conf
BIN_DIR=$ROOT_DIR/bin
# DATA_DIR needs to be the same as the exposed Docker volume in Dockerfile
DATA_DIR=$ROOT_DIR/data
# LOGS_DIR needs to be the same as the exposed Docker volume in Dockerfile
LOGS_DIR=$ROOT_DIR/logs
# PLUGINS_DIR needs to be the same as the exposed Docker volume in Dockerfile
PLUGINS_DIR=$ROOT_DIR/plugins

# The env variables below are needed for Docker and cannot be overwritten
export CRONICLE_Storage__Filesystem__base_dir=${DATA_DIR}
export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
export CRONICLE_echo=1
export CRONICLE_foreground=1

# if [ ! -d $ROOT_DIR/venv ]
# then
#   python3 -m venv $ROOT_DIR/venv
# fi
# source "$ROOT_DIR/venv/bin/activate"

# Only run setup when setup needs to be done
if [ ! -f $DATA_DIR/.setup_done ]
then
  cp $CONF_DIR/config.json $CONF_DIR/config.json.origin

  if [ -f $DATA_DIR/config.json.import ]
  then
    # Move in custom configuration
    cp $DATA_DIR/config.json.import $CONF_DIR/config.json
  fi
  if [ -z "$WORKER" ]; then
    $BIN_DIR/control.sh setup
  fi

  # Create plugins directory
  mkdir -p $PLUGINS_DIR

  # Marking setup done
  touch $DATA_DIR/.setup_done
fi

PID_FILE=$LOGS_DIR/cronicled.pid
if [ -f "$PID_FILE" ]; then
    echo "Removing old PID file: $PID_FILE"
    rm -f $PID_FILE
fi

if [ -e /opt/cronicle/logs/_plugin_imported ]
then
  echo "Plugin already imported!"
else
  echo "Importing plugin..."
  /opt/cronicle/bin/control.sh import /opt/cronicle/import/plugins.pixl
  touch /opt/cronicle/logs/_plugin_imported
  echo "Plugin successfully imported!"
fi

if [ -n "$1" ];
then
  exec "$@"
else
  /opt/cronicle/bin/control.sh start
fi