## Behavior-Driven-Developement for testing SDN_Controller

##### This readme navigates you through installation and setup for using behave.


### Required Software:
* Virtualbox (https://www.virtualbox.org/)
* Vagrant (https://www.vagrantup.com)


### Installation:

To install behave and the testing environment follow th instructions below.

#### Installation via Vagrantfile

In order to install behave via Vagrantfile you need to clone the repository first.  

`git clone https://github.com/lsinfo3/BDD-mininet`  
 
The cloned folder now contains the necessary Vagrantfile.
To start the virtual machine type

`vagrant up --provider virtualbox`

When the startup is complete follow the instructions on the screen to log into the VM and start Virtualenv.

Now follow the configuration instructions below in order to setup the correct behave environment.



### Configuration
Now, before you can run the code, you need to set a few environment variables. Therefore you need to edit the config file and source it afterwards.  
Following variables need to be set:
* First: Set the Behave variables (prefix is BH_) 
  * **BH_LOG** -  with this variable you can set the loglevel of your choice. Default is "OUTPUT" which prints you the normal output of the used subsystems (Mininet or Openstack/Terraform), with "WARNING" you can suppress normal output.
  * **BH_OPENSTACK** - set this variable to "true" for testing an SDN-Controller (in this case ONOS) in an OpenStack environment. For testing with Mininet set it to "false".
  * **BH_CONTROLLER_TYPE** - here you can define which SDN-Controller you want to test. Default is "REMOTE", for the ONOS SDN-Controller you need to set this variable to "ONOS". This variable only affects tests run with Mininet.
  * **BH_CONTROLLER_IP_PORT** - here you define the IP and Port which your SDN-Controller is running on (e.g. 10.10.0.1:6633). You need to provide this information for Mininet tests only.  
* Second: Setting the OpenStack (Terraform and Openstack/Neutron-client) variables. (`BH_OPENSTACK = true`)
    * You will be prompted for username and password
    * **TF_VAR_** - variables need to be set accordingly to your OpenStack System (auth_path, project, domain_name and user_domain_name)
    * **OS_** - variables need to be set accordingly to your OpenStack System 
    * **_ENDPOINT_TYPE** - variables need to be set accordingly to your OpenStack System

### Running Behave:
Switch to the folder in which you placed your "*.feature" file and type "behave".  
For choosing the test to execute please edit the "*.feature" file.
In case you just want to execute tagged tests type `behave --tags=yourTag`
In case you just want to execute all tests except your tagged ones, type `behave --tags=-yourTag`

### Additional
The OpenStack tests work with an ONOS SDN-Controller running on a virtual machine within the OpenStack infrastructure. To access this controllers GUI you need to run the test and wait for Terraform output. The output provides you with the public IP of the controller ("controller_fip="). Use this IP to connect to the GUI (e.g.`http://"controller_fip":8181/onos/ui/index.html`).   
To access the controllers console use the above described IP and connect into the vm using ssh. ONOS is running on a docker container within this vm. Type `sudo docker attach onos` to gain access to the ONOS console.
Every OpenStack infrastructure will be deleted at the end of the currently running test. This is required to run multiple tests of different OpenStack infrastructures. In case this isn't necessary, you may comment line 149 in "environment.py" file. This will prevent Behave from destroying. You may want to use this in order to test the reachability between "h1" and "h2", "h3" and "h4" without deploying the same infrastructure over and over again.

### Troubleshooting:
It may happen that deploying the OpenStack infrastructure via Terraform causes errors the first time they are executed. If that happens please rerun the test once or even twice. In most cases the problem vanishes. If there are still problems with deploying the infrastructure please switch to the special Terraform subfolder with the topology causing the problems and try to run `terraform destroy`. After successfully destruction of the erroneous infrastructure switch back to the behave root folder and run the test again.  
In case an error like `Exception: Error creating interface pair (s1-eth1,s2-eth1): RTNETLINK answers: File existsts` occurs, type `mn -c` to clean up mininet.
