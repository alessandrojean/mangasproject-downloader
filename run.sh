echo -ne "\033]0;${USER}@${HOSTNAME}: mangásPROJECT Downloader\007"
python -m mangasproject "$@"
