tmux kill-session -t server

tmux new-session -d -s server

tmux send-keys 'sudo python3 src/main.py' C-m