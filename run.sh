sudo tmux has-session -t server

if [ $? == 0 ]; then
    sudo tmux kill-session -t server
fi
sudo tmux new-session -d -s server

sudo tmux send-keys "python3 src/main.py $branch" C-m