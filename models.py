import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class User_vk(Base):
    __tablename__ = 'user_vk'

    user_vk_id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=20))
    surname = sq.Column(sq.String(length=20))


class Partners(Base):
    __tablename__ = 'partners'

    partner_vk_id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=20))
    surname = sq.Column(sq.String(length=20))
    profile_link = sq.Column(sq.String, nullable=False)

    def info(self):
        return [self.name, self.surname, self.profile_link]


class Black_list(Base):
    __tablename__ = 'black_list'

    user_vk_id = sq.Column(sq.Integer, sq.ForeignKey('user_vk.user_vk_id', ondelete='CASCADE'), nullable=False)
    partner_vk_id = sq.Column(sq.Integer, sq.ForeignKey('partners.partner_vk_id', ondelete='CASCADE'),
                              nullable=False)
    User_vk = relationship(User_vk, backref='Black_list')
    Partners_list = relationship(Partners, backref='Black_list')

    __table_args__ = (
        sq.PrimaryKeyConstraint(
            partner_vk_id,
            user_vk_id),
        {})

    def __str__(self):
        return f'Black_list: (USER_VK_ID: {self.user_vk_id}, PARTNER_VK_ID: {self.partner_vk_id})'

    def info(self):
        return self.partner_vk_id


class Favorite_partners(Base):
    __tablename__ = 'favorite_partners'

    user_vk_id = sq.Column(sq.Integer, sq.ForeignKey('user_vk.user_vk_id', ondelete='CASCADE'), nullable=False)
    partner_vk_id = sq.Column(sq.Integer, sq.ForeignKey('partners.partner_vk_id', ondelete='CASCADE'), nullable=False)
    user_vk = relationship(User_vk, backref='Favorite_partners')
    partners = relationship(Partners, backref='Favorite_partners')

    __table_args__ = (
        sq.PrimaryKeyConstraint(
            partner_vk_id,
            user_vk_id),
        {})

    def __str__(self):
        return f'Favorite_partners: (USER_VK_ID: {self.user_vk_id}, PARTNER_VK_ID: {self.partner_vk_id})'

    def info(self):
        return self.partner_vk_id


def create_tables():
    engine = sq.create_engine('postgresql://postgres:123456@localhost:5432/vk_base')
    Base.metadata.drop_all(engine)  # ----удаляет все существующие таблицы перед созданием---
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=create_tables)
    session = Session()
    session.close()
