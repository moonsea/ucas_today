#!/bin/bash
#deploy project
bundle install
rake db:migrate
rake db:seed
while(true)
do
    python Getnews.py
    sleep 1d
done
