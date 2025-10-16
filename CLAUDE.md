# CLAUDE.md

이 파일은 Claude Code (claude.ai/code)가 이 저장소에서 작업할 때 참고할 가이드를 제공합니다.

## 프로젝트 개요

이 저장소는 AI 평가 및 로깅 플랫폼인 Braintrust를 학습하기 위한 저장소입니다. 다음 내용을 다루는 예제와 실험들이 포함되어 있습니다:
- 오프라인 평가 (체계적 비교를 위한 구조화된 실험)
- 온라인 평가 (실시간 성능 모니터링)
- AI 애플리케이션 요청 로깅 및 트레이싱
- OpenAI 및 autoevals 점수 함수 통합

## 환경 설정

**Python 버전**: 3.12.9 (`.python-version`으로 관리)

**패키지 매니저**: uv (최신 Python 패키지 매니저)

**의존성 설치**:
```bash
uv sync
```

**가상환경 활성화**:
```bash
source .venv/bin/activate
```

**필수 환경 변수** (`.env` 파일):
- `BRAINTRUST_API_KEY`: 모든 Braintrust 작업에 필수
- `OPENAI_API_KEY`: OpenAI를 사용하는 예제에 필수

## Eval 실행 방법

**단일 eval 파일 실행**:
```bash
braintrust eval path/to/file.py
```

**디렉토리 내 모든 eval 실행**:
```bash
braintrust eval experiments/1.write_evals/
```

**Watch 모드** (파일 변경 시 자동 재실행):
```bash
braintrust eval --watch path/to/file.py
```

**개발 모드**:
```bash
braintrust eval --dev path/to/file.py
```

**Python 스크립트 직접 실행** (로깅 예제용):
```bash
python path/to/script.py
```

## 프로젝트 구조

### `/quickstart/`
기본 입문 예제:
- `eval_tutorial.py`: Levenshtein 점수를 사용한 간단한 "Say Hi Bot" eval
- `wrap_openai.py`: Braintrust 트레이싱을 위한 OpenAI 호출 래핑
- `wrap_openai_stream.py`: 트레이싱이 적용된 OpenAI 스트리밍 응답
- `wrap_openai_add.py`: 더 복잡한 OpenAI 통합 패턴
- `eval_openai.py`: OpenAI 기반 작업 평가

### `/experiments/`
주제별로 구성된 구조화된 학습 예제:

**1.write_evals/** - 평가 실험 작성:
- `1-1.eval_basic.py`: 핵심 Eval() 함수 구조 및 구성요소 (data, task, scores)
- `1-2.scores.py`: autoevals의 다양한 점수 함수 사용
- `1-3.unhandled_scores.py`: 커스텀 점수 로직
- `1-4.eval_closed_q_a.py`: 폐쇄형 Q&A 평가 패턴
- `1-5.hill_climing.py`: 반복적 개선 전략
- `1-6.custom_reporters.py`: 커스텀 결과 리포팅

**2.run_evals/** - 실행 패턴:
- `2-1.run_code_directly.py`: CLI 대비 프로그래밍 방식으로 eval 실행

### `/Logs/`
로깅 및 트레이싱 예제:
- `1.write_logs/1.write_logs.py`: `@traced` 데코레이터와 `init_logger()`를 사용한 기본 로깅
- `1.write_logs/2.user_feedback.py`: `log_feedback()`으로 사용자 피드백 캡처

### `/cookbook/`
완전한 엔드투엔드 예제가 포함된 Jupyter 노트북:
- `1.ai_search_evals.ipynb`: AI 검��� 애플리케이션 평가
- `2.classifying_news_articles.ipynb`: 텍스트 분류 평가

## 핵심 Braintrust 개념

### Eval 구성요소
모든 eval은 세 가지 구성요소로 이루어집니다:
1. **Data**: `input`, 선택적 `expected`, `metadata`, `tags`를 포함하는 테스트 케이스
2. **Task**: 입력을 받아 출력을 반환하는 함수 (일반적으로 LLM 호출)
3. **Scores**: 출력 품질을 평가하는 함수들 (예: Levenshtein, Factuality)

### 데이터 구조 일관성
로그와 실험은 동일한 데이터 구조를 사용합니다. 이는 다음을 의미합니다:
- eval용 계측(instrumentation)을 로깅에 재사용 가능
- 기록된 트레이스가 실험과 동일한 데이터 캡처
- 자동화된 점수가 실험과 로그 모두에서 작동

### 트레이싱
`@traced` 데코레이터(Python) 또는 `wrap_openai()`를 사용하여 함수의 입력/출력을 자동으로 캡처합니다. 이는 트레이스 내에 스팬(span)을 생성하여 상세한 관찰성을 제공합니다.

### 사용자 피드백
`log_feedback()`을 사용하여 로그된 요청에 대한 피드백을 캡처합니다:
- 점수 (예: 좋아요/싫어요를 1/0으로)
- 예상 값 (수정 사항)
- 댓글 (자유 형식 텍스트)
- 추가 메타데이터 (user_id, session_id 등)

## 일반적인 패턴

**기본 eval 구조**:
```python
from autoevals import Levenshtein
from braintrust import Eval

Eval(
    "프로젝트 이름",
    data=lambda: [{"input": "...", "expected": "..."}],
    task=lambda input: model_call(input),
    scores=[Levenshtein],
)
```

**트레이싱을 사용한 로깅**:
```python
from braintrust import init_logger, traced

logger = init_logger(project="프로젝트 이름")

@traced
def my_function(input):
    # 함수가 자동으로 트레이싱됨
    return result
```

**OpenAI 래핑**:
```python
from braintrust import wrap_openai
from openai import OpenAI

client = wrap_openai(OpenAI())
# 모든 호출이 자동으로 트레이싱됨
```

## 개발 참고사항

- 저장소는 README 파일에 한글 주석과 문서를 사용합니다
- 모든 예제는 `.env`에 유효한 API 키가 필요합니다 (구조는 `.env` 참고)
- 결과는 eval 실행 후 Braintrust UI에서 확인 가능합니다
- 이 코드베이스는 주로 교육/실험용이며, 예제가 존재하지 않는 프로젝트를 참조할 수 있습니다