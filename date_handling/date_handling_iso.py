from datetime import datetime, timedelta

## Calculo de fechas
# GET LAST RANGE END DATE
end_date_str = "2026-03-01T00:00:00Z"
end_date = datetime.fromisoformat(end_date_str.replace("Z","+00:00"))
end_date_3_11 = datetime.fromisoformat(end_date_str)
print("end_date_str:", end_date_str)
print("end_date:", end_date)
print("end_date_3_11+:", end_date_3_11)
new_end_date = end_date_3_11 + timedelta(days=7)
print("new_end_date:", new_end_date)
new_end_date_str = f"{new_end_date.date()}T00:00:00Z"
print ("new_end_date_str:",new_end_date_str)
