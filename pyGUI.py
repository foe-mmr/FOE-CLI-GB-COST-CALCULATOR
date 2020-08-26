from mttkinter import *
import tktable

class PyGUI:
	def __init__(self, version):
		self.root = mtTkinter.Tk(className=version+' FOE CLI GB Calculator')
		self.root.geometry("250x350")

		self.version = version
		self.gbTitle = mtTkinter.StringVar()
		self.gbOwnerName = mtTkinter.StringVar()
		self.remainingFPs = mtTkinter.StringVar()
		self.investText = mtTkinter.StringVar()
		self.profitText = mtTkinter.StringVar()
		self.warningText = mtTkinter.StringVar()
		self.tableArray = tktable.ArrayVar(self.root)
		self.Table = tktable.Table(self.root,
					   state='disabled',
					   titlerows=1,
					   rows=6,
					   cols=3,
					   variable=self.tableArray,
					   flashmode='on')

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
		if field == "investText":
			self.investText.set(val)
		if field == "warningText":
			self.warningText.set(val)
		if field == "table":
			self.updateTable(val)
			

	def updateTable(self, val):
		columns = ['#','Cost','Difference']

		row_count=0
		col_count=0
		#SETTING COLUMNS
		for col in columns:
			index = "%i,%i" % (row_count,col_count)
			self.tableArray[index] = col
			col_count+=1
		row_count=1
		col_count=0
		#SETTING DATA IN ROWS
		for row in val:
			color = 'reset'
			for item in row:
				index = "%i,%i" % (row_count,col_count)
				## PLACING THE VALUE IN THE INDEX CELL POSITION ##
				self.tableArray[index] = item

				if item == "LOCKED":
					color = 'red'
				if col_count == 2 and isinstance(item, int) and int(item) > 0 and color == 'reset':
					color = 'green'
				if col_count == 1 and item == "SAFE":
					color = 'yellow'

				self.Table.tag_cell(color, "%i,%i" % (row_count,0))
				self.Table.tag_cell(color, "%i,%i" % (row_count,1))
				self.Table.tag_cell(color, "%i,%i" % (row_count,2))

				col_count+=1       
			col_count=0
			row_count+=1

	def createWindow(self):
		lb_gbTitle = mtTkinter.Label(self.root, textvariable=self.gbTitle)
		lb_gbTitle.pack(side='top', fill='x')

		lb_gbOwnerName = mtTkinter.Label(self.root, textvariable=self.gbOwnerName)
		lb_gbOwnerName.pack()

		values = [['1','-','-'],
				  ['2','-','-'],
				  ['3','-','-'],
				  ['4','-','-'],
				  ['5','-','-']]

		self.updateTable(values)
		self.Table.pack()

		self.Table.tag_configure('green', background='green')
		self.Table.tag_configure('reset', background='white')
		self.Table.tag_configure('red', background='red')
		self.Table.tag_configure('yellow', background='yellow')

		lb_remainingFPs = mtTkinter.Label(self.root, textvariable=self.remainingFPs)
		lb_remainingFPs.pack()

		lb_profitText = mtTkinter.Label(self.root, textvariable=self.profitText)
		lb_profitText.pack()

		lb_investText = mtTkinter.Label(self.root, textvariable=self.investText)
		lb_investText.pack()

		lb_warningText = mtTkinter.Label(self.root, textvariable=self.warningText, wraplength=240)
		lb_warningText.pack(side='bottom')
		
		self.gbTitle.set("")
		self.gbOwnerName.set("")
		self.remainingFPs.set("")
		self.profitText.set("")
		self.warningText.set("")