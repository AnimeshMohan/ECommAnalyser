from flask import Flask, render_template, request, redirect, url_for
from itertools import izip_longest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import DecBase, Sites, Categories, Items, Sales, Keycode

app = Flask(__name__,static_url_path = '/static')

engine = create_engine('sqlite:///ecommanalyser.db')
DecBase.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

finserial = 665
appendtext = 'new'
appendnum = 000

@app.route('/')
@app.route('/home')
def homePage():
	return render_template('index.html')

@app.route('/sites')
def sitesPage():
	return render_template('sites.html')

@app.route('/categories')
def categoriesPage():
	catdbm = session.execute("select cat_name from categories where c_id like \"cm%\"")
	catdbw = session.execute("select cat_name from categories where c_id like \"cw%\"")
	catdbf = session.execute("select cat_name from categories where c_id like \"cf%\"")
	catdbh = session.execute("select cat_name from categories where c_id like \"ch%\"")
	catdbg = session.execute("select cat_name from categories where c_id like \"cg%\"")
	catm = []
	catw = []
	catf = []
	cath = []
	catg = []
	for i in catdbm:
		i=str(i)
		i=i[3:-3]
		catm.append(i)
	catm.append(" ")
	for i in catdbw:
		i=str(i)
		i=i[3:-3]
		catw.append(i)
	for i in catdbf:
		i=str(i)
		i=i[3:-3]
		catf.append(i)
	catf.append(" ")
	for i in catdbh:
		i=str(i)
		i=i[3:-3]
		cath.append(i)
	cath.append(" ")
	cath.append(" ")
	cath.append(" ")
	for i in catdbg:
		i=str(i)
		i=i[3:-3]
		catg.append(i)
	catg.append(" ")
	catg.append(" ")
	return render_template('categories.html',categories=izip_longest(catm,catw,catf,cath,catg))

@app.route('/items')
def itemChoosePage():
	return render_template('items.html')

@app.route('/itemlist',methods=['GET','POST'])
def itemsPage():
	cat = session.execute("select * from categories")
	catlist = []
	elem = []
	for row in cat:
		elem.append(str(row.c_id))
		elem.append(str(row.cat_name))
		catlist.append(elem)
		elem = []

	site = session.execute("select * from sites")
	sitelist = []
	for row in site:
		elem.append(str(row.s_id))
		elem.append(str(row.site_name))
		sitelist.append(elem)
		elem = []

	if request.method=='POST':
		category = request.form['category']
		site = request.form['site']
		if category == "all" and site == "all":
			query_res=session.execute("select i.item_id,i.item_name,i.no_viewed,s.month,s.no_sold,s.no_stars from items i,sales s where i.item_id=s.item_id")
		elif category == "all" and site != "all":
			query_res=session.execute("select i.item_id,i.item_name,i.no_viewed,s.month,s.no_sold,s.no_stars from items i,sales s where i.item_id=s.item_id and i.s_id='"+site+"'")
		elif category != "all" and site == "all":
			query_res=session.execute("select i.item_id,i.item_name,i.no_viewed,s.month,s.no_sold,s.no_stars from items i,sales s where i.item_id=s.item_id and i.c_id='"+category+"'")
		else:
			query_res=session.execute("select i.item_id,i.item_name,i.no_viewed,s.month,s.no_sold,s.no_stars from items i,sales s where i.item_id=s.item_id and i.s_id='"+site+"' and i.c_id='"+category+"'")
		querylist = []
		elem = []
		for row in query_res:
			print row
			elem.append(str(row.item_id))
			elem.append(str(row.item_name))
			elem.append(str(row.no_viewed))
			elem.append(str(row.month))
			elem.append(str(row.no_sold))
			elem.append(str(row.no_stars))
			querylist.append(elem)
			elem = []
		print querylist
		return render_template('viewlist.html',queryresult=querylist)
	else:
		return render_template('itemlist.html',categories = catlist, sites= sitelist)

@app.route('/calculator',methods=['GET','POST'])
def calculatorPage():
	cat = session.execute("select * from categories")
	catlist = []
	elem = []
	for row in cat:
		elem.append(str(row.c_id))
		elem.append(str(row.cat_name))
		catlist.append(elem)
		elem = []

	site = session.execute("select * from sites")
	sitelist = []
	for row in site:
		elem.append(str(row.s_id))
		elem.append(str(row.site_name))
		sitelist.append(elem)
		elem = []

	if request.method=='POST':
		category = request.form['category']
		site = request.form['site']
		iid = request.form['iid']
		print site,category,iid
		query_res=session.execute("select i.item_id,i.item_name,avg(s.no_sold) as sold,avg(s.no_stars) as star from items i,sales s where i.item_id=s.item_id and i.item_id='"+iid+"' and i.s_id='"+site+"' and i.c_id='"+category+"'")
		querylist = []
		elem = []
		for row in query_res:
			print row
			elem.append(str(row.item_id))
			elem.append(str(row.item_name))
			elem.append(str(row.sold))
			elem.append(str(row.star))
			querylist.append(elem)
			elem = []
		print querylist
		return render_template('viewcalc.html',queryresult=querylist)
	else:
		return render_template('calculator.html',categories = catlist, sites= sitelist)

@app.route('/modify',methods=['GET','POST'])
def modifyPage():
	return render_template('modify.html')

@app.route('/insert',methods=['GET','POST'])
def insertPage():
	cat = session.execute("select * from categories")
	catlist = []
	elem = []
	for row in cat:
		elem.append(str(row.c_id))
		elem.append(str(row.cat_name))
		catlist.append(elem)
		elem = []

	site = session.execute("select * from sites")
	sitelist = []
	for row in site:
		elem.append(str(row.s_id))
		elem.append(str(row.site_name))
		sitelist.append(elem)
		elem = []

	if request.method=='POST':
		iid = request.form['iid']
		site = request.form['site']
		category = request.form['category']
		brand = request.form['brand']
		price = request.form['price']
		noviews = request.form['noviews']
		salesmar = request.form['salesmar']
		starsmar = request.form['starsmar']
		salesjun = request.form['salesjun']
		starsjun = request.form['starsjun']
		salessep = request.form['salessep']
		starssep = request.form['starssep']
		salesdec = request.form['salesdec']
		starsdec = request.form['starsdec']
		lastentry = session.query(Sales).order_by(Sales.serial_num.desc()).first()
		lastnum = lastentry.serial_num
		session.execute("insert into items values ('"+iid+"','"+brand+"','"+site+"','"+category+"',"+price+","+noviews+")")
		lastnum = lastnum+1
		session.execute("insert into sales values ('"+site+"','"+category+"','"+iid+"','March',"+str(int(salesmar))+","+str(round(float(starsmar),2))+","+str(int(lastnum))+")")
		lastnum = lastnum+1
		session.execute("insert into sales values ('"+site+"','"+category+"','"+iid+"','June',"+str(int(salesjun))+","+str(round(float(starsjun),2))+","+str(int(lastnum))+")")
		lastnum = lastnum+1
		session.execute("insert into sales values ('"+site+"','"+category+"','"+iid+"','September',"+str(int(salessep))+","+str(round(float(starssep),2))+","+str(int(lastnum))+")")
		lastnum = lastnum+1
		session.execute("insert into sales values ('"+site+"','"+category+"','"+iid+"','December',"+str(int(salesdec))+","+str(round(float(starsdec),2))+","+str(int(lastnum))+")")
		session.commit()
		return redirect('/itemlist')
	else:
		return render_template('insert.html',categories = catlist, sites= sitelist)

@app.route('/delete',methods=['GET','POST'])
def deletePage():
	cat = session.execute("select * from categories")
	catlist = []
	elem = []
	for row in cat:
		elem.append(str(row.c_id))
		elem.append(str(row.cat_name))
		catlist.append(elem)
		elem = []

	site = session.execute("select * from sites")
	sitelist = []
	for row in site:
		elem.append(str(row.s_id))
		elem.append(str(row.site_name))
		sitelist.append(elem)
		elem = []

	if request.method=='POST':
		iid = request.form['item']
		category = request.form['category']
		site = request.form['site']
		print iid,category,site
		session.execute("delete from items where item_id ='"+iid+"'")
		session.commit()
		return redirect('/itemlist')
	else:
		return render_template('delete.html',categories = catlist, sites= sitelist)

@app.route('/update',methods=['GET','POST'])
def updatePage():
	cat = session.execute("select * from categories")
	catlist = []
	elem = []
	for row in cat:
		elem.append(str(row.c_id))
		elem.append(str(row.cat_name))
		catlist.append(elem)
		elem = []

	sit = session.execute("select * from sites")
	sitelist = []
	for row in sit:
		elem.append(str(row.s_id))
		elem.append(str(row.site_name))
		sitelist.append(elem)
		elem = []

	if request.method=='POST':
		iid = request.form['itemid']
		data = request.form['data']
		attribute = request.form['attribute']
		category = request.form['category']
		site = request.form['site']

		if attribute == "star_mar":
			month = "March"
			flag = 1
		elif attribute == "star_jun":
			month = "June"
			flag = 1
		elif attribute == "star_sep":
			month = "September"
			flag = 1
		elif attribute == "star_dec":
			month = "December"
			flag = 1
		elif attribute == "sales_mar":
			month = "March"
			flag = 2
		elif attribute == "sales_jun":
			month = "June"
			flag = 2
		elif attribute == "sales_sep":
			month = "September"
			flag = 2
		elif attribute == "sales_dec":
			month = "December"
			flag = 2
		else:
			flag = 3

		if flag == 1:
			session.execute("update sales set no_stars = "+str(round(float(data),2))+" where month='"+month+"' and item_id='"+iid+"' and s_id='"+site+"' and c_id='"+category+"'")
		if flag == 2:
			session.execute("update sales set no_sold = "+str(int(data))+" where month='"+month+"' and item_id='"+iid+"' and s_id='"+site+"' and c_id='"+category+"'")
		if flag == 3:
			if attribute == "price":
				session.execute("update items set price = "+str(int(data))+" where item_id='"+iid+"' and s_id='"+site+"' and c_id='"+category+"'")
			if attribute == "no_viewed":
				session.execute("update items set no_viewed = "+str(int(data))+" where item_id='"+iid+"' and s_id='"+site+"' and c_id='"+category+"'")
		session.commit()
		print iid,data,attribute,category,site
		return redirect('/itemlist')
	else:
		return render_template('update.html',categories = catlist, sites= sitelist)

@app.route('/keys',methods=['GET','POST'])
def keysPage():
	cat = session.execute("select * from categories")
	catlist = []
	elem = []
	for row in cat:
		elem.append(str(row.c_id))
		elem.append(str(row.cat_name))
		catlist.append(elem)
		elem = []

	sit = session.execute("select * from sites")
	sitelist = []
	for row in sit:
		elem.append(str(row.s_id))
		elem.append(str(row.site_name))
		sitelist.append(elem)
		elem = []

	if request.method=='POST':
		category = request.form['category']
		site = request.form['site']
		posskey = session.execute("select gen_id from keycode where s_id = '"+site+"' and c_id = '"+category+"'")
		posskeylist = []
		for i in posskey:
			i = str(i)
			i = i[3:-3]
			posskeylist.append(i)
		print posskeylist
		for row in posskeylist:
			keylist = session.execute("select item_id from items where item_id like \""+i+"%\"")
		keyslist = []
		for i in keylist:
			i=str(i)
			i=i[3:-3]
			keyslist.append(i)
		print keyslist

		return render_template('keyliist.html',keyslist=keyslist,posskeylist=posskeylist)
	else:
		return render_template('keys.html',categories = catlist, sites= sitelist)

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)