import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from CommonAPI.projectInOrg import get_projects, get_projects_to_json, get_folders
from google.cloud import resourcemanager_v3

ALL_PROJECTS="1"
SOME_PROJECTS="2"
DIRECT_PROJECT_NAME="1"
KEYWORD_PROJECT_NAME="2"
NO = "2"
GAP = 10

def getFolder():
    print(get_folders("organizations/911781043447"))
    
def get_projs_in_org(num):
    org_id=input(f'{num}. Organization ID를 입력하세요 (ex - 911781043447)')
    print("project 검색 중 입니다.")
    hierarchy = get_projects("Organization", org_id)
    
    return get_projects_to_json(hierarchy)

def except_projects(projects, num):
    excepted_projs=[]
    cnt = 0
    for proj in projects:
        print(f"{cnt}. {proj}")
        cnt = cnt + 1

    nums = input(f"{num}. 제외할 프로젝트 번호를 띄어쓰기(' ')로 구분하여 입력하시오")

    idxs = nums.split(" ")

    for idx in idxs:
        excepted_projs.append(projects[int(idx)])

    return excepted_projs
    


def get_projs():
    projects=[]
    excepted_projs=[]
    num=1
    choice = input(f"{num}. 모든 프로젝트를 제거하시겠습니까?(1. yes/2. no) 1 또는 2를 입력하세요")
    
    num = num + 1
    projects = get_projs_in_org(num)

    num = num + 1

    
    if choice==SOME_PROJECTS:
        cnt = int(len(projects) / GAP)+1
        if cnt==0:
            excepted_projs = excepted_projs + except_projects(projects, num)
        for page_cnt in range(0, cnt):
            start = page_cnt * GAP
            end = start + GAP
            excepted_projs = excepted_projs + except_projects(projects[start:end], num)

            if NO == input(f"{num+1}. 더 제외할 프로젝트가 있나요?(1. yes/2. no) 1 또는 2를 입력하세요"):
                break
        
    return projects, excepted_projs


def delete_project(project_id):
    client = resourcemanager_v3.ProjectsClient()

    request = resourcemanager_v3.DeleteProjectRequest(
        name=f"projects/{project_id}",
    )

    # Make the request
    operation = client.delete_project(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)