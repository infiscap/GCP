from projectInOrg import get_projects, display_directory
from typing import Dict, List, Union
import os

def main():
    org_id=input('Organization ID를 입력하세요 (ex - 541096552061)')
    print("project 검색 중 입니다.")
    hierarchy = get_projects("Organization", org_id)
    
    service_name=input('Disable할 service name을 입력하세요(ex - containerscanning.googleapis.com)')
    addr_dict = set_disable_services_in_project(hierarchy, service_name)


def set_disable_services_in_project(resource: Union[Dict[str, Union[str, List[str]]], None], service_name):
    address_dict = {}

    if resource is None:
        return

    #org or folder list
    for key in resource.keys(): 
        if isinstance(resource[key], list):
            # project list
            for idx in range(len(resource[key])):
                if isinstance(resource[key][idx], dict):
                    set_disable_services_in_project(resource[key][idx], service_name)
                else:
                    # project
                    try:
                        set_project_cmd = f"gcloud config set project {resource[key][idx]}"
                        service_disable_cmd = f"gcloud services disable {service_name} --force"

                        set_project = os.popen(set_project_cmd).read()
                        service_disable = os.popen(service_disable_cmd).read()
                        print(resource[key][idx])
                        print(service_disable)
                    except:
                        1

if __name__=="__main__":
    main()
