sudo yum install -y python35-pip python35-devel libxml2-devel libxslt-devel 
sudo yum install gcc
sudo python35 -m pip install pip pyyaml ipython jupyter pandas boto beautifulsoup4 -U

export PYSPARK_DRIVER_PYTHON='which jupyter'
export PYSPARK_DRIVER_PYTHON_OPTS="notebook --NotebookApp.open_browser=False --NotebookApp.ip='*' --NotebookApp.port=8888"