from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///server_db_1.db', echo=True)

Base = declarative_base()


class TwitterTable(Base):
    __tablename__ = 'twitter_table'
    # twit info
    Id = Column(Integer, primary_key=True)
    Created_at = Column(String)
    Added_at = Column(DateTime, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow())
    # user info
    Id_user = Column(Integer)  # ['user']['id']
    Username = Column(String)  # ['user']["screen_name"]
    Location = Column(String, nullable=True)  # ['user']['location']
    Text = Column(String)  # ['extended_tweet']['full_text']
    Hashtags = Column(String)  # ['extended_tweet']['entities']['hashtags']
    Retweet_count = Column(Integer)
    # sentiment info
    Polarity = Column(Integer)
    Subjectivity = Column(Integer)

    def __repr__(self):
        return "<twitter_table( " \
               "Id = {}," \
               "Created_at = {}, " \
               "Added_at = {}, " \
               "Id_user = {}, " \
               "Username = {}, " \
               "Location = {}, " \
               "Text = {}, " \
               "Hashtags = {}," \
               "Retweet_count = {}," \
               "Polarity = {}," \
               "Subjectivity = {})>".format(
            self.id,
            self.created_at,
            self.fetched_at,
            self.id_user,
            self.screen_name,
            self.location,
            self.full_text,
            self.hashtags,
            self.retweet_count,
            self.polarity,
            self.subjectitivity
        )

# create tables
def db_init():
    Base.metadata.create_all(engine)
# from df_setup import engine, Base, db_init


# for checking existing table and columns
# from sqlalchemy import MetaData
from sqlalchemy import MetaData
m = MetaData()
m.reflect(engine)
for table in m.tables.values():
    print(table.name)
    for column in table.c:
        print(column.name)


