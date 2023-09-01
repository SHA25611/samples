"""This file contains minimum of neccessary configuration parameters to build a weblogic domain.
   This file can be further extended by increasing the list and corresponding changes in the create_domain.py
   script.
"""

# Basic domain parameters

template = "/wlsadm/ORACLE_HOME/wlserver/common/templates/wls/wls.jar"
domain_name = "wl_domain_3"
wl_username = "weblogic3"
wl_password = "weblogic5678999"  #update as per policy


# Nodemanager parameters for administration server machine

nm_listen_Address = '10.190.0.3'
nm_listen_port = 5811
SL = "false"
nm_username = "nm_weblogic345"
nm_password = "nm_weblogic5678345"
nm_type = "PerDomainNodeManager"
nodemanager_home = ""  # to provide null values use empty string instead of 'None' 

# Other Home location parameters

weblogic_home = "/wlsadm/ORACLE_HOME"
java_home = "/wlsadm/java/jdk1.8.0_301"


# Physical Machine parameters
# Format :: machine_matrix = {'machine_name':['nm_listen_address','nm_listen_port','nm_type'],...}

machine_matrix = {'wl_machine_1': ['10.190.0.3',5811,'Plain'], 'wl_machine_2': ['10.190.0.4',5812,'Plain'], 'wl_machine_3': ['10.190.0.5',5813,'Plain'] }



# cluster parameters

#cluster_name = "vf_auto_cls"
#cluster_address = "172.31.22.122"  # ip adrress of admin machine
#--cluster_machine_lst = ["vf_auto_01","vf_auto_02","vf_auto_03","vf_auto_04"]

cluster_matrix = {'wl_it_cls3': ['10.190.0.3'] }

# Admin server parameters

admin_name = "wl_admin_server_3"
listen_Address = "10.190.0.3" # ip address of admin machine
listen_port = 7006 # or port of your choice, but it should not be already in use
create_SSL = True # or False
SSL_enabled = True
SSL_port = 7007
adm_machine = 'wl_machine_1'


# Managed server parameters, using python lists here
# Format :: mng_server_matrix = {'mng_serv_name':['Listen_Address',Listen_port,machine,cluster],....}

mng_server_matrix = { 'wl_it_01': ['10.190.0.4',8003,'wl_machine_2','wl_it_cls3'], 'wl_it_02': ['10.190.0.5',8004,'wl_machine_3','wl_it_cls3'], 'wl_it_03': ['10.190.0.4',8005,'wl_machine_2','wl_it_cls3'], 'wl_it_04': ['10.190.0.5',8006,'wl_machine_3','wl_it_cls3'] }


# Finishing parameters

overwrite_domain = 'True'
server_startmode = 'prod'   # dev/prod/secure
domain_home = r"/wlsadm/ORACLE_HOME/user_projects/domains/wl_domain_3"



