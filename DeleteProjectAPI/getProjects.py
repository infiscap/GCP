import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from CommonAPI.projectInOrg import get_projects, get_projects_to_json

ALL_PROJECTS="1"
SOME_PROJECTS="2"
DIRECT_PROJECT_NAME="1"
KEYWORD_PROJECT_NAME="2"

def get_projs_in_org(num):
    org_id=input(f'{num}. Organization ID를 입력하세요 (ex - 911781043447)')
    print("project 검색 중 입니다.")
    hierarchy = get_projects("Organization", org_id)
    print(hierarchy)
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