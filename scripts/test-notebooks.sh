#!/bin/bash

# must be invoked from kube-init.sh

for file in $(dirname $0)/../examples/notebooks/*.ipynb; do
    echo Testing notebook: $file
    jupyter nbconvert \
        --to notebook \
        --execute \
        --ExecutePreprocessor.timeout=60 \
        --stdout $file > /dev/null

    # accumulate errors
    (( err = err || $? ))
done

exit $err