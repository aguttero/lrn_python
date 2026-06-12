# Example input list of dictionaries
signers = [
    {"email": "alice@example.com", "role": "Signer"},
    {"email": "bob@example.com", "role": "Approver"},
    {"email": "alice@example.com", "role": "Viewer"},
    {"email": "charlie@example.com", "role": "Signer"},
]

api_response = [
    {
        "email": "bob@example.com",
        "name": "Leonardo",
        "role": "APPROVER",
        "order": 1,
        "label": "Administrador de Servicio",
    },
    {
        "email": "alice@example.com",
        "name": "Ernesto",
        "role": "APPROVER",
        "order": 2,
        "label": "Comprador / Category Buyer",
    },
    {
        "email": "alice2@example.com",
        "name": "Cristian",
        "role": "APPROVER",
        "order": 3,
        "label": "Gerente Linea con Atribuciones",
    },
    {
        "email": "bob2@example.com",
        "name": "Leonardo",
        "role": "APPROVER",
        "order": 4,
        "label": "Gerente de Rubro / Subgerente de Rubro",
    },
    {
        "email": "charlie@example.com",
        "name": "Luis",
        "role": "APPROVER",
        "order": 5,
        "label": "Gerente de Compras",
    },
]


def parse_dict_items(api_response):
    for dict in api_response:
        for key, value in dict.items():
            print(f"{key}: {value}")
        print("- - -")
    return 0


def parse_dict_key(api_response, key):
    for dict in api_response:
        print(dict[key])
        print("- - -")
    return 0


def find_multiple_duplicates(data_list, key, target_count=3):
    seen = set()
    duplicated_values = set()

    for dict in data_list:
        if key in dict:
            val = dict[key]
            if val in seen:
                duplicated_values.add(val)
                # Short-circuit early once we hit your target count (e.g., 3 distinct duplicates)
                if len(duplicated_values) >= target_count:
                    return list(duplicated_values)
            else:
                seen.add(val)

    return list(duplicated_values)


def find_repeat_email(apiresponse: list):
    pass


def has_duplicate_value(data_list, key):
    seen = set()
    for dict in data_list:
        if key in dict:
            val = dict[key]
            if val in seen:
                return True  # Stops instantly on the first duplicate
            seen.add(val)
    return False


def main():

    result = find_multiple_duplicates(api_response, "email", 3)
    print(f"result= {result!r}")
    if result:
        print("valida a True")

    if not result:
        print("valida a False")

    # result = has_duplicate_value(api_response, "email")
    # result = parse_dict_items(api_response)
    # result = parse_dict_key(api_response, "email")

    return 0


if __name__ == "__main__":
    exit_code: int = main()
    print(f"exit code: {exit_code}")
    exit(exit_code)
