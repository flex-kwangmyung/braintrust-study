## Datasets

Datasets을 사용하면 운영 환경(production), 스테이징, 평가(evaluations), 심지어 수동으로도 데이터를 수집하고, 그 데이터를 활용해 평가를 실행하며 시간이 지남에 따라 개선 사항을 추적할 수 있습니다.

예를 들어 Datasets를 통해 다음을 수행할 수 있습니다:
- 대형 JSONL이나 CSV 파일을 직접 관리하는 대신, 평가 스크립트용 테스트 케이스를 저장
- 운영 환경에서 생성된 모든 응답을 로깅하고, 수동으로 또는 모델 채점 기반 평가로 품질을 점검
- 사용자 검토가 완료된 생성물(리뷰/피드백)을 저장해 새로운 테스트 케이스를 발굴

Braintrust에서 dataset은 다음과 같은 핵심 특성을 갖습니다:
- Integrated: Datasets는 Braintrust 플랫폼의 다른 기능과 통합되어 있어, 평가에서 사용하고, Playground에서 탐색하며, 스테이징/운영 환경에서 직접 로깅할 수 있습니다.

- Versioned. 모든 삽입, 업데이트, 삭제에는 버전이 매겨지며, SDK를 통해 평가를 특정 dataset 버전에 고정(pinning)할 수 있습니다.

- Scalable. Datasets는 현대적인 클라우드 데이터 웨어하우스에 저장되므로, 저장 용량이나 성능 한계를 걱정하지 않고 원하는 만큼 데이터를 수집할 수 있습니다.

- Secure. Braintrust를 사용자의 클라우드 환경에서 실행하는 경우, datasets는 사용자의 웨어하우스에 저장되며 당사 인프라를 거치지 않습니다.


## Manage datasets with the SDK

dataset의 레코드는 JSON 객체로 저장되며, 각 레코드는 상위 수준의 세 가지 필드를 가집니다:

- input: 애플리케이션에서 예제를 재현하는 데 사용할 수 있는 입력 집합입니다. 예를 들어, 질의응답 모델에서 예제를 로깅한다면 input에는 질문이 들어갈 수 있습니다.

- expected (선택): 모델의 출력입니다. 예를 들어 질의응답 모델이라면 답변이 될 수 있습니다. 평가 실행 시 expected 필드로 접근할 수 있지만, expected가 반드시 정답(ground truth)일 필요는 없습니다.

- metadata (선택): 데이터를 필터링하고 그룹화하는 데 사용할 수 있는 키-값 쌍의 집합입니다. 예를 들어 질의응답 모델의 예제를 로깅한다면, 질문의 지식 소스 같은 정보를 metadata에 담을 수 있습니다.

### Creat a dataset
SDK에서 초기화 할때 자동 생성됩니다.
```python
import braintrust
 
dataset = braintrust.init_dataset(project="My App", name="My New Dataset")
print("Dataset created:", dataset)

```

### Read a dataset
```python
dataset = braintrust.init_dataset(project="My App", name="My Existing Dataset")
print("Dataset retrieved:")
 
for row in dataset:
    print(row)

```

### Filter, sort, and limit dataset
생략

