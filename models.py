from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

from bot import BASE_DIR


engine = create_engine(f'sqlite:///{BASE_DIR}\\passwords.db')


BaseModel = declarative_base()


class LoginCredential(BaseModel):
    __tablename__ = 'login_credential'

    id = Column(Integer, primary_key=True)
    site_name = Column(String)
    account_login = Column(String)
    account_password = Column(String)

    def __repr__(self):
        return f'{self.__class__.__name__} {self.site_name}'


BaseModel.metadata.create_all(engine)


Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

