sudo apt-get install libxslt1-dev gdal-bin

~/venv/bin/pip install tilestache uwsgi Pillow==2.9.0

sudo cp tilestache.nginx /etc/nginx/sites-available/tilestache
sudo ln -sf /etc/nginx/sites-available/tilestache /etc/nginx/sites-enabled/tilestache
sudo service nginx restart

sudo cp tilestache.upstart /etc/init/tilestache.conf
ln -s /usr/lib/pymodules/python2.7/mapnik ~/venv/lib/python2.7/site-packages/mapnik
ln -s /usr/lib/python2.7/dist-packages/lxml ~/venv/lib/python2.7/site-packages/lxml

# get the shapefile
# sudo service tilestache start