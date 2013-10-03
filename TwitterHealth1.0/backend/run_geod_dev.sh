ps -ef | grep 'python.* geod.py.*' | grep -v grep | awk '{print $2}' | xargs kill
nohup python -OO geod.py dev.fount.in 3 2013 4 16 &