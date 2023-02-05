# Importing all the required libraries
import const as CONST
from photoImport import Credential
from anjan_task import ConnectSqlTable, PlotFigure,  WordFile

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # TASK 3
    upload = Credential(
        google_cred=CONST.google_cred,
        app_name=CONST.app_name,
        client_secret=CONST.cred,
        scope=CONST.scope
    )
    upload.listFiles(size=CONST.page_size)
    upload.download_file(real_file_id=CONST.real_file_id, filepath=CONST.drive_filepath)
    upload.resize_image(img_path=CONST.drive_filepath, date_format=CONST.date_format, max_size=CONST.pixel_size)
    upload.create_folder(filepath=CONST.drive_filepath)
    upload.uploadFile(filepath=CONST.drive_filepath, filename=CONST.drive_sample, mimetype=CONST.file_type)
    upload.search_file(query=CONST.queue)


    # TASK 4
    SQL = ConnectSqlTable(db=CONST.dB_path)
    coll, row = SQL.get_row_column(QUERY=CONST.DATA_QUERY)

    PF = PlotFigure(week=CONST.week_check, date_format=CONST.date_format, pic_format=CONST.pic_format)
    PF.figures(dt_coll=CONST.date, folder_name=CONST.fig, rows_name=row, columns_name=coll)

    # TASK 5

    save_doc = WordFile(media_path=CONST.media, figure_path=CONST.fig,
                        date_format=CONST.date_format, pic_format=CONST.pic_format)
    predict_column, predict_row = SQL.get_row_column(QUERY=CONST.PREDICT_QUERY)
    save_doc.saveFile(rows_name=row, columns_name=coll,
                      columns_predict=predict_column, row_predict=predict_row,
                      doc_name=CONST.doc_name, dt_coll=CONST.date, data=CONST)
