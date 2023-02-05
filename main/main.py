# Importing all the required libraries
import const
from photoImport import Credential
# from anjan_task import *


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    upload = Credential(
        google_cred=const.google_cred,
        app_name=const.app_name,
        client_secret=const.cred,
        scope=const.scope
    )
    upload.listFiles(size=const.page_size)
    upload.download_file(real_file_id=const.real_file_id, filepath=const.drive_filepath)
    upload.resize_image(img_path=const.drive_filepath, date_format=const.date_format, max_size=const.pixel_size)
    upload.create_folder(filepath=const.drive_filepath)
    upload.uploadFile(filepath=const.drive_filepath, filename=const.drive_sample, mimetype=const.file_type)
    upload.search_file(query=const.queue)

'''
    # TASK 4
    dataBase = ConnectSqlTable(db=const.dB_path)
    coll, row = dataBase.get_row_column(QUERY=const.DATA_QUERY)

    PF=PlotFigure(week=const.week_check, date_format=const.date_format, pic_format=const.pic_format)
    PF.figures(dt_coll=const.column_name[date], folder_name=const.fig, rows_name=row, columns_name=coll)

    save_doc(
        media=const.media,
        figure=const.fig,
        doc_name=const.doc_name,
        rows_name=row,
        columns_name=coll
    )"""
'''