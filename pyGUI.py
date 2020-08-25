from mttkinter import *
import tktable

class PyGUI:
	def __init__(self, version):
		print "INIT"
		self.root = mtTkinter.Tk(className='FOE CLI GB Calculator '+version)
		self.root.geometry("200x200")

		self.version = version
		self.gbTitle = mtTkinter.StringVar()
		self.gbOwnerName = mtTkinter.StringVar()
		self.remainingFPs = mtTkinter.StringVar()
		self.profitText = mtTkinter.StringVar()
		self.warningText = mtTkinter.StringVar()
		self.table = tktable.ArrayVar(self.root)

		self.createWindow()

	def updateVal(self, field, val):
		if field == "gbTitle":
			self.gbTitle.set(val.encode('utf8'))
		if field == "gbOwnerName":
			self.gbOwnerName.set(val.encode('utf8'))
		if field == "remainingFPs":
			self.remainingFPs.set(val)
		if field == "profitText":
			self.profitText.set(val)
		if field == "warningText":
			self.warningText.set(val)
		if field == "table":

			columns = ['#','Cost','Difference']
			'''
			values = [['1','-','-'],
					  ['2','-','-'],
					  ['3','-','-'],
					  ['4','-','-'],
					  ['5','-','-']]
			'''

			row_count=0
			col_count=0
			#SETTING COLUMNS
			for col in columns:
				index = "%i,%i" % (row_count,col_count)
				self.table[index] = col
				col_count+=1
			row_count=1
			col_count=0
			#SETTING DATA IN ROWS
			for row in val:
				for item in row:
					index = "%i,%i" % (row_count,col_count)
					## PLACING THE VALUE IN THE INDEX CELL POSITION ##
					self.table[index] = item
					col_count+=1       
				col_count=0
				row_count+=1

	def createTable(self):
		columns = ['#','Cost','Difference']
		values = [['1','-','-'],
				  ['2','-','-'],
				  ['3','-','-'],
				  ['4','-','-'],
				  ['5','-','-']]

		row_count=0
		col_count=0
		#SETTING COLUMNS
		for col in columns:
			index = "%i,%i" % (row_count,col_count)
			self.table[index] = col
			col_count+=1
		row_count=1
		col_count=0
		#SETTING DATA IN ROWS
		for row in values:
			for item in row:
				index = "%i,%i" % (row_count,col_count)
				## PLACING THE VALUE IN THE INDEX CELL POSITION ##
				self.table[index] = item
				col_count+=1       
			col_count=0
			row_count+=1

		test = tktable.Table(self.root,
					   state='disabled',
					   titlerows=1,
					   rows=6,
					   cols=3,
					   variable=self.table,
					   flashmode='on')

		test.pack()


	def createWindow(self):
		lb_gbTitle = mtTkinter.Label(self.root, textvariable=self.gbTitle)
		lb_gbTitle.pack(side='top', fill='x')

		lb_gbOwnerName = mtTkinter.Label(self.root, textvariable=self.gbOwnerName)
		lb_gbOwnerName.pack()

		self.createTable()

		lb_remainingFPs = mtTkinter.Label(self.root, textvariable=self.remainingFPs)
		lb_remainingFPs.pack()

		lb_profitText = mtTkinter.Label(self.root, textvariable=self.profitText)
		lb_profitText.pack()

		lb_warningText = mtTkinter.Label(self.root, textvariable=self.warningText)
		lb_warningText.pack(side='bottom', fill='x')
		
		self.gbTitle.set("?")
		self.gbOwnerName.set("?")
		self.remainingFPs.set("?")
		self.profitText.set("?")
		self.warningText.set("?")