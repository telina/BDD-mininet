## Behavior-Driven-Developement with Mininet 

#### This readme navigates you through installation and setup for using behave.


### Required Software:
* Virtualbox (https://www.virtualbox.org/)
* Vagrant (https://www.vagrantup.com)


### Installation:

First of all, use Vagrant to start an Ubuntu/vivid64 VM.

`agrant init ubuntu/vivid64`

`vagrant up --provider virtualbox`

`vagrant ssh`


If you being asked for credentials when starting the vm use vagrant/vagrant.

Now you should be on the Ubuntu shell. Type:

`sudo -s`

this makes the next steps more convenient.

`apt-get update`

`apt-get -y install git`


Next you need to get Mininet. This codes requires at least version 2.2.1 of Mininet.

`git clone https://github.com/mininet/mininet /home/vagrant/mininet`

`cd /home/vagrant/mininet`

`git checkout -b 2.2.1 2.2.1`

`cd /home/vagrant`

`mininet/util/install.sh -nfv`

This is the native installation you can find on the [Mininet website](http://mininet.org/download/ "Mininet installation"). 
If you want to know more about the install.sh options, check the website.


Next step is the installation of [pip](https://pypi.python.org/pypi/pip) and [virtualenv](https://virtualenv.pypa.io/en/latest/)

`apt-get install -y python-pip`

`pip install virtualenv`


Now you need to get the code:

`git clone https://github.com/lsinfo3/BDD-mininet /home/vagrant/BDD-mininet`

`cd /home/vagrant/BDD-mininet`


Setup and start a virtual environment named "venv":

`virtualenv /home/vagrant/BDD-mininet/venv`

`source /home/vagrant/BDD-vagrant/venv/bin/activate`


Last step is the installation of the required software with the requirements.txt file that comes with the code:

`sudo pip install -r requirements.txt`

After executing this command you should see following output:

"Successfully installed behave enum34 parse parse-type PyHamcrest requests" 


### Environment Variables
Now, before you start the code, you need to set a few environment variables as follows:
* "ONOS_CONTROLLER" -> In case you are using the Onos Controller you need to set this variable. (e.g `export ONOS_CONTROLLER=192.168.0.1:6632`) The default port ist 6633.
* "REMOTE_CONTROLLER"  -> To use a controller of your choice set the "RemoteController"-variable to an IP and PORT (e.g. `export REMOTE_CONTROLLER=192.168.0.1:6631`) The default Port is 6633.
* "DEFAULT_CONTROLLER" -> If you want to test a small scenario which only needs simple forwarding behavior, you can set this variable to true. (e.g. `export DEFAULT_CONTROLLER=True`) This enables the OVSController.
* In case you have a controller running on localhost with standard port=6633, just ignore all of the variables.

### Running Behave:
Switch to the folder in which you placed your "*.feature" file and type "behave".
In case you just want to execute tagged tests type `behave --tags=yourTag`
In case you just want to execute alls test except your tagged ones, type `behave --tags=-yourTag`
Tags:
@unstable -> flapping behavior with Onos in ractive mode
@OVS      -> works with OVS (DEFAULT_CONTROLLER=True) (no STP needed)

# Additional

The reactive mode of the onos controller led to a flapping of the test scenarios. This behavior forced us to only use the proactive mode of this controller. This means, everytime before a scenario is about to be executed, an intent (host-to-host-intent) is installed to allow host h1 to communicate with host h2.


### Troubleshooting:
In case an error like "Exception: Error creating interface pair (s1-eth1,s2-eth1): RTNETLINK answers: File exists" occurs, type `mn -c` to clean up mininet. 




