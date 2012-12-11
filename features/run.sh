#!/bin/bash

START="2012-11-17"
END="2012-12-9"

python health.py airport_toy health_toy.pickle 0.8 $START $END
python meetings.py airport_toy meetings_toy.pickle 0.1 1 $START $END

#python generate_DBN_obs.py health_toy_pickle meetings_toy.pickle