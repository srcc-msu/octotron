#!/bin/bash
set -u
cd "$(dirname "$0")"

source ./react_config.sh
source ./mail_config.sh

bash ./composed_mail.sh "$RECIPIENT" "$PREFIX $2: $3" "$MSG"
