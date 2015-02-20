#first time
#sphinx-apidoc -F -o ./documents_source ./src
sphinx-apidoc -f -o ./documents_source ./src
sphinx-build -a ./documents_source ./publish
