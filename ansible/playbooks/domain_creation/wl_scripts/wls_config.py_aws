"""This file contains minimum of neccessary configuration parameters to build a weblogic domain.
   This file can be further extended by increasing the list and corresponding changes in the create_domain.py
   script.
"""

# Basic domain parameters

template = "/wlsadm/ORACLE_HOME/wlserver/common/templates/wls/wls.jar"
domain_name = "vodafone_italy_new"
wl_username = "weblogic"
wl_password = "weblogic5678"  #update as per policy


# Nodemanager parameters

nm_listen_Address = "localhost"
nm_listen_port = "5556"
nm_username = "nm_weblogic"
nm_password = "nm_weblogic5678"
nm_type = "CustomLocationNodeManager"
nodemanager_home = "/wlsadm/ORACLE_HOME/user_projects/domains/vodafone_italy_new/nodemanager"

# Other Home location parameters

weblogic_home = "/wlsadm/ORACLE_HOME"
java_home = "/wlsadm/java/jdk1.8.0_301"


# Physical Machine parameters
# Format :: machine_matrix = {'machine_name':['machine_address'],...}

machine_matrix = {'target-host-10': ['172.31.48.123'], 'target-host-06': ['172.31.60.206'], 'target-host-07': ['172.31.63.227'] }



# cluster parameters

#cluster_name = "vf_auto_cls"
#cluster_address = "172.31.22.122"  # ip adrress of admin machine
#--cluster_machine_lst = ["vf_auto_01","vf_auto_02","vf_auto_03","vf_auto_04"]

cluster_matrix = {'vf_it_cls1': ['172.31.48.123'] }

# Admin server parameters

listen_Address = "172.31.48.123" # ip address of admin machine
listen_port = 8009 # or port of your choice, but it should not be already in use
create_SSL = True # or False
SSL_enabled = True
SSL_port = 8010
adm_machine = 'target-host-10'


# Managed server parameters, using python lists here
# Format :: mng_server_matrix = {'mng_serv_name':['Listen_Address',Listen_port,machine,cluster],....}

mng_server_matrix = { 'vf_it_01': ['172.31.60.206',8011,'target-host-06','vf_it_cls1'], 'vf_it_02': ['172.31.63.227',8012,'target-host-07','vf_it_cls1'], 'vf_it_03': ['172.31.60.206',8013,'target-host-06','vf_it_cls1'], 'vf_it_04': ['172.31.63.227',7014,'target-host-07','vf_it_cls1'] }


# Finishing parameters

overwrite_domain = 'True'
server_startmode = 'dev'   # dev/prod/secure
domain_home = "/wlsadm/ORACLE_HOME/user_projects/domains/vodafone_italy_new"



