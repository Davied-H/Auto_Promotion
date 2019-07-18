from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey  # 区分大小写
from sqlalchemy.orm import sessionmaker
import configparser

cf = configparser.ConfigParser()
cf.read("conf/app.config")
# 创建连接
db_path = 'sqlite:///data/{}'.format(cf.get("default","db_name"))
engine = create_engine(db_path)

# 生成orm基类
base = declarative_base()


# 表映射
class Promotion(base):
    __tablename__ = 'promotion'  # 表名
    id = Column(Integer, primary_key=True)
    commodity_id = Column(String(32))  # 商品id
    message_text = Column(String(100))  # 消息文本
    picture_path = Column(String(30), default="")  # 图片路径
    coupon_begin_time = Column(String(30))  # 优惠券开始时间
    coupon_end_time = Column(String(30))  # 优惠券结束时间


base.metadata.create_all(engine)  # 创建表结构
Session_class = sessionmaker(bind=engine)  # 创建与数据库的会话，class,不是实例
DB = Session_class()  # 生成session实例




#
#
# class SqliteDb:
#     def __init__(self, db_name="default.db"):
#         self.db_name = db_name
#         self.db = sqlite3.connect(self.db_name)
#         try:
#             self.db.execute(
#                 "create table promotion (id integer primary key,message varchar(50) ,picture_path varchar(100) )")
#             self.result = True
#         except sqlite3.OperationalError:
#             self.result = False
#
#     def insert(self, table=None, value=None):
#         if table:
#             if value:
#                 self.db.execute("insert into {} values (?,?,?)".format(table), value)
#                 self.db.commit()
#
#     def close(self):
#         self.db.close()
#
#
# if __name__ == "__main__":
#     aaa = SqliteDb(db_name="../data/default.db")
#     aaa.close()
