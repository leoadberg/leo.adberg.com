# TODO: Automatically install https://github.com/romkatv/powerlevel10k#installation
# TODO: fzf

alias scr="screen -aAxRS"
function dif() {
  git diff --color=always $@ | less -r
}
function difm() {
  dif $(git merge-base HEAD origin/master) $@
}

# iTerm2
alias notify='echo -e "\033]9;Done!\\a"'
alias focus='echo -e "\033]1337;StealFocus\\a"'
