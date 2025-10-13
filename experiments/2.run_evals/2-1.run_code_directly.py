# braintrust eval 대신 코드에서 직접 호출 가능

from autoevals import Factuality
from braintrust import Eval
 
 
# def main():
#     result = Eval(
#         "Say Hi Bot",
#         data=lambda: [
#             {
#                 "input": "David",
#                 "expected": "Hi David",
#             },
#         ],
#         task=lambda input: "Hi " + input,
#         scores=[Factuality],
#     )
#     print(result)
 
 

async def main():
    result = await Eval(
        "Say Hi Bot",
        data=lambda: [
            {
                "input": "David",
                "expected": "Hi David",
            },
        ],
        task=lambda input: "Hi " + input,
        scores=[Factuality],
    )
    print(result)