echo "change detected rebuilding" ${pwd}
cd /home/debian/monorepo
git pull
git reset --hard origin/main
# TODO: put build instructions here instead of in the yaml file
cd code
npm install
sudo systemctl restart chess_website.service
sudo systemctl daemon-reload
