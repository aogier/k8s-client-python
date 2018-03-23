#!/bin/bash

# must be invoked from kube-init.sh

kernel_name=$1
echo Using kernel: $kernel_name

examples_root=$(dirname $0)/../examples

for file in $examples_root/*.py; do
    if [ $(basename $file) == '__init__.py' ]; then
        continue
    fi

    filename=$examples_root/notebooks/$(basename ${file%.py}.ipynb)

    if [ ! -f $filename ]; then
        echo WARNING: example $file does not have a notebook
    fi
done

for file in $examples_root/notebooks/*.ipynb; do
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
