import sys
from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

DecBase = declarative_base()

class Sites(DecBase):

	__tablename__='sites'

	s_id = Column(String(5), primary_key=True, nullable=False)
	site_name = Column(String(10), nullable=False)

class Categories(DecBase):

	__tablename__='categories'

	c_id = Column(String(5), primary_key=True, nullable=False)
	cat_name = Column(String(25), nullable=False)

class Items(DecBase):

	__tablename__='items'

	item_id = Column(String(6), primary_key=True, nullable=False)
	item_name = Column(String(25), nullable=False)
	s_id = Column(String(5), ForeignKey('sites.s_id'), primary_key=True, nullable=False)
	c_id = Column(String(5), ForeignKey('categories.c_id'), primary_key=True, nullable=False)
	price = Column(Integer)
	no_viewed = Column(Integer)
	sites = relationship(Sites)
	categories = relationship(Categories)

class Sales(DecBase):

	__tablename__='sales'

	s_id = Column(String(5), ForeignKey('sites.s_id'), primary_key=True, nullable=False)
	c_id = Column(String(5), ForeignKey('categories.c_id'), primary_key=True, nullable=False)
	item_id = Column(String(6), ForeignKey('items.item_id'), primary_key=True, nullable=False)
	month = Column(String(10), nullable=False)
	no_sold = Column(Integer)
	no_stars = Column(Float)
	serial_num = Column(Integer, primary_key=True)
	sites = relationship(Sites)
	categories = relationship(Categories)
	items = relationship(Items)
	 
class Keycode(DecBase):

	__tablename__='keycode'

	s_id = Column(String(5),  ForeignKey('sites.s_id'), primary_key=True, nullable=False)
	c_id = Column(String(5),  ForeignKey('categories.c_id'), primary_key=True, nullable=False)
	gen_id = Column(String(4), primary_key=True, nullable=False)
	sites = relationship(Sites)
	categories = relationship(Categories)


engine = create_engine('sqlite:///ecommanalyser.db')
DecBase.metadata.create_all(engine)
