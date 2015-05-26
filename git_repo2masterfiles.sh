#!/bin/bash

# This script is in root's crontab
# It copies from git repo to /var/cfengine/masterfiles
# root's crontab entry:
# */1 * * * * /home/git/custom_promises.stg/custom_promises/git_repo2masterfiles.sh

git_staging_dir="/home/git/custom_promises.stg"
cfe_masterfiles_dir="/var/cfengine/masterfiles"

/usr/bin/rsync -av --no-p --delete ${git_staging_dir}/custom_promises/custom_policies/ ${cfe_masterfiles_dir}/custom_policies/

/usr/bin/rsync --no-p ${git_staging_dir}/custom_promises/promise_cf/promises.cf ${cfe_masterfiles_dir}/promises.cf

/usr/bin/rsync -av --no-p --delete ${git_staging_dir}/custom_promises/modules/ /var/cfengine/modules/

/bin/chown root:root /var/cfengine/modules/.
/bin/chown root:root /var/cfengine/modules/*
