## Experiments

Experiments를 통해 AI 애플리케이션의 성능을 스냅샷으로 기록하여 지속 개선할 수 있음.   

기존 소프트웨어에서 성능은 일반적으로 속도를 의미함. 
 - 예를 들어 요청을 완료하는 데 걸리는 밀리초 수 등이 있음 
 - AI에서는 속도 외에도 정확도나 품질 등 다른 측정 기준을 포함하는 경우가 많음. 
   - 이러한 유형의 지표는 특히 대규모 환경에서 정의하고 측정하기가 더 어려움. 
   - LLM 애플리케이션의 성능을 평가하는 것을 평가(evaluation)라고 합니다.

Braintrust는 두 가지 유형의 평가를 지원함:

- 오프라인 평가는 애플리케이션을 체계적으로 비교하고 개선하기 위한 구조화된 실험.
- 온라인 평가는 실시간 요청에 스코어러를 실행하여 성능을 실시간으로 모니터링.

양쪽 유형의 평가는 모두 고품질 AI 애플리케이션 구축에 중요함.

### 평가(evals)가 중요한 이유?
인공지능 개발 과정에서 팀이 업데이트가 성능에 미치는 영향을 파악하기란 어려움.   
이는 일반적인 소프트웨어 개발 루프를 깨뜨려, 반복 작업을 공학적 접근이 아닌 추측 작업처럼 느끼게 만듬.

평가(Evaluations)는 이 문제를 해결함.  
AI 애플리케이션의 비결정적 출력을 효과적인 피드백 루프로 정제하여 더 안정적이고 고품질의 제품을 출시할 수 있도록 지원함.

구체적으로, 우수한 평가(Eval)는 다음과 같은 도움을 즘:
- 업데이트가 개선인지 퇴보인지 파악
- 좋은 예시/나쁜 예시로 신속하게 파고들기
- 특정 예시와 이전 실행 결과 비교
- 도마뱀 잡기식 대응(whack-a-mole) 방지

### Breaking down evals
evals는 3가지 파트로 구성됨
- Data: 애플리케이션을 테스트하기 위한 예시 집합, [추후 다시 살펴봄](https://www.braintrust.dev/docs/guides/datasets)
평가 데이터셋은 테스트 케이스 목록입니다. 각 테스트 케이스에는 입력값과 선택적 예상 출력값, 메타데이터, 태그가 포함됩니다. 데이터 레코드의 주요 필드는 다음과 같습니다:

    - Input: 테스트 케이스를 고유하게 정의하는 인자(임의의 JSON 직렬화 가능 객체). Braintrust는 `input`을 통해 평가 실행 간 두 테스트 케이스가 동일한지 판단하므로, 실행별 상태 정보는 포함하지 않아야 함. 동일한 평가를 두 번 실행할 때 `input`이 동일해야 함.
    - Expected (선택 사항): output과 비교하여 output의 정확성을 판단할 기준값(임의의 JSON 직렬화 가능 객체). Braintrust는 output과 expected를 자동으로 비교하지 않음. 이를 올바르게 수행하는 방법은 다양하기 때문.
    - Metadata. (선택 사항): 테스트 예시, 모델 출력 또는 관련성이 있는 기타 모든 것에 대한 추가 데이터가 포함된 dictionary. 예시를 찾고 분석하는 데 사용할 수 있음. 예를 들어 프롬프트, 예시의 ID, 모델 매개변수 또는 나중에 분류/분석하는 데 유용한 기타 정보를 기록할 수 있음.
    - Tags(선택 사항): 나중에 레코드를 필터링하고 그룹화하는 데 사용할 수 있는 문자열 리스트.

- Task: 테스트하려는 AI 함수(입력을 받아 출력을 반환하는 모든 함수)
- Scores: 입력, 출력, 선택적 기대값을 받아 점수를 계산하는 점수 함수 집합

위 3가지는 Eval 함수로 설정 가능함
```python
from autoevals import Levenshtein
from braintrust import Eval
 
Eval(
    "Say Hi Bot",  # Replace with your project name
    data=lambda: [
        {
            "input": "Foo",
            "expected": "Hi Foo",
        },
        {
            "input": "Bar",
            "expected": "Hello Bar",
        },
    ],  # Replace with your eval dataset
    task=lambda input: "Hi " + input,  # Replace with your LLM call
    scores=[Levenshtein],
)
```

### Viewing experiments
Eval 함수를 호출하면 Braintrust에 experiment를 생성하고 터미널에 결과를 보여준다.  

UI를 통해 AI 애플리케이션의 성능을 명확히 파악할 수 있으며 다음 작업 수행가능:

- 테이블에서 각 테스트 케이스와 점수를 미리 보기
- 높은 점수/낮은 점수로 필터링
- 개별 사례를 클릭하여 상세 추적 정보 확인
- 상위 점수 확인
- 개선 사항 또는 퇴보 사항으로 정렬

### Run evals
```bash
braintrust eval eval_basic.py

braintrust eval [file or directory] [file or directory] ...
```
- `--watch`: watch mode
- `--dev` : dev mode

**Github action**
- braintrustdata/eval-action 액션을 사용하면 Github 워크플로 내에서 직접 평가를 실행할 수 있음. 
- 평가를 실행할 때마다 액션이 자동으로 댓글을 게시:

- 사용을 위해 `.github/workflows`에 yaml 파일 추가
- 예시
```yaml
name: Run Python evals
 
on:
  push:
    # Uncomment to run only when files in the 'evals' directory change
    # - paths:
    #     - "evals/**"
 
permissions:
  pull-requests: write
  contents: read
 
jobs:
  eval:
    name: Run evals
    runs-on: ubuntu-latest
 
    steps:
      - name: Checkout
        id: checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
 
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.12" # Replace with your Python version
 
      # Tweak this to a dependency manager of your choice
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r test-eval-py/requirements.txt
 
      - name: Run Evals
        uses: braintrustdata/eval-action@v1
        with:
          api_key: ${{ secrets.BRAINTRUST_API_KEY }}
          runtime: python
          root: my_eval_dir
```

자세한 내용은 [여기](https://github.com/braintrustdata/eval-action) 참고

### Interpret evals

UI 상세보기는 다음 기능을 제공
- Diff mode toggle: 평가 실행 간 비교를 가능하게 합니다. 토글을 클릭하면 현재 평가 결과와 기준선 결과를 비교하여 확인할 수 있습니다.
- Filter바: 테스트 케이스의 하위 집합에 집중할 수 있습니다. 자연어 또는 BTQL을 입력하여 필터링할 수 있습니다.
- Column visivility: 열 표시 여부를 전환할 수 있습니다. 문제 영역을 집중적으로 확인하기 위해 회귀 분석별로 열을 정렬할 수도 있습니다.
- Table: 평가 실행의 모든 테스트 케이스에 대한 데이터를 표시합니다.