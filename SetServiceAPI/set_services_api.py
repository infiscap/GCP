from projectInOrg import get_projects, get_projects_to_json
import os
ALL_PROJECTS="1"
SOME_PROJECTS="2"
DIRECT_PROJECT_NAME="1"
KEYWORD_PROJECT_NAME="2"
ENABLE="1"
EMPTY=1

def get_projs_in_org(num):
    org_id=input(f'{num}. Organization ID를 입력하세요 (ex - 541096552061)')
    print("project 검색 중 입니다.")
    hierarchy = get_projects("Organization", org_id)
    return get_projects_to_json(hierarchy)

def get_projs():
    projects=[]
    num=1
    choice = input(f"{num}. 모든 프로젝트를 확인하시겠습니까?(1. yes/2. no) 1 또는 2를 입력하세요")
    if choice==ALL_PROJECTS:
        num = num + 1
        projects = get_projs_in_org(num)
    elif choice==SOME_PROJECTS:
        num = num + 1
        choice = input(f"{num}. 프로젝트를 직접 입력하시겠습니까?(1. yes/2. no) 1 또는 2를 입력하세요")
        if choice==DIRECT_PROJECT_NAME:
            num = num + 1
            projects=input(f"{num}. 프로젝트를 띄어쓰기(' ')로 이용해 입력하세요?ex(aaa bbb)")
            # projects = projects.replace(" ", "")
            projects=projects.split(" ")
        elif choice==KEYWORD_PROJECT_NAME:
            num = num + 1
            tmp_projs = get_projs_in_org(num)
            num = num + 1
            keyword = input(f"{num}. 검색할 키워드를 입력해 주세요?ex (prod)")
            for proj in tmp_projs:
                if proj.find(keyword) != -1:
                    projects.append(proj)

    return projects, num

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
