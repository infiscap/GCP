import os
from getProjects import get_projs_in_org, get_projs

ENABLE="1"
EMPTY=1

def main():
    projects, num = get_projs()
    if len(projects)==0:
        print("project가 존재하지 않습니다. 다시 확인하세요")
        return
        
    num = num + 1
    service_name = input(f"{num}. service name을 입력하세요(ex - containerscanning.googleapis.com)")
    num = num + 1
    en_disable = input(f"{num}. 다음을 선택하시오(1. enable, 2. disable)")

    setable = "disable"

    if en_disable == ENABLE:
        setable = "enable"
    
    for proj in projects:
        try:
            set_project_cmd = f"gcloud config set project {proj}"
            service_disable_cmd = f"gcloud services {setable} {service_name}"
            if setable=="disable":
                service_disable_cmd = service_disable_cmd + " --force"

            set_project = os.popen(set_project_cmd).read()
            service_disable = os.popen(service_disable_cmd).read()
            print(proj)
            print(service_disable)
        except:
            EMPTY

if __name__=="__main__":
    main()
