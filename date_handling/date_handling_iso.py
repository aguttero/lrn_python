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


# VALIDATE That range new end date is in the past:
test_last_end_date_str = "2026-04-04T00:00:00Z"
test_start_range_date_str = test_last_end_date_str


test_end_range_date_3_11 = datetime.fromisoformat(test_start_range_date_str.replace("T00:00:00Z"," 00:00:00")) + timedelta(days=7)

#test_end_range_date_3_11_naive = test_end_range_date_3_11.date()

print ("- - - - ")
datetime_today = datetime.today()
print ("datetime.today:", datetime_today)
print ("test_end_range_date_3_11:", test_end_range_date_3_11)
#print ("test_end_range_date_3_11_naive:", test_end_range_date_3_11_naive)

print ("- - - - ")

if datetime_today >= test_end_range_date_3_11:
    print ("OK to run search")
else:
    print ("ERROR - Reschedule Chron")
