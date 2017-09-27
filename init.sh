sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf $PWD/etc/nginx.conf /etc/nginx/sites-enabled/ask.conf
sudo /etc/init.d/nginx restart
gunicorn -c etc/gunicorn.conf ask.wsgi
