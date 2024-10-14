# 사용법

## 1. 파일 옮기기

git clone https://github.com/infiscap/GCP.git

## 2. 실행

$ **python setServicesMain.py**

### 2.1 프로젝트 선택

- 모든 프로젝트 선택 : Org에 있는 모든 프로젝트

- 프로젝트 직접 입력 : 사용자가 API를 설정할 프로젝트명 직접 입력

- keyword 입력 : ORG에 포함되어 있는 프로젝트에서 keyword가 포함된 프로젝트만 검색

### 2.2 org 및 service name 설정

- Organization ID : 모든 프로젝트나 keyword 처리시 사용할 org id

- Service name : 적용할 Service name(ex containerscanning.googleapis.com)

- enable / disable : service의 적용 및 해제