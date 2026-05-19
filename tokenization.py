import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")

print("Vocabulary size:", encoder.n_vocab)

text = "Hello, how are you doing today?"

tokens = encoder.encode(text)

print("Tokens:", tokens)

my_tokens = [13225, 11, 1495, 553, 481, 5306, 4044, 30]

decoded_text=encoder.decode(my_tokens)

print(decoded_text)
