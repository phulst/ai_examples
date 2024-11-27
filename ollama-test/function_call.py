from ollama import chat
from ollama import ChatResponse
import requests


def fetch_crypto_price(crypto: str) -> float:
  """
  Only call if user asks for price of 
   a specific cryptocurrency. Fetch crypto price from CoinCap API. 

  Args:
    crypto (str): Cryptocurrency name (e.g., 'bitcoin')

  Returns:
    float: Crypto price in USD
  """
  url = f"https://api.coincap.io/v2/assets/{crypto.lower()}"
  response = requests.get(url)
  
  if response.status_code == 200:
    data = response.json()
    return float(data['data']['priceUsd'])
  else:
    raise Exception(f"Failed to fetch price for {crypto}. Status code: {response.status_code}")


prompt = 'What is the current price of Bitcoin?'
print('Prompt:', prompt)

available_functions = {
  # we only have one function here, but you can add more
  'fetch_crypto_price': fetch_crypto_price
}

response: ChatResponse = chat(
  'llama3.2',
  messages=[{'role': 'user', 'content': prompt}],
  # instead of having to specify the JSON schema for your function, you can now simply
  # pass a direct reference to the function. The JSON schema is automatically generated
  # from the function signature and docstring.
  tools=[fetch_crypto_price],
)
# print(response)

if response.message.tool_calls:
  # There may be multiple tool calls in the response
  for tool in response.message.tool_calls:
    # Ensure the function is available, and then call it
    if function_to_call := available_functions.get(tool.function.name):
      print('Calling function:', tool.function.name)
      print('Arguments:', tool.function.arguments)
      print('Function output:', function_to_call(**tool.function.arguments))
    else:
      print('Function', tool.function.name, 'not found')
