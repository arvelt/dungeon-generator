# 自分の現在のリポジトリのgh-pagesをdocsの配下にsubmoduleとして登録する
# git submodule add -b gh-pages `git remote -v|grep fetch|awk '{print$2}'` docs

#first time
sphinx-apidoc -F -o ./documents_source ./src
#sphinx-apidoc -f -o ./documents_source ./src
sphinx-build -a ./documents_source ./publish

#cp -rf publish/* docs/
