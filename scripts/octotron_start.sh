#!/bin/bash
set -u
cd "$(dirname "$0")"

source ./mail_config.sh

bash ./single_mail.sh "$RECIPIENT" "$PREFIX Octotron started" ""
