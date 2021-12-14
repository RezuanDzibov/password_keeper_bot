from models import engine, LoginCredential, session
from sqlalchemy import select, delete


class Database:

    def __init__(self):
        self._session = session

    def insert_row(self, site_name: str, account_login: str, account_password: str):
        login_credentials = LoginCredential(
            site_name=site_name,
            account_login=account_login,
            account_password=account_password
        )
        self._session.add(login_credentials)
        self._session.commit()

    def get_site_names(self):
        rows = self._session.query(LoginCredential.site_name).all()
        return rows

    def get_row(self, site_id: int):
        statement = select(LoginCredential).where(LoginCredential.id == site_id)
        row = [row for row in self._session.execute(statement=statement).scalars()][0]
        return row

    def delete_row(self, site_id: int):
        self._session.query(LoginCredential).filter(LoginCredential.id == site_id).delete()
        session.commit()