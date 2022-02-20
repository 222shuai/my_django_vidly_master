import pymysql

# 要使用mysql需要调用pymysql，但django默认使用的是MySQLdb，该模块已经很久没更新了，
# 因此可以使用以下方法让django以为是用了MySQLdb
pymysql.install_as_MySQLdb()  # 让django以为是用了MySQLdb