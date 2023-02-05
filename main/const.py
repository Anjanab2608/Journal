app_name = 'Journal'

dB_path = 'main/database/Predictions.db'
week_check = 21
fig = 'figures'
media = 'media'
doc_name = 'journal.docx'
pic_format = '.jpg'
doc_date_format = '%A, %d. %b %Y'

column_name = {'name': [
    'date',
    'smoked_cigarette',
    'played_sport',
    'temp_yesterday',
    'day_answer',
    'drank_alcohol',
    'hours_slept',
    'user_bedtime',
    'user_wake_up_time',
    'prediction']
}

DATA_QUERY = "SELECT * FROM DATA;"
PREDICT_QUERY = "SELECT * FROM PREDICT;"

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
