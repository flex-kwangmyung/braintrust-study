# Tracing
- Tracing은 프로그램의 최상위 입력과 출력을 만들어내는 하위 구성요소를 탐색하는 데 매우 유용한 도구입니다. 
- 현재 Tracing은 logging과 evaluations에서 지원됩니다.

## Anatomy of a trace
하나의 trace는 독립적인 단일 요청을 나타내며, 여러 개의 span으로 구성됩니다.
- eval span, task span, score span, llm span....

span은 시작/종료 시간이 있는 하나의 작업 단위를 의미하며, 선택적으로 입력(input), 출력(output), 메타데이터(metadata), 점수(scores), 지표(metrics) 등의 필드를 포함할 수 있습니다(이 필드들은 experiment
에서 로깅할 수 있는 것들과 동일합니다).   
각 span은 보통 부모 span 내부에서 실행되는 하나 이상의 하위 span을 포함하며, 예를 들어 중첩 함수 호출이 이에 해당합니다.   
일반적인 span 사례로는 LLM 호출, 벡터 검색, 에이전트 체인의 단계, 모델 평가 등이 있습니다.

각 trace는 펼쳐서 내부의 모든 span을 확인할 수 있습니다.   
잘 설계된 trace는 애플리케이션의 흐름을 쉽게 이해하도록 도와주며, 문제가 발생했을 때 디버깅을 용이하게 합니다.  
Tracing API는 온라인(프로덕션 로깅)과 오프라인(평가)에서 동일한 방식으로 동작합니다.