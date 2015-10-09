# textfitXL by Jon Neff

Insight Data Engineering project.  Scale up a machine learning algorithm that predicts whether a comment will get voted up or down on Reddit.

1.  Spin up 8 m4.xlarge instances on AWS.  Use very open security settings for easier configuration (and less security :).  If you only plan to work with a subset of the Reddit comment corpus, a smaller number of nodes may be sufficient.  The 2007/RC_2007-10 input file (85 MB) can be processed on a laptop with 1.4 GHz processor and 4 GB memory. 

2.  Install and configure Spark 1.4.1 on all nodes.  

3.  Install dependencies:

	Need to install dependencies on ALL NODES as follows:

	sudo apt-get update

	sudo apt-get install git

	git config --global user.name "Your Name"

	git config --global user.email "youremail@domain.com"

	git clone https://github.com/fnielsen/afinn.git

	sudo python /home/ubuntu/afinn/setup.py install

	sudo ln -s /usr/local/lib/python2.7/dist-packages/afinn-0.1.dev0-py2.7.egg/afinn /usr/local/lib/python2.7/dist-packages/afinn

	sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose

4.  Git clone this repository on to master node:  git clone https://github.com/jonneff/textfit.git

5.  Start Ipython notebook with Spark in the textfit directory.  For a cluster, use 

	IPYTHON_OPTS="notebook" pyspark --master spark://<private ip>:7077 --executor-memory 6400M --driver-memory 6400M

	<private ip> is the private IP address of your Spark master node.  Set executor-memory and driver-memory to about 75-80% of available memory on nodes.  

	For single node installation using a small dataset you can use

	IPYTHON_OPTS="notebook" pyspark

6.  If you are using a remote server you may need to set up port forwarding to see the Ipython notebook.  Use something like

	ssh -i ~/.ssh/<your pem key file> -N -f -L localhost:7778:localhost:8888 ubuntu@master

	where "master" is the public DNS for the master node.  

	Then you can connect to the textfitXL Ipython notebook by pointing your browser at http://localhost:7778.  In the browser window, click on logistic_regression.ipynb to start the textfitXL notebook.  

7.  Download the Reddit comment corpus or a subset thereof using the instructions here:  

	https://archive.org/details/2015_reddit_comments_corpus.  

	Modify the following statement in cell 2 of the Ipython notebook to point to the Reddit JSON file or files you wish to read:  

	df = hiveContext.read.json("s3n://reddit-comments/*", StructType(fields))

8.  You should now be able to run the Ipython notebook on the input dataset.  This notebook is intended to be an interactive tool for data scientists to use in exploring the Reddit corpus and fitting different models.  Individual cells must be executed in order for the code to work properly.  

