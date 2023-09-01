import wls_config as config
import os 

usr_nm = config.wl_username
pswd = config.wl_password
adm_srv_name = config.admin_name
dmn_hme = config.domain_home

boot_file_path = str(dmn_hme) + r"/servers/"+str(adm_srv_name)+r"/security/boot.properties"

boot_file = open(boot_file_path,"w+")

line1 = "username="+usr_nm
line2 = "password="+pswd

boot_file.write(line1 +"\n")
boot_file.write(line2+"\n")

boot_file.close()

print("Boot identity successfully created..")
