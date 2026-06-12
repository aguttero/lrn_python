from collections import defaultdict

# Example input list of dictionaries
signers = [
    {"email": "alice@example.com", "role": "Signer"},
    {"email": "bob@example.com", "role": "Approver"},
    {"email": "alice@example.com", "role": "Viewer"},
    {"email": "charlie@example.com", "role": "Signer"},
]

# 1. Group all roles by email
email_roles = defaultdict(list)
for signer in signers:
    email_roles[signer["email"]].append(signer["role"])

print("email_roles:", email_roles)

from collections import Counter

# Extract all values for the key
all_values = [d[key] for d in data_list if key in d]

# Count frequencies
counts = Counter(all_values)

# Filter out values that appear more than once
all_duplicates = [val for val, count in counts.items() if count > 1]


# 2. Separate into repeated and non-repeated dictionaries
# repeated_signers = {}
# non_repeated_signers = {}

# for email, roles in email_roles.items():
#     if len(roles) > 1:
#         # Include all roles associated with the repeated email
#         repeated_signers[email] = roles
#     else:
#         # Keep the single role as a string instead of a list
#         non_repeated_signers[email] = roles[0]

# print("Repeated:", repeated_signers)
# print("Non-Repeated:", non_repeated_signers)
