import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from modelHW import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = ''
engine = sq.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

pub1 = session.query(Publisher).filter_by(name='Пушкин').first()
if not pub1:
    pub1 = Publisher(name="Пушкин")
    session.add(pub1)
    session.commit()
print(pub1)

b1 = Book(title='Капитанская дочка', publisher=pub1)
b2 = Book(title='Руслан и Людмила', publisher=pub1)
b3 = Book(title='Евгений Онегин', publisher=pub1)
session.add_all([b1, b2, b3])
session.commit()

s1 = session.query(Shop).filter_by(name='Буквоед').first()
if not s1:
    s1 = Publisher(name="Буквоед")
    session.add(s1)
    session.commit()
s2 = session.query(Shop).filter_by(name='Лабиринт').first()
if not s2:
    s2 = Publisher(name="Лабиринт")
    session.add(s2)
    session.commit()
s3 = session.query(Shop).filter_by(name='Книжный дом').first()
if not s3:
    s3 = Publisher(name="Книжный дом")
    session.add(s3)
    session.commit()
session.add_all([s1, s2, s3])
session.commit()

st1 = Stock(book=b1, shop=s1, count=50)
st2 = Stock(book=b2, shop=s2, count=50)
st3 = Stock(book=b3, shop=s3, count=50)
session.add_all([st1, st2, st3])
session.commit()

date = datetime.date(datetime.now())
sal1 = Sale(price=600, date_sale=date,  stock=st1, count=10)
sal2 = Sale(price=500, date_sale=date,  stock=st2, count=10)
sal3 = Sale(price=400, date_sale=date, stock=st3, count=10)
session.add_all([sal1, sal2, sal3])
session.commit()


p = session.query(Publisher).filter(sq.or_(Publisher.id==x, Publisher.name==x)).all()[0]
sales = session.query(Sale).join(Stock).join(Shop).join(Book).filter(Book.publisher==p).subquery('t')
shops = session.query(Shop).join(Stock).join(Sale).filter(Sale.id==sales.c.id)
for i in shops:
    print(i)

session.close()
