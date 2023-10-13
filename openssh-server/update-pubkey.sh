#!/bin/bash

mkdir -p "$PUBLIC_KEY_DIR"

if [[ -n "$PUBLIC_KEY" ]]; then
    if ! grep -q "${PUBLIC_KEY}" /config/.ssh/authorized_keys; then
        echo "$PUBLIC_KEY" >> /config/.ssh/authorized_keys
        echo "Public key from env variable added"
    fi
fi

if [[ -n "$PUBLIC_KEY_URL" ]]; then
    PUBLIC_KEY_DOWNLOADED=$(curl -s "$PUBLIC_KEY_URL")
    if ! grep -q "$PUBLIC_KEY_DOWNLOADED" /config/.ssh/authorized_keys; then
        echo "$PUBLIC_KEY_DOWNLOADED" >> /config/.ssh/authorized_keys
        echo "Public key downloaded from '$PUBLIC_KEY_URL' added"
    fi
fi

if [[ -n "$PUBLIC_KEY_FILE" ]] && [[ -f "$PUBLIC_KEY_FILE" ]]; then
    PUBLIC_KEY2=$(cat "$PUBLIC_KEY_FILE")
    if ! grep -q "$PUBLIC_KEY2" /config/.ssh/authorized_keys; then
        echo "$PUBLIC_KEY2" >> /config/.ssh/authorized_keys
        echo "Public key from file added"
    fi
fi

if [[ -d "$PUBLIC_KEY_DIR" ]]; then
    for F in "${PUBLIC_KEY_DIR}"/*; do
        PUBLIC_KEYN=$(cat "$F")
        if ! grep -q "$PUBLIC_KEYN" /config/.ssh/authorized_keys; then
            echo "$PUBLIC_KEYN" >> /config/.ssh/authorized_keys
            echo "Public key from file '$F' added"
        fi
    done
fi