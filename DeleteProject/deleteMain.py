import os
from DeleteAPI import get_projs_in_org, get_some_projs, DeleteProject, DeleteLienProject, DeleteFolder

DELETE="1"
EMPTY=1
SOME_PROJECTS="2"

def main():
    num=1
    excepted_projs=[]
    
    projects, org_id = get_projs_in_org(num)
    num = num + 1
    choice = input(f"{num}. 모든 프로젝트를 제거하시겠습니까?(1. yes/2. no) 1 또는 2를 입력하세요")
    
    if choice==SOME_PROJECTS:
        excepted_projs = get_some_projs(projects, num)

    if len(excepted_projs)>0:
        print("제외할 프로젝트는 다음과 같습니다.")
        print(f"{excepted_projs}\n")
    
    projects = [idx for idx in projects if idx not in excepted_projs]
    print("선택한 프로젝트가 삭제됩니다.")
    print(projects)

    if DELETE == input("계속 진행할까요?(1. yes/2. no) 1 또는 2를 입력하세요"):    
        lien_projects_dic = DeleteProject(projects)
        if lien_projects_dic:
            print("다음과 같이 보호된 프로젝트가 존재합니다.")
            print(lien_projects_dic)
            if DELETE == input("삭제할까요?(1. yes/2. no) 1 또는 2를 입력하세요"):
                DeleteLienProject(lien_projects_dic)
        DeleteFolder()
        
    
if __name__=="__main__":
    main()