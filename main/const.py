app_name = 'Journal'

dB_path = 'main/database/Predictions.db'
week_check = 21
fig = 'main/figures'
media = 'main/media'
doc_name = 'journal.docx'
pic_format = '.jpg'
doc_date_format = '%A, %d. %b %Y'

# SQL QUERIES
DATA_QUERY = "SELECT * FROM DATA;"
PREDICT_QUERY = "SELECT * FROM PREDICTION;"

# column names
date = 'date'
smoke = 'smoked_cigarette'
sport = 'played_sport'
temp = 'temp_yesterday'
alcohol = 'drank_alcohol'
sleep = 'hours_slept'
bedtime = 'user_bedtime'
wake_time = 'user_wake_up_time'
answer = 'predicted'
para = 'para'

# Credentials
cred = 'main/cred/credentials.json'
google_cred = 'main/cred/google-drive-credentials.json'
scope = ['https://www.googleapis.com/auth/drive']

real_file_id = '1jqPGS_-Tk1ApjUKq_M6ByNKpwZL80Cn2'
date_format = '%Y-%m-%d'
page_size = 6
pixel_size = 1000
file_type = 'image/jpg'
drive_filepath = './Weather_1'
drive_sample = 'tornado.jpg'

queue = "name contains 'weather'"
