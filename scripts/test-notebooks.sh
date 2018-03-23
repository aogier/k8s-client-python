#!/bin/bash

# must be invoked from kube-init.sh

kernel_name=$1
echo Using kernel: $kernel_name

for file in $(dirname $0)/../examples/notebooks/*.ipynb; do
    echo Testing notebook: $file
    jupyter nbconvert \
        --to notebook \
        --execute \
        --ExecutePreprocessor.timeout=60 \
        --ExecutePreprocessor.kernel_name=$kernel_name \
        --stdout $file > /dev/null

    if [ $? != 0 ]; then
        echo $file FAILED
        err=1
    fi

done

exit $err
