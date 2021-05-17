import datetime

d = datetime.datetime.now()
formated_time = d.strftime('%b %d, %Y, %#I:%M %p')
print(formated_time)