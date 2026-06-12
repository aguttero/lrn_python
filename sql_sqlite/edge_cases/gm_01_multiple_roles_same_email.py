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
