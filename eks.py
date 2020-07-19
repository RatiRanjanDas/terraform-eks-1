import os
import argparse
import time
import subprocess
import nginx_config
import sys
import yaml
#from python_terraform import *

#sys.path.insert(0,'./vc_scripts')
from DVC_Scaler import create_hostname_vm


#import setup

'''
os.system("terraform init")
time.sleep(30)
os.system("terraform plan")
time.sleep(20)
os.system("terraform apply")
time.sleep(700)
os.system("aws eks --region ap-south-1 update-kubeconfig --name terraform-eks-demo")
time.sleep(10)
os.system("kubectl create namespace service")
time.sleep(10)
os.system("kubectl create secret docker-registry regcred --docker-server=https://index.docker.io/v1/ --docker-username=nouveaulabs --docker-password=I@mgod456")
time.sleep(10)
os.system("git clone https://github.com/RatiRanjanDas/Nouveau-Service-YAML-files.git")
time.sleep(30)
'''
pwd = os.path.dirname(__file__)
print(pwd)
def create_eks(config_path, vpc, subnet):
    owd = os.getcwd()
    print(owd)
    os.chdir('./EKS_with_terraform_master')
    print(os.getcwd())
    #os.system("terraform destroy -auto-approve")
    #os.system("rm -rf terraform.*")
    os.system("terraform init")
    #os.system("terraform plan -var 'cluster_name=terraform-eks-demo' -out terraform-plan")
    os.system("terraform apply -auto-approve")
    #time.sleep(700)
    print("terraform applied successfully!!")
    os.system("aws eks --region ap-south-1 update-kubeconfig --name terraform-eks-demo") 
    time.sleep(10)
    print("kubeconfig updated!!")
    eks_cluster_name = config_path.get("ekscluster").get('cluster_name')
    eks_region = config_path.get("ekscluster").get('region')
    kub_nodes = subprocess.check_output(["kubectl", "get", "nodes", "-o", "wide"])
    kub_nodes_str = kub_nodes.decode("utf-8")
    #print("after decode:"+str(kub_nodes_str))
    kub_nodes_list=list(kub_nodes_str.split("\n"))
    node_list = []
    node_name = {}#dqdn and privateip
    for node_names in kub_nodes_list[1:-1]:
        node_name = {"fqdn": [x for x in node_names.split(' ') if x ][0], "ip_address": [x for x in node_names.split(' ') if x ][6]}
        node_list.append(node_name)
    print(node_list)
    os.system("kubectl create namespace service") 
    os.chdir(owd)
    print(os.getcwd())
    return eks_cluster_name, eks_region, node_list#list of eks nodes

def update_yamls():
    os.system("kubectl create secret docker-registry regcred --docker-server=https://index.docker.io/v1/ --docker-username=nouveaulabs --docker-password=I@mgod456")
    print("updating yamls")
    yaml_path = os.path.join(pwd, "k8s_yaml/")
    os.system('kubectl apply -f '+ yaml_path)
    return

def setup_ingress(list_of_eks_nodes):
    #add eks nodes in nginx upstream
    nginx_config.nginx_upstream_update(list_of_eks_nodes)
    #create the nginx vm
    nginx_hostname = create_hostname_vm.create('nginx')
    #terraform_path = os.path.join(pwd, "../terraform/terraform-create.sh")
    #result = subprocess.call([terraform_path, public_key_path, private_key_path, isPublic, aws_amis, hostname, subnet_id, isElastic, cpu_core_count, cpu_threads_per_core, volume_size, aws_creds, aws_region, instance_type, base_dir, isRoute53])
    #start nginx
    print("setup ingress done")
    return nginx_hostname
#create_eks('','','')
update_yamls()
