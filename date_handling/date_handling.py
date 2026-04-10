import datetime as dt

datetime_now = dt.datetime.now()
print ("datetime.now:", datetime_now)
# datetime.now: 2026-04-10 09:02:48.702769

datetime_today = dt.datetime.today()
print ("datetime.today:", datetime_today)
# datetime.today: 2026-04-10 09:02:48.702787

date_today = dt.date.today()
print ("date_today:",date_today)
# DATE OBJECT ALWAYS NAIVE -> No TZ asigned
# date_today: 2026-04-10
## HACE FALTA IMPORTAR TIMEZONE para usar tzinfo
#sys_tz = dt.tzinfo()



# Ver variablel de onjeto tzinfo
#print ("sys_tz:", sys_tz)
print ("datetime_today.tzinfo:", datetime_today.tzinfo)
#print ("datetime_today.offset:", datetime_today.tzinfo.utcoffset(datetime_today))
#print ("datetime_today.dst:", datetime_today.tzinfo.dst)

print ("- - - -")
print("dt.UTC:", dt.UTC)
