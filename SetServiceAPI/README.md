# 사용법(공사중 ...)

## 1. 파일 옮기기

GCP Terminal에 projectInOrg.py와 servicesDisable.py를 옮긴다.

## 2. 실행

$ **python servicesDisable.py**

Organization ID를 입력하세요 (ex - 541096552061)  **541096552061**

*project 검색 중 입니다.
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1725329996.612802    8446 config.cc:230] gRPC experiments enabled: call_status_override_on_cancellation, event_engine_dns, event_engine_listener, http2_stats_fix, monitoring_experiment, pick_first_new, trace_record_callops, work_serializer_clears_time_cache*

Disable할 service name을 입력하세요(ex - containerscanning.googleapis.com)  **containerscanning.googleapis.com**


*Updated property [core/project].
commitment-demo*

*Updated property [core/project].
younkicho-364103*

위와 같은 형식으로 나타나며 ORG에 있는 모든 프로젝트의 service API를 disable 하게 된다.

