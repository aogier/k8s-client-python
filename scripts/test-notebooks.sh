#!/bin/bash

# must be invoked from kube-init.sh

kernel_name=$1
echo Using kernel: $kernel_name

. $(dirname $0)/test_utils.bash

for file in $examples_root/*.py; do
    if [ $(basename $file) == '__init__.py' ]; then
        continue
    fi

    filename=$examples_root/notebooks/$(basename ${file%.py}.ipynb)

    if [ ! -f $filename ]; then
        log "WARNING: example '$file' does not have a notebook"
    fi
done

nb_testfile=$(mktemp)
py_testfile=$(mktemp)
for file in $examples_root/notebooks/*.ipynb; do
    log "Testing notebook: '$file'"

    jupyter nbconvert \
        --to notebook \
        --output-dir=$(dirname "$nb_testfile") \
        --output=$(basename "$nb_testfile") \
        --log-level=0 \
        --execute \
        --ExecutePreprocessor.timeout=60 \
        --ExecutePreprocessor.kernel_name=$kernel_name \
        --NotebookExporter.preprocessors=$exporter_preprocessors \
        "$file" > /dev/null

    if [ $? != 0 ]; then
        log "Notebook '$file' FAILED"
        err=1
    fi

    # XXX: print diff ?
    if ! diff "$file" "${nb_testfile}.ipynb" > /dev/null; then
        log "WARNING: example $file seems dirty (saved cell output?)"
    fi

    py_realfile="$examples_root/$(basename ${file%.ipynb}.py)"
    if [ ! -f "$py_realfile" ]; then
        log "WARNING: notebook '$file' is not exported in examples (searched '$py_realfile')"
    fi

    # convert to plain scripts
    jupyter nbconvert \
        --to python \
        --PythonExporter.exclude_input_prompt=True \
        --output-dir=$(dirname "$py_testfile") \
        --output=$(basename "$py_testfile") \
        --log-level=0 \
        "$file"

    # XXX: print diff ?
    if ! diff "$py_realfile" "${py_testfile}.py" > /dev/null; then
        log "WARNING: generated example $py_realfile differs (local modifications?)"
    fi

done

exit $err
