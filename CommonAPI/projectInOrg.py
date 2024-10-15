from typing import Dict, List, Union
from google.cloud import resourcemanager_v3


def get_folders(
    parent_id: str = "organizations/12345",
    folders: Dict[str, str] = None,
) -> Dict[str, str]:
    if folders is None:
        folders = {}
    client = resourcemanager_v3.FoldersClient()
    request = resourcemanager_v3.ListFoldersRequest(
        parent=parent_id,
    )
    page_result = client.list_folders(request=request)
    # if page_result:
    #     print("page_result")
    # if not page_result:
    #     print("not page_result")
    # print(f"{parent_id} - {page_result.folders}")
    for pages in page_result:
        # print(type(pages.name))
        # print(type(pages.display_name))
        folders[pages.name] = pages.display_name
        get_folders(parent_id=pages.name, folders=folders)
    return folders

def projects_in_folder(parent_type:str = "folder", obj_id: str="") -> List[str]:
    client = resourcemanager_v3.ProjectsClient()
    query = f'parent.type:{parent_type} parent.id:{obj_id}'
    request = resourcemanager_v3.SearchProjectsRequest(query=query)
    response = client.search_projects(request=request)

    projects = []
    for project in response:
        if project.state == resourcemanager_v3.Project.State.ACTIVE:
            projects.append(project.project_id)

    return projects

def get_folder_hierarchy(
    parent_id: str = "organizations/12345",
    hierarchy: Union[Dict[str, Union[str, List[str]]], None] = None,
) -> Dict[str, Union[str, List[str]]]:

    if hierarchy is None:
        hierarchy = {}

    client = resourcemanager_v3.FoldersClient()
    request = resourcemanager_v3.ListFoldersRequest(parent=parent_id)
    response = client.list_folders(request=request)

    for folder in response:
        folder_id = folder.name.split('/')[-1]
        folder_name = folder.display_name
        projects = projects_in_folder(obj_id=folder_id)

        if projects:
            hierarchy[folder_name] = projects

        sub_hierarchy = get_folder_hierarchy(parent_id=folder.name, hierarchy={})
        if sub_hierarchy:
            hierarchy[folder_name].append( sub_hierarchy )
    return hierarchy


def get_projects(org_name, org_id):
    hierarchy={}
    hierarchy[org_name] = projects_in_folder("organization", org_id)
    hierarchy[org_name].append( get_folder_hierarchy(f"organizations/{org_id}") )
    
    return hierarchy

def get_projects_to_json(resource: Union[Dict[str, Union[str, List[str]]], None]):
    projects = []

    if resource is None:
        return

    #org or folder list
    for key in resource.keys(): 
        if isinstance(resource[key], list):
            # project list
            for idx in range(len(resource[key])):
                if isinstance(resource[key][idx], dict):
                    return_proj = get_projects_to_json(resource[key][idx]) 
                    for proj in return_proj:
                        projects.append( proj)
                else:
                    # project
                    projects.append(resource[key][idx])
    return projects

def display_directory(hierarchy: Union[Dict[str, Union[str, List[str]]], None], space:int = 0):
    if hierarchy is None:
        return
    for key in hierarchy.keys():
        print(" " * space * 4 + key)
        if isinstance(hierarchy[key], list):
            for idx in range(len(hierarchy[key])):
                if isinstance(hierarchy[key][idx], dict):
                    display_directory(hierarchy[key][idx], space+1)
                elif isinstance(hierarchy[key][idx], list):
                    for data in hierarchy[key][idx]:
                        print(data)
                else:
                    print(" " * (space+1) * 4 + hierarchy[key][idx])
                