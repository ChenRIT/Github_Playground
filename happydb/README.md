Goal: extract entities that make people happy

Workflow (take product names as an example):

1. Obtain ground truth (e.g., samples of the products people buy)
   1)  List a few common products.
   2)  Write a script to count appearance frequency of a few known entities (e.g., bike or car).
       - Input: happy moments HM
       - Output: A dictionary DF of form {key: value}, where "key" represents entity names (type: str), and "value" represents the numbers of appearance (type: int)
   3)  Write a script to find all happy moments that contain keywords related to purchase behavior, e.g., "buy", "bought", "order" and "purchase".
       - Input: happy moments HM (in txt or csv format)
       - Output: happy moments HPR related to purchasing (in txt)
   4)  Manually scan through HPR to find patterns of qualified entities.

2. Write KOKO queries to extract product names.
3. Compare KOKO's results with DF for performance evaluation.