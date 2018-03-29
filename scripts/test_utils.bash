export examples_root=$(dirname $0)/../examples
export exporter_preprocessors='["nbconvert.preprocessors.clearoutput.ClearOutputPreprocessor"]'

log () {
    
    echo '##'
    echo '# '$1
    echo '##'
    
}