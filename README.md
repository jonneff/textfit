# textfit
Insight Data Engineering project.  Scale up a machine learning algorithm that predicts whether a comment will get voted up or down on Reddit.

Dependencies:

Need to install numpy, tdigest and afinn on ALL NODES as follows:

sudo apt-get update
sudo apt-get install python-pip
sudo pip install cython
sudo pip install tdigest
sudo apt-get install git
git config --global user.name "Your Name"
git config --global user.email "youremail@domain.com"
git clone https://github.com/fnielsen/afinn.git
sudo python /home/ubuntu/afinn/setup.py install
sudo ln -s /usr/local/lib/python2.7/dist-packages/afinn-0.1.dev0-py2.7.egg/afinn /usr/local/lib/python2.7/dist-packages/afinn
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose



