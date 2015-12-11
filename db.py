import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey

MYSQL_SERVER_DB = 'mysql://root:1@192.168.1.251/monitor'
engine = sqlalchemy.create_engine(MYSQL_SERVER_DB)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

def create_all():
    Base.metadata.create_all()
    
def drop_all():
    Base.metadata.drop_all()
    
class ClientInfo(Base):
    __tablename__ = 'client_info'
    
    id = Column(Integer, primary_key=True)
    identity = Column(String(32), nullable=False, unique=True) 
    name = Column(String(32), nullable=False)
    type = Column(Integer, nullable=False)
    ip_addr = Column(String(16), nullable=False)
    mac_addr = Column(String(20), nullable=False)
    status = Column(Integer, nullable=False)
    update_time = Column(DateTime, nullable=False)
    
    def __repr__(self):
        return '<ClientInfo(name=%s, ip_addr=%s, mac_addr=%s, status=%d, update_time=%s)>'  % (
                                        self.name, self.ip_addr, self.mac_addr, self.status, self.update_time)


class ClientUpdateHistory(Base):
    __tablename__ = 'client_update_history'
    
    id = Column(Integer, primary_key=True)
    ip_addr = Column(String(16), nullable=False)
    update_time = Column(DateTime)
    client_identity = Column(String(32), ForeignKey('client_info.identity'))
    
    client = relationship('ClientInfo', backref=backref('client_update_history', order_by=update_time))
    
    def __repr__(self):
        return '<ClientUpdateHistory(status=%d, update_tiem=%s)>' % (
                                                        self.status, self.update_time)

if __name__ == '__main__':
    print('Create tables')
    create_all()
    print('Create tables successfully')