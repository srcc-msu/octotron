#!/bin/bash
# reaction script, that will be called by octotron for notifications
# uses ./react_config.sh to check and convert input parameters

set -u
cd "$(dirname "$0")"

source ./react_config.sh
source ./mail_config.sh

bash ./composed_mail.sh "$RECIPIENT" "$PREFIX $SHORT" "$DATA"
