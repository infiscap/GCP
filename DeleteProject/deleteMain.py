import os
from DeleteAPI import get_projs, delete_project, getFolder

DELETE="1"
EMPTY=1

def main():
    projects, excepted_projs = get_projs()
    lien_projects_dic={}

    if len(excepted_projs)>0:
        print("제외할 프로젝트는 다음과 같습니다.")
        print(f"{excepted_projs}\n")
    
    projects = [idx for idx in projects if idx not in excepted_projs]
    print("선택한 프로젝트가 삭제됩니다.")
    print(projects)

    if DELETE == input("계속 진행할까요?(1. yes/2. no) 1 또는 2를 입력하세요"):    
        for proj in projects:
            cmd = f"gcloud alpha resource-manager liens list --project={proj} --format='value('NAME')'"
            result = os.popen(cmd).read()

            if result != "":
                lien_projects_dic[proj]=result.split("\n")[0]
            else:
                delete_project(proj)
        
        if lien_projects_dic:
            print("다음과 같이 보호된 프로젝트가 존재합니다.")
            print(lien_projects_dic)
            if DELETE == input("삭제할까요?(1. yes/2. no) 1 또는 2를 입력하세요"):
                for key in lien_projects_dic.keys():
                    cmd = f"gcloud alpha resource-manager liens delete {lien_projects_dic[key]}"
                    result = os.popen(cmd).read()                    
                    delete_project(key)
        

def main2():
    getFolder()
    
if __name__=="__main__":
    main2()