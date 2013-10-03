#!/bin/bash

# Boston
ssh sadilek@f01.cs.rochester.edu 'ssh node50 -o StrictHostKeyChecking=no '"'"'cd ~/code/TwitterHealth/backend && ./collect_health.sh 42.3644,-71.059,50km'"'"'' &

# LA
ssh sadilek@f01.cs.rochester.edu 'ssh node51 -o StrictHostKeyChecking=no '"'"'cd ~/code/TwitterHealth/backend && ./collect_health.sh 33.995,-118.063,100km'"'"'' &

# London
ssh sadilek@f01.cs.rochester.edu 'ssh node52 -o StrictHostKeyChecking=no '"'"'cd ~/code/TwitterHealth/backend && ./collect_health.sh 51.514,-0.122,100km'"'"'' &

# NYC
ssh sadilek@f01.cs.rochester.edu 'ssh node53 -o StrictHostKeyChecking=no '"'"'cd ~/code/TwitterHealth/backend && ./collect_health.sh 40.716667,-74.00,100km'"'"'' &

# Seattle
ssh sadilek@f01.cs.rochester.edu 'ssh node54 -o StrictHostKeyChecking=no '"'"'cd ~/code/TwitterHealth/backend && ./collect_health.sh 47.577,-122.229,100km'"'"'' &

# SF
ssh sadilek@f01.cs.rochester.edu 'ssh node55 -o StrictHostKeyChecking=no '"'"'cd ~/code/TwitterHealth/backend && ./collect_health.sh 37.566,-122.327,100km'"'"'' &

# Rochester
ssh sadilek@f01.cs.rochester.edu 'ssh node56 -o StrictHostKeyChecking=no '"'"'cd ~/code/TwitterHealth/backend && ./collect_health.sh 42.96,-79.09,170km'"'"'' &
