
import os
from dotenv import load_dotenv
import braintrust

load_dotenv()
print(f"BRAINTRUST_API_KEY loaded: {bool(os.getenv('BRAINTRUST_API_KEY'))}")


dataset = braintrust.init_dataset(project="My KY Project", name = "My KY Dataset")
print("Dataset created:", dataset)

# 데이터셋 insert
for i in range(10):
    id = dataset.insert(input=i, expected={"result": i + 1, "error": None}, metadata={"foo": i % 2})
    print("Inserted record with id", id)

# 데이터 업데이트
# insert를 할때 id를 리턴하는데 업데이트 할때 이 id를 입력
dataset.update(input=i, expected={"result": i + 1, "error": "Timeout"}, id=id)

#delete record
dataset.delete(id=id)


# 개별 레코드 접근 (fetch 사용)
print("\n=== 데이터셋 요약 정보 ===")
all_records = list(dataset)
print(f"총 레코드 수: {len(all_records)}")
for i in range(len(all_records)):
    print(f"{i} 번째 레코드: {all_records[i]}")


# 데이터 삭제
dataset.flush()

print("데이터 flush 완료")