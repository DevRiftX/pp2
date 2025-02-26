import re

def searcher(txt, pattern):
    if re.search(pattern, txt):
        print(f'"{txt}" contains the pattern')
    else:
        print(f'"{txt}" does not contain the pattern')

def matcher(txt, pattern):
    if re.match(pattern, txt):
        print(f'"{txt}" matches the pattern')
    else:
        print(f'"{txt}" does not match the pattern')

def full_matcher(txt, pattern):
    if re.fullmatch(pattern, txt):
        print(f'"{txt}" fully matches the pattern')
    else:
        print(f'"{txt}" does not fully match the pattern')

# 1. Matches 'a' followed by zero or more 'b'
txt = input("Enter a string for pattern 'ab*': ")
pattern = r"ab*"
matcher(txt, pattern)

# 2. Matches 'a' followed by exactly 2 to 3 'b'
txt = input("Enter a string for pattern 'abb' or 'abbb': ")
pattern = r"abb{1,2}"
matcher(txt, pattern)

# 3. Find sequences of lowercase letters joined with an underscore
txt = input("Enter a string for pattern '[a-z]+_[a-z]+': ")
pattern = r"[a-z]+_[a-z]+"
searcher(txt, pattern)

# 4. Find sequences of an uppercase letter followed by lowercase letters
txt = input("Enter a string for pattern '[A-Z][a-z]+': ")
pattern = r"[A-Z][a-z]+"
searcher(txt, pattern)

# 5. Matches 'a' followed by anything, ending in 'b'
txt = input("Enter a string for pattern 'a.*b': ")
pattern = r"a.*b"
matcher(txt, pattern)

# 6. Replace spaces, commas, and dots with a colon
txt = "Hello, world. Python is amazing."
result = re.sub(r"[ ,.]+", ":", txt)
print("Modified text:", result)

# 7. Convert snake_case to CamelCase
txt = "hello_world_example"
result = ''.join(word.title() for word in txt.split('_'))
print("CamelCase:", result)

# 8. Split string at uppercase letters
txt = "AhahsahashahsAHhasdhashashhsa"
pattern = re.findall(r"[A-Z][^A-Z]*", txt)
print("Split at uppercase:", pattern)

# 9. Insert spaces before uppercase letters
txt = "AtahaAnAhasdhhasdhsad"
result = re.sub(r"([A-Z])", r" \1", txt).strip()
print("With spaces:", result)

# 10. Convert CamelCase to snake_case
txt = "HelloWorldExample"
result = re.sub(r"([A-Z])", r"_\1", txt).lower().lstrip("_")
print("Snake case:", result)