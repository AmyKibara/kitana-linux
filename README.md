# Kitana - linux
Contains files created on ubuntu 24.04 USB

## Saving to github
cd ros2_ws
git init
git add .

Create gitignore and add the build/, install/ and log/ folders

git config --global user.email "amy.kibara@gmail.com"
git config --global user.name "AmyKibara"
git commit -m "Initial commit"

Create repo on github, link remote and push
git remote add origin https://github.com/AmyKibara/kitana-linux.git
git branch -M main
git push -u origin main

