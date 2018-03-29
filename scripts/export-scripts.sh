#!/bin/bash

if ! which jupyter > /dev/null 2>&1; then
  echo Jupyter is not installed.
  exit
fi

. $(dirname $0)/test_utils.bash

# FIXME: it's super lame and I feel dumber every time I read it
if ! diff -urN \
    -x '*.pyc' \
    -x '*.pyd' \
    -x '*.pyo' \
    -x __pycache__ \
    $examples_root/example_utils \
    $examples_root/notebooks/example_utils >/dev/null 2>&1; then     
    log 'Warning: example support packages differs from notebooks/'
fi

for file in $examples_root/notebooks/*.ipynb; do
    
    # cleanup notebook
    jupyter nbconvert \
        --to notebook \
        --inplace \
        --NotebookExporter.preprocessors=$exporter_preprocessors \
        "$file"
    
    # convert to plain scripts
    jupyter nbconvert \
        --to python \
        --PythonExporter.exclude_input_prompt=True \
        --output-dir=$examples_root \
        "$file"
        
        # wait for https://github.com/pallets/jinja/pull/829
        # --PythonExporter.template_file=$examples_root/notebooks/.templates/python.tpl \

done

echo repository status after scrub/export: 
git status $examples_root --porcelain