import os
from getProjects import get_projs_in_org, get_projs, delete_project


DELETE="1"
EMPTY=1


def main():
    projects, excepted_projs = get_projs()

    if len(excepted_projs)>0:
        print("제외할 프로젝트는 다음과 같습니다.")
        print(excepted_projs)
    
    if DELETE == input("선택한 프로젝트가 삭제됩니다. 계속 진행할까요?(1. yes/2. no) 1 또는 2를 입력하세요"):
        projects = [idx for idx in projects if idx not in excepted_projs]

        cmd = "gcloud alpha resource-manager liens list"
        result = os.popen(cmd).read()
        print(result)
        
        # for proj in projects:
        #     delete_project(proj)
    

if __name__=="__main__":
    main()
