from utils.similarity import cosine_similarity

a = [1, 2, 3]
b = [1, 2, 3]
c = [5, 6, 7]

print(cosine_similarity(a, b))
print(cosine_similarity(a, c))