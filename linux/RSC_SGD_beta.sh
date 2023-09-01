#!/bin/bash
#Script purpose : To remotely clean the file system of the provided server in the datacenter
#Author : Anand Shammi, Vodafone Group (shammi.anand@vodafone.com) 

echo " "
   echo "---------------------------------------------------------------------"
   echo "| You are using Remote System Cleaner script, Please note the below:|"
   echo "| 1. This script is compatible with SGD, clients using puTTy follow |"
   echo "|    the below:-                                                    |"
   echo "|   1.1 Please connect an SGD session to soltau2 and run id.sh on it|"
   echo "|       keep the session on standby mode then connect to soltau2    |"
   echo "|       using the puTTy application, then run your copy of RSC puTTY|" 
   echo "|       version on the puTTy application itself.                    |"
   echo "| 2. Please provide the inputs to the script in recommended format, |"
   echo "|    otherwise it may cause unwanted loss of files from the server. |"
   echo "| 3. Please try to run the script to completion in one go or in case|"
   echo "|    if the script is terminated in middle due to any reason, please|"
   echo "|    run the auxilary script GCS, in the same folder containing the |"
   echo "|    RSC script, GCS comes along with RSC in one pack.              |"
   echo "---------------------------------------------------------------------"
echo " "


echo "Please provide the name of the remote server :"
raw_srv_list=()
srv_count=0
#while read i; 
# do
#   if [[ -z "$i" ]]; 
#    then
#     break
#   fi
#   raw_srv_list+=("$i")
# done
read srvr_name
raw_srv_list=("$srvr_name")
ifs=" " read -ra srv_list <<< "${raw_srv_list[@]}"
echo "Processing, please wait ...                   "
count=0
mkdir env
cd env
for item in "${srv_list[@]}"; 
do
ssh $item > /dev/null 2>&1 << EOMF > ./cache 
   echo " "
   echo "                        @@@@@@@++++++@@@@@@@                          "
   echo "----------------------------------------------------------------------"
   echo "-  List of partitions more than 70 percent full                      -"
   echo "----------------------------------------------------------------------"
   echo "  No.           Utilized             Mount point                      "
   echo "-------      -------------          ----------------------------------"
   df -h | awk ' { print  \$(NF-1) "       " \$NF }' | awk '\$1~/^([7-9][0-9]|[1][0][0])[%]$/' | awk '{ print "  " NR-1 "               " \$(NF-1) "                "\$NF }'
   echo "----------------------------------------------------------------------"
   echo "- Please choose one Number (No.) or Path (Mount point)        "
EOMF

sim=0
while IFS= read -r l || [ -n "$l" ]
do
 if [[ "$sim" == 1 ]]
  then 
   echo "$l" >> ./cache_
 fi

 if [[ "$l" == "                        @@@@@@@++++++@@@@@@@                          " ]]
  then
    sim=1
 fi

done < ./cache
cat cache
#echo $item

export intro="cache"
intr_size=$(wc -l < "$intro")
#echo "$intr_size"
if [[ $intr_size -eq 0 ]]
then
 echo " "
 echo " "
 echo "Error : one of the following happened"
 echo "1. hostname is unknown or not reachable"
 echo "2. All the filesystems are below 70% occupied"
 echo " "
 cd ..
 rm -rf env
 break
fi
fs_arr=( $(cat cache_ | grep % | awk '{ print $NF }') )
#rm cache_  # removing the separated data to avoid appending for different servers
#echo "${#fs_arr[@]}"
#echo "${fs_arr[@]}"
#echo "${fs_arr[0]}"
#echo "${fs_arr[1]}"
#echo "${fs_arr[2]}"
#echo "${fs_arr[3]}"
#echo "${fs_arr[4]}"



echo " "

mnt_pnt=" "
choice=0
while :
 do
  read choice

  if [[ "$choice" == "Q" || "$choice" == "q" ]]
  then
   rm ./cache_
   cd ..
   rm -rf env
   break
  fi  

  
  count_=0
  for elm in "${fs_arr[@]}";
  do
    if [[ "$choice" == "$count_" || "$choice" == "$elm" ]]
    then
      echo "your choice : $count_  -  $elm "
      mnt_pnt="$elm"
      break
    else
      ((count_++))
    fi
  done
  #echo "${#fs_arr[@]}" 
  if [[ $count_ -gt ${#fs_arr[@]}-1 ]]
  then
   echo "-INVALID CHOICE, Please select again or terminate the script by pressing ctrl + z- "
   echo "ENTER YOUR CHOICE: "
   continue  

  fi 
  
ssh $item > /dev/null 2>&1 << EOFT > ./tr_cache
  echo " "
  echo " this line is the separator for the directory tree of the partition "
  echo " "
  cd "${fs_arr[count_]}"
  pwd
  echo " "
  ls -lRtr 

EOFT
 echo "    "
 echo "Analyzing partition...  "
 echo "    "
 flag_=0
 while IFS= read -r p || [ -n "$p" ]
 do
  if [[ "$flag_" == 1 ]]
   then
    echo $p >> fcache
  fi

  if [[ "$p" == " this line is the separator for the directory tree of the partition " ]]
   then 
    flag_=1
  fi
 done < tr_cache

 cat fcache | awk '$1~/.*:/' > ./dir_lst

 while IFS= read -r ln || [ -n "$ln" ]
  do
   echo "${ln%?}" >> ./f_dir_lst
  done < dir_lst
 
 cp fcache f_cache
 rm tr_cache
 rm fcache   #removing intermidiate residual files.
 rm dir_lst

# now breaking the f_dir_lst file into multiple files if required (****obsolete idea****)

export lst="f_dir_lst"
length=$(wc -l < "$lst")
#echo $length

# At this point we are building a presentable model of the directory tree of the partition

echo " "
echo "Building partition model,"
echo "this may take several minutes if the partition is too big. "
echo " "

partition_name=$(echo "$mnt_pnt" | sed  's/[/]/%/g')
echo "$partition_name" > ./temp_partition_var
mkdir $partition_name
cd $partition_name

dir_pth=" "
flg=0
cnt_=0
stage=0
pattern='^\.(\/[[:alnum:]]*|.|_)*:$'

(
 echo "10" ; sleep 1
 while IFS= read -r lne || [ -n "$lne" ]
  do
   if [[ "$flg" == 1 && -n "$lne" ]]
    then
     echo "$lne" >> ../$partition_name/$dir_pth/content 
   else
    if [[ -z "$lne" ]]
     then
      flg=0
    fi
   fi

   if [[ "$lne" =~ $pattern ]]
    then
     dir_pth=$(echo "$lne" | sed 's/[/.:]/%/g')
     mkdir $dir_pth
     cur_pth_=$(pwd)
     echo  "$cnt_" "          " "${lne%?}" "                                      " "$cur_pth_""/""$dir_pth""/content" >> ../map  
     flg=1
     ((cnt_++))
   fi
  
   if [[ $cnt_ -gt 100 && $cnt_ -lt 500 && "$stage" == "0" ]]
    then
     stage=1
     echo "14" ; sleep 1
   fi

   if [[ $cnt_ -gt 500 && $cnt_ -lt 1000 && "$stage" == "1" ]]
    then
     stage=2
     echo "18" ; sleep 1
   fi

   if [[ $cnt_ -gt 1000 && $cnt_ -lt 1500 && "$stage" == "2" ]]
    then
     stage=3
     echo "22" ; sleep 1
   fi

   if [[ $cnt_ -gt 1500 && $cnt_ -lt 2000 && "$stage" == "3" ]]
    then
     stage=4
     echo "26" ; sleep 1
   fi

   if [[ $cnt_ -gt 2000 && $cnt_ -lt 2500 && "$stage" == "4" ]]
    then
     stage=5
     echo "30" ; sleep 1
   fi

   if [[ $cnt_ -gt 2500 && $cnt_ -lt 3000 && "$stage" == "5" ]]
    then
     stage=6
     echo "34" ; sleep 1
   fi

   if [[ $cnt_ -gt 3000 && $cnt_ -lt 3500 && "$stage" == "6" ]]
    then
     stage=7
     echo "38" ; sleep 1
   fi

   if [[ $cnt_ -gt 3500 && $cnt_ -lt 4000 && "$stage" == "7" ]]
    then
     stage=8
     echo "42" ; sleep 1
   fi

   if [[ $cnt_ -gt 4000 && $cnt_ -lt 4500 && "$stage" == "8" ]]
    then
     stage=9
     echo "46" ; sleep 1
   fi

   if [[ $cnt_ -gt 4500 && $cnt_ -lt 5000 && "$stage" == "9" ]]
    then
     stage=10
     echo "50" ; sleep 1
   fi

   if [[ $cnt_ -gt 5000 && $cnt_ -lt 5500 && "$stage" == "10" ]]
    then
     stage=11
     echo "54" ; sleep 1
   fi

   if [[ $cnt_ -gt 5500 && $cnt_ -lt 6000 && "$stage" == "11" ]]
    then
     stage=12
     echo "58" ; sleep 1
   fi


   if [[ $cnt_ -gt 6000 && $cnt_ -lt 6500 && "$stage" == "12" ]]
    then
     stage=13
     echo "62" ; sleep 1
   fi

   if [[ $cnt_ -gt 6500 && $cnt_ -lt 7000 && "$stage" == "13" ]]
    then
     stage=14
     echo "66" ; sleep 1
   fi

   if [[ $cnt_ -gt 7000 && $cnt_ -lt 7500 && "$stage" == "14" ]]
    then
     stage=15
     echo "70" ; sleep 1
   fi

   if [[ $cnt_ -gt 7500 && $cnt_ -lt 8000 && "$stage" == "15" ]]
    then
     stage=16
     echo "74" ; sleep 1
   fi

   if [[ $cnt_ -gt 8000 && $cnt_ -lt 8500 && "$stage" == "16" ]]
    then
     stage=17
     echo "78" ; sleep 1
   fi

   if [[ $cnt_ -gt 8500 && $cnt_ -lt 9000 && "$stage" == "17" ]]
    then
     stage=18
     echo "82" ; sleep 1
   fi

   if [[ $cnt_ -gt 9000 && $cnt_ -lt 9500 && "$stage" == "18" ]]
    then
     stage=19
     echo "86" ; sleep 1
   fi

   if [[ $cnt_ -gt 9500 && $cnt_ -lt 10000 && "$stage" == "19" ]]
    then
     stage=20
     echo "90" ; sleep 1
   fi

   if [[ $cnt_ -gt 10000 && $cnt_ -lt 10500 && "$stage" == "20" ]]
    then
     stage=21
     echo "94" ; sleep 1
   fi

   if [[ $cnt_ -gt 10500 && $cnt_ -lt 11000 && "$stage" == "21" ]]
    then
     stage=22
     echo "98" ; sleep 1
   fi

   if [[ $cnt_ -gt 11000 && $cnt_ -lt 11500 && "$stage" == "22" ]]
    then
     stage=23
     echo "98.5" ; sleep 1
   fi

   if [[ $cnt_ -gt 11500 && $cnt_ -lt 12000 && "$stage" == "23" ]]
    then
     stage=24
     echo "99" ; sleep 1
   fi

   if [[ $cnt_ -gt 12000 && $cnt_ -lt 12500 && "$stage" == "24" ]]
    then
     stage=25
     echo "99.5" ; sleep 1
   fi



  done < ../f_cache
  echo "100" ; sleep 2
) | zenity --progress --title="Building partition model" --percentage=0 --auto-close --text="Click Cancel to terminate the script"

#(( $?!=0 )) && zenity --error --text="Error in zenity command"

#echo "$?"
ret=$?
#echo "$ret"
if [[ "$ret" != "0" ]]
then 
 echo " "
 echo "You canceled the process,the script will be terminated"
 #echo "Please run the GCS to properly use this script further"
 echo " "
 cd ..
 cd ..
 rm -rf env
 exit 1
fi
#now the GUI toolkit comes into play, that will take inputs from the user 

echo "Please explore the partition manually and take option based decisions "
echo "Host_name""                                       ""File_System""                                        ""Directory_path""                                ""Option_chosen(1=zip__2=remove)""      ""Age""        ""Extension"      >> ../execution_plan
   
action=" "
link_pth=" "
while :
do
  if [[ "$action" == "N" ]]
   then
    break
  fi
  
  link_pth=$(zenity --file-selection)
  if [[ -z "$link_pth" ]]
   then 
    echo " you cancelled the file browser, do you want to exit ?(yes/no) "
    read inpt
    if [[ "$inpt" == "yes" ]]
     then
      break
    else
      continue
    fi
  else
    cat $link_pth
  fi
  echo " "
  echo " Would you consider cleaning this folder ?(yes/no)"
  read fact
  if [[ "$fact" == "yes" ]]
   then
    
    echo "----------------------------------------------------------------------"
    echo "-         Choose :           1.Zip           2.Remove                -"  
    echo "----------------------------------------------------------------------"

    
 
    read option
    if [[ "$option" == "1" || "$option" == "zip" ]]
     then 
      echo " Enter the age of files(in days) you want to zip "
      read age
      #echo " $age days old files will be zipped "
      echo " Enter the extension of the file which you want to zip (exactly in the following format *.trc, *.trm etc) "
      read extension
      locat=$(cat ../map | grep $link_pth | awk '{ print $2 }')
      
      echo "$item""                              ""$mnt_pnt""                                   ""$locat""                                                 ""$option""             ""$age""      ""$extension"    >> ../execution_plan    

    else
      if [[ "$option" == "2" || "$option" == "remove" ]] 
       then 
        echo " Enter the age of files(in days) you want to remove "
        read age
        #echo " $age days old files will be removed "
        echo " Enter the extension of the file which you want to remove (exactly in the following format *.trc, *.trm etc) "
        read extension
        locat=$(cat ../map | grep $link_pth | awk '{ print $2 }')
      
        echo "$item""                             ""$mnt_pnt""                                  ""$locat""                                                   ""$option""           ""$age""        ""$extension"   >> ../execution_plan 
      else
       echo " INVALID OPTION "
      fi
    fi
  fi 
  
  echo " Press N to stop exploring and proceed or hit enter to keep exploring"
  read action
  
done

cat ../execution_plan

echo " "
echo "Are you sure you want to proceed with the above execution plan?(yes/no)"
read fdecision_
if [[ "$fdecision_" == "yes" ]]                                                                 # if of the final execution block starts
then
# Now proceeding for actual cleaning of the file system on the remote server based on the execution plan generated.
remote_server="$item"
mount_point="$mnt_pnt"
dir_array=( $(cat ../execution_plan | awk '{ print $3 }') )
echo "${dir_array[@]}"
echo "${#dir_array[@]}"
option_array=( $(cat ../execution_plan | awk '{ print $4 }') )
echo "${option_array[@]}"
echo "${#option_array[@]}"
age_array=( $(cat ../execution_plan | awk '{ print $5 }') )
echo "${age_array[@]}"
echo "${#age_array[@]}"
ext_array=( $(cat ../execution_plan | awk '{ print $6 }') )
echo "${ext_array[@]}"
echo "${#ext_array[@]}"

end_="${#dir_array[@]}"

ssh $remote_server << EOFF
cd "$mount_point"
pwd

# take an infinite loop with a global and a local counter for logic implementation

global_comm_counter=0

directory_=" "
option_=" "
age_=" "
extension_=" "

while :
do
if [[ \$global_comm_counter -gt $end_-1 ]]
 then
   break
else
#-------------------------------------------------------------------------
for locs1 in "${dir_array[@]}";
 do
   local_comm_counter1=0
   for value_1 in \$locs1;
    do
     if [[ "\$local_comm_counter1" == "\$global_comm_counter" ]]
      then
       directory_="\$value_1"
       break
     else
       ((local_comm_counter1++))
       continue
     fi
     
    done  
 done
#-------------------------------------------------------------------------
for locs2 in "${option_array[@]}";
 do
   local_comm_counter2=0
   for value_2 in \$locs2;
    do
     if [[ "\$local_comm_counter2" == "\$global_comm_counter" ]]
      then
       option_="\$value_2"
       break
     else
       ((local_comm_counter2++))
       continue
     fi
     
    done  
 done
#--------------------------------------------------------------------------
for locs3 in "${age_array[@]}";
 do
   local_comm_counter3=0
   for value_3 in \$locs3;
    do
     if [[ "\$local_comm_counter3" == "\$global_comm_counter" ]]
      then
       age_="\$value_3"
       break
     else
       ((local_comm_counter3++))
       continue
     fi
     
    done  
 done
#-------------------------------------------------------------------------
for locs4 in "${ext_array[@]}";
 do
   local_comm_counter4=0
   for value_4 in \$locs4;
    do
     if [[ "\$local_comm_counter4" == "\$global_comm_counter" ]]
      then
       extension_="\$value_4"
       break
     else
       ((local_comm_counter4++))
       continue
     fi
     
    done  
 done

fi


if [[ "\$global_comm_counter" == "0" ]]
 then
  ((global_comm_counter++))
  continue
else
 echo "switching to \$directory_"
 cd \$directory_
 echo "inside \$(pwd)"
 if [[ "\$option_" == "1" ]]
  then 
   echo "Zipping files in progress..."
   find . \( -type d ! -name . -prune \) -o \( -type f -mtime "+\$age_" -name "\$extension_" \) -exec gzip {} \;
 else
  if [[ "\$option_" == "2" ]]
   then
    echo "removing files in progress..."
    find . \( -type d ! -name . -prune \) -o \( -type f -mtime "+\$age_" -name "\$extension_" \) -exec rm -rf {} \;
  else
    exit 1
  fi
 fi
 echo "switching back to $mount_point"
 cd "$mount_point"
 echo "back to \$(pwd)"
fi
#echo "\$directory_   \$option_   \$age_   \$extension_"

((global_comm_counter++))

done

EOFF
else                                                                                              #else of the final execution block
cd ..
#----------------------------------------------------------------------
rm map f_cache f_dir_lst execution_plan temp_partition_var cache_ cache
rm -rf $partition_name
#----------------------------------------------------------------------


echo " "
ssh $item > /dev/null 2>&1 << EOMFFFF > ./cache 
   echo " "
   echo "                        @@@@@@@++++++@@@@@@@                          "
   echo "----------------------------------------------------------------------"
   echo "-  List of partitions more than 70 percent full                      -"
   echo "----------------------------------------------------------------------"
   echo "  No.           Utilized             Mount point                      "
   echo "-------      -------------          ----------------------------------"
   df -h | awk ' { print  \$(NF-1) "       " \$NF }' | awk '\$1~/^([7-9][0-9]|[1][0][0])[%]$/' | awk '{ print "  " NR-1 "               " \$(NF-1) "                "\$NF }'
   echo "----------------------------------------------------------------------"
   echo "- Please choose one Number (No.) or Path (Mount point)        "
EOMFFFF

sim=0
while IFS= read -r l || [ -n "$l" ]
do
 if [[ "$sim" == 1 ]]
  then 
   echo "$l" >> ./cache_
 fi

 if [[ "$l" == "                        @@@@@@@++++++@@@@@@@                          " ]]
  then
    sim=1
 fi

done < ./cache

cat cache_
echo " "
 echo "press Q to exit or continue by entering your new choice "
 continue
fi                                                                                                #fi of the final execution block

cd ..
#----------------------------------------------------------------------
rm map f_cache f_dir_lst execution_plan temp_partition_var cache_ cache
rm -rf $partition_name
#----------------------------------------------------------------------


echo " "
ssh $item > /dev/null 2>&1 << EOMFFFFF > ./cache 
   echo " "
   echo "                        @@@@@@@++++++@@@@@@@                          "
   echo "----------------------------------------------------------------------"
   echo "-  List of partitions more than 70 percent full                      -"
   echo "----------------------------------------------------------------------"
   echo "  No.           Utilized             Mount point                      "
   echo "-------      -------------          ----------------------------------"
   df -h | awk ' { print  \$(NF-1) "       " \$NF }' | awk '\$1~/^([7-9][0-9]|[1][0][0])[%]$/' | awk '{ print "  " NR-1 "               " \$(NF-1) "                "\$NF }'
   echo "----------------------------------------------------------------------"
   echo "- Please choose one Number (No.) or Path (Mount point)        "
EOMFFFFF

sim=0
while IFS= read -r l || [ -n "$l" ]
do
 if [[ "$sim" == 1 ]]
  then 
   echo "$l" >> ./cache_
 fi

 if [[ "$l" == "                        @@@@@@@++++++@@@@@@@                          " ]]
  then
    sim=1
 fi

done < ./cache

cat cache_
echo " "
 echo "press Q to exit or continue by entering your new choice "
 
 done 
  




 
((count++))
done  2> /dev/null
