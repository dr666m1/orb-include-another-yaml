if [[ -z $PARAM_OUT ]]; then
  yamlbundler -i $PARAM_FILEPATH
else
  yamlbundler $PARAM_FILEPATH -o $PARAM_OUT
fi
