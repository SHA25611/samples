import wls_config as config

#Testing accessibility for configuration values

#print('Hello there, below values are from config file')

#print(config.template)

#print(config.wl_username)

#print(config.wl_password)

#-----------------------Succeeded--------------------------------------------

''' Replicating the steps to create a weblogic domain using WLST offline
    using the configuration information from the config file.
'''

#Step-1 - Choosing domain template

readTemplate(config.template)

print('>> Template successfully loaded')

#Step-2 - Set basic domain parameters

set('Name',config.domain_name)
location = '/Security/'+config.domain_name+'/User/weblogic'
cd(location)
#print('>> changed Mbean directory to :-' + location)

cmo.setName(config.wl_username)
cmo.setPassword(config.wl_password)

print('>> weblogic username and password configured')

#Step-3 Configure Nodemanager for admin server

cd('/NMProperties')
set('ListenAddress',config.nm_listen_Address)
set('ListenPort',config.nm_listen_port)
#---Home_locations
set('WebLogicHome',config.weblogic_home)
set('JavaHome',config.java_home)
set('SecureListener',config.SL)
#---set('NodeManagerHome',config.nodemanager_home)
#---nodemanger_options
setOption('NodeManagerType',config.nm_type)
setOption('NodeManagerHome',config.nodemanager_home)

#---
cd('/SecurityConfiguration/base_domain')
set('NodeManagerUsername',config.nm_username)
set('NodeManagerPasswordEncrypted',config.nm_password)

print('>> Nodemanager configuration succeded')

#Step-4 Configure physical machines

m_d = config.machine_matrix  # m_d is a machine dictionary
for key in m_d:
    cd('/')
    create(str(key),'Machine')
    #path = '/Machine/' + str(key)
    #cd(path)
    #set('Address',m_d[key][0])

print('>> Machines configuration succeded ')

#Step-5 Configure clusters

c_d = config.cluster_matrix  # m_d is a machine dictionary
for key in c_d:
    cd('/')
    create(str(key),'Cluster')
    path = '/Cluster/' + str(key)
    cd(path)
    set('ClusterAddress',c_d[key][0])

print('>> Cluster configuration succeded')

#Step-6 Configure Admin server

cd('/')
cd('Server/AdminServer')
set('Name', config.admin_name)
set('ListenAddress', config.listen_Address)
set('ListenPort', config.listen_port)
#cd('/Server/AdminServer')
#set('Machine',config.adm_machine)

if(config.create_SSL == True):

    create('AdminServer','SSL')
    cd('SSL/AdminServer')
    set('Enabled', config.SSL_enabled)
    set('ListenPort', config.SSL_port)

print('>> Adminserver configuration succeded')

#Step-7 Configure managed servers

msm = config.mng_server_matrix

for key in msm:
    cd('/')
    create(str(key),'Server')
    path = '/Servers/' + str(key)
    cd(path)
    set('ListenAddress',msm[key][0])
    set('ListenPort',msm[key][1])
    set('Machine',msm[key][2])
    set('Cluster',msm[key][3])

print('>> Managed server configuration succeded')

#Step-8 Finish writing domain

cd('/')
setOption('OverwriteDomain',config.overwrite_domain)
setOption('ServerStartMode',config.server_startmode)

writeDomain(config.domain_home)

print('>> Closing template')
closeTemplate()

#Step-9 Starting admin server with all the needed parameters

admin_server_name = config.admin_name
domain_name = config.domain_name
mgmt_url = "t3://"+str(config.listen_Address)+":"+str(config.listen_port)
usr_nm = config.wl_username
pwd = config.wl_password
dmn_home = config.domain_home
blk_trm = "true"
tm_out = 60000
admin_log = "/wlsadm/ORACLE_HOME/user_projects/domains/"+domain_name+"/servers/"+admin_server_name+"/logs/"+admin_server_name+".log"

print(">> Starting admin server")
print(">> Logging startup information to :" + admin_log)

startServer(admin_server_name,domain_name,mgmt_url,usr_nm,pwd,dmn_home,blk_trm,tm_out,serverLog=admin_log)

print(">> Admin server started successfully")
print(">> Connecting to admin server")

connect(usr_nm,pwd,mgmt_url)

print(">> Mapping machines to nodemanager")
print(">> Starting edit session")
edit()
startEdit()

for key in m_d:
    pth = "/Machines/"+key+"/NodeManager/"+key
    cd(pth)
    cmo.setListenAddress(m_d[key][0])
    cmo.setListenPort(m_d[key][1])
    cmo.setNMType(m_d[key][2])

activate()

# Shutting down admin server
print(">> Configuration complete, shutting down admin server") 
shutdown(admin_server_name) 

print("Domain succesfully created...")
print('>> Exiting WLST..')
exit()



