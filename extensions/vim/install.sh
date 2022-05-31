[ -e ~/.vim/syntax/jspec.vim ] && rm ~/.vim/syntax/jspec.vim
[ -e ~/.vim/ftdetect/jspec.vim ] && rm ~/.vim/ftdetect/jspec.vim
mkdir -p  ~/.vim/syntax/ && cp ./syntax/* ~/.vim/syntax/
mkdir -p ~/.vim/ftdetect/ && cp ./ftdetect/* ~/.vim/ftdetect/