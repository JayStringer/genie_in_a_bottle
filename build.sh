#!/bin/bash -e

DEV=${DEV:-true}
ENV_NAME=${ENV_NAME:-"genie_env"}

if [[ $DEV == true ]]; then
    # Create a virtual env with required packages for development
    virtualenv -p python3 $ENV_NAME
    . $ENV_NAME/bin/activate

    make update-dev-env

    echo "============================================================================="
    echo "'. $ENV_NAME/bin/activate' to activate the virtualenv. Exit with 'deactivate'"
    echo "============================================================================="

fi

# Deactivate after done
deactivate
