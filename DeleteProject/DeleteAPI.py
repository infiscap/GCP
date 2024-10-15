import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from CommonAPI.projectInOrg import get_projects, get_projects_to_json, get_folders
from google.cloud import resourcemanager_v3

ALL_PROJECTS="1"
DIRECT_PROJECT_NAME="1"
KEYWORD_PROJECT_NAME="2"
NO = "2"
GAP = 10
DELETE="1"
ENDOFFOLDER = True

def delete_folder(folder_id):
    client = resourcemanager_v3.FoldersClient()
    request = resourcemanager_v3.DeleteFolderRequest(
        name=folder_id,
    )
    operation = client.delete_folder(request=request)

    print("Waiting for operation to complete...")
    response = operation.result()
    print(response)

def DeleteFolder(
    parent_id: str = "organizations/12345"
) -> bool:
    client = resourcemanager_v3.FoldersClient()
    request = resourcemanager_v3.ListFoldersRequest(
        parent=parent_id,
    )
    page_result = client.list_folders(request=request)
    if not page_result.folders:
        return ENDOFFOLDER
   
    for pages in page_result:
        if ENDOFFOLDER == DeleteFolder(parent_id=pages.name):
            delete_folder(pages.name)
    return ENDOFFOLDER

    
def get_projs_in_org(num):
    org_id=input(f'{num}. Organization ID를 입력하세요 (ex - 911781043447)')
    print("project 검색 중 입니다.")
    hierarchy = get_projects("Organization", org_id)
    
    return get_projects_to_json(hierarchy), org_id

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
    


def get_some_projs(projects, num):
    excepted_projs=[]

    cnt = int(len(projects) / GAP)+1
    # if cnt==0:
    #     excepted_projs = excepted_projs + except_projects(projects, num)
    for page_cnt in range(0, cnt):
        start = page_cnt * GAP
        end = start + GAP
        excepted_projs = excepted_projs + except_projects(projects[start:end], num)

        if NO == input(f"{num+1}. 더 제외할 프로젝트가 있나요?(1. yes/2. no) 1 또는 2를 입력하세요"):
            break
        
    return excepted_projs


def delete_project(project_id):
    client = resourcemanager_v3.ProjectsClient()

    request = resourcemanager_v3.DeleteProjectRequest(
        name=f"projects/{project_id}",
    )
    operation = client.delete_project(request=request)

    print("Waiting for operation to complete...")
    response = operation.result()
    print(response)
    
def DeleteProject(projects):
    lien_projects_dic={}
    
    for proj in projects:
        cmd = f"gcloud alpha resource-manager liens list --project={proj} --format='value('NAME')'"
        result = os.popen(cmd).read()

        if result != "":
            lien_projects_dic[proj]=result.split("\n")[0]
        else:
            delete_project(proj)
    return lien_projects_dic

def DeleteLienProject(lien_projects_dic):
    for key in lien_projects_dic.keys():
        cmd = f"gcloud alpha resource-manager liens delete {lien_projects_dic[key]}"
        os.popen(cmd).read()                    
        delete_project(key)