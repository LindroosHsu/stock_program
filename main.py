#!/usr/bin/env python
#-*-coding: utf-8-*-

'''
**********************************
This is a little stock program.

Author: Lindroos Xu
E-mail: somewhereibeing@gmail.com
Version: 0.1.0 (Stable)

All data extracted from "http://www.cathaysec.com.tw/".

This program provides the river figure and
determine the amount of the three main traded

**********************************
'''

import wx
import re
import urllib
import urllib2
import pylab

class MyFrame(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title)
		
		menuBar = wx.MenuBar()
		menu1 = wx.Menu()
		menu1.Append(101, "&About")
		menu1.AppendSeparator()
		menu1.Append(102, "&Close")
		menuBar.Append(menu1, "&Help")
		self.SetMenuBar(menuBar)
		self.SetIcon(wx.Icon("key.png", wx.BITMAP_TYPE_ANY))
		
		verSizer = wx.BoxSizer(wx.VERTICAL)
		threeComHorSizer = wx.BoxSizer(wx.HORIZONTAL)
		scHorSizer = wx.BoxSizer(wx.HORIZONTAL)
		mainVerSizer = wx.BoxSizer(wx.VERTICAL)
		selfVerSizer = wx.BoxSizer(wx.VERTICAL)
		JPVerSizer = wx.BoxSizer(wx.VERTICAL)
		
		#----Stock Code----
		scLabel = wx.StaticText(self, -1, u"股票代號: ")
		self.scText = wx.TextCtrl(self, -1, size=(100,-1))
		self.scText.SetMaxLength(4)
		self.scText.SetInsertionPoint(0)
		scHorSizer.Add(scLabel)
		scHorSizer.Add(self.scText)
		scButton = wx.Button(self, -1, u"畫河流圖")
		scHorSizer.Add(scButton)
		#------------------
		
		#----main buy and sell----
		mainList = [u'一日', u'五日']
		mainLabel = wx.StaticText(self, -1, u"主力買賣: ")
		self.mainChoice = wx.Choice(self, -1, choices=mainList)
		mainVerSizer.Add(mainLabel)
		mainVerSizer.Add(self.mainChoice)
		#-------------------------
		
		#----self buy and sell----
		selfList = [u'一日', u'五日']
		selfLabel = wx.StaticText(self, -1, u"自營買賣: ")
		self.selfChoice = wx.Choice(self, -1, choices=selfList)
		selfVerSizer.Add(selfLabel)
		selfVerSizer.Add(self.selfChoice)
		#-------------------------
		
		#----JP buy and sell----
		JPList = [u'一日', u'五日', u'十日', u'二十日', u'六十日']
		JPLabel = wx.StaticText(self, -1, u"投信買賣: ")
		self.JPChoice = wx.Choice(self, -1, choices=JPList)
		JPVerSizer.Add(JPLabel)
		JPVerSizer.Add(self.JPChoice)
		#-----------------------
		
		#----foreign buy and sell----
		#----------------------------
		
		button = wx.Button(self, -1, u"設定主力, 自營, 投信的判斷和搜尋\n(請三個日期都要選擇)")
		self.textCtrl = wx.TextCtrl(self, -1, size=(250, 250), style=wx.TE_READONLY|wx.TE_MULTILINE)
		self.textCtrl.SetInsertionPoint(0)
		clearButton = wx.Button(self, -1, u"清除")
				
		#----add into sizer----
		verSizer.AddSizer(scHorSizer, flag=wx.ALIGN_CENTER)
		threeComHorSizer.AddSizer(mainVerSizer)
		threeComHorSizer.AddSizer(selfVerSizer)
		threeComHorSizer.AddSizer(JPVerSizer)
		verSizer.AddSizer(threeComHorSizer, flag=wx.ALIGN_CENTER)
		verSizer.Add(button, flag=wx.EXPAND)
		verSizer.Add(self.textCtrl, flag=wx.ALIGN_CENTER)
		verSizer.Add(clearButton, flag=wx.ALIGN_CENTER)
		
		self.SetSizer(verSizer)
		self.Fit()
		#----------------------
		
		self.Bind(wx.EVT_MENU, self.OnAbout, id=101)
		self.Bind(wx.EVT_MENU, self.OnClose, id=102)
		self.Bind(wx.EVT_BUTTON, self.scButtonClicked, scButton)
		self.Bind(wx.EVT_BUTTON, self.ButtonClicked, button)
		self.Bind(wx.EVT_BUTTON, self.clearButtonClicked, clearButton)
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

#--------------------------------------------------------------------------------------------#

	def OnDrow(self, date, closePrice):
	
		sum, arDate, x = 0, 72, []
		average, tAR1, tAR2, tAR3, tAR4, bAR1, bAR2, bAR3, bAR4 = [], [], [], [], [], [], [], [], []

		for i in range(0, len(date)): x.append(i)
			
		for i in range(0, arDate-1):
			average.append(None)
			tAR1.append(None)
			tAR2.append(None)
			tAR3.append(None)
			tAR4.append(None)
			bAR1.append(None)
			bAR2.append(None)
			bAR3.append(None)
			bAR4.append(None)
		
		try:
			for i in range(0, len(closePrice)):
				try:
					for j in range(i, i+arDate):
						sum += closePrice[j]
				except:
					break;
				average.append(sum/arDate)
				sum = 0
			
			for i in range(arDate, len(average)):
				tAR1.append(average[i]*1.2)
				tAR2.append(average[i]*1.15)
				tAR3.append(average[i]*1.1)
				tAR4.append(average[i]*1.05)
				bAR1.append(average[i]*0.95)
				bAR2.append(average[i]*0.9)
				bAR3.append(average[i]*0.85)
				bAR4.append(average[i]*0.8)
			
			pylab.plot(average)
			pylab.plot(x, closePrice)
			pylab.plot(tAR1)
			pylab.plot(tAR2)
			pylab.plot(tAR3)
			pylab.plot(tAR4)
			pylab.plot(bAR1)
			pylab.plot(bAR2)
			pylab.plot(bAR3)
			pylab.plot(bAR4)
			
			pylab.xticks(x[0::40], date[0::40], rotation=17)
			pylab.grid(True)
			pylab.show()
		
		except:
			self.scText.Clear()

#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
	
	def scButtonClicked(self, event):
	
		if not self.scText.IsEmpty():
			date, closePrice = self.GetStockPrice()
			self.OnDrow(date, closePrice)
		else:
			box=wx.MessageDialog(None, u"請輸入股票代號", "ERROR", style=wx.CANCEL)
			box.ShowModal()
			box.Destroy()

#--------------------------------------------------------------------------------------------#		
#--------------------------------------------------------------------------------------------#

	def ButtonClicked(self, event):
	
		try:
			mainData, selfData, JPData = self.GetThreeCom()
			mainConditions = self.Ask(u'主力')
			selfConditions = self.Ask(u'自營')
			JPConditions = self.Ask(u'投信')
			mainResult, selfResult, JPResult = [], [], []
		
			try:		
			#----main consider----
				for condition in mainConditions:
					if condition.endswith('Buy', 0, 3):
						mainResult.append(self.ConsiderConditions(condition, mainData, 'Buy'))
					else:
						mainResult.append(self.ConsiderConditions(condition, mainData, 'Sell'))
			#---------------------
		
			#----self consider----
				for condition in selfConditions:
					if condition.endswith('Buy', 0, 3):
						selfResult.append(self.ConsiderConditions(condition, selfData, 'Buy'))
					else:
						selfResult.append(self.ConsiderConditions(condition, selfData, 'Sell'))
			#---------------------
		
			#----JP consider----
				for condition in JPConditions:
					if condition.endswith('Buy', 0, 3):
						JPResult.append(self.ConsiderConditions(condition, JPData, 'Buy'))
					else:
						JPResult.append(self.ConsiderConditions(condition, JPData, 'Sell'))
			#-------------------
			except:
				box=wx.MessageDialog(None, u"設定的條件有錯誤", "ERROR", style=wx.CANCEL)
				box.ShowModal()
				box.Destroy()
			
			for i in range(0, len(mainResult)):
				self.textCtrl.WriteText(u"主力第"+str(i+1)+u"個條件符合的股票代碼: "+str(mainResult[i])+"\n")
			for i in range(0, len(selfResult)):
				self.textCtrl.WriteText(u"自營第"+str(i+1)+u"個條件符合的股票代碼: "+str(selfResult[i])+"\n")
			for i in range(0, len(JPResult)):
				self.textCtrl.WriteText(u"投信第"+str(i+1)+u"個條件符合的股票代碼: "+str(JPResult[i])+"\n")
			self.textCtrl.WriteText("-----------------------------------------------")
		
		except:
			pass
		
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#

	def ConsiderConditions(self, condition, data, BorS):
	
		if BorS == 'Buy':
			which = 'buy'
		else:
			which = 'sell'		
		result = []
		
		if condition[len(BorS):(len(BorS))+1] == '>':
			number = condition[(condition.find('>'))+1:]
			for i in data:
				try:
					if int(data[i][which]) > int(number):
						result.append(i)
				except:
					pass
				
		elif condition[len(BorS):(len(BorS))+1] == '<':
			number = condition[(condition.find('<'))+1:]
			for i in data:
				try:
					if int(data[i][which]) < int(number):
						result.append(i)
				except:
					pass
					
		else:
			number1 = condition[len(BorS):condition.find('~')]
			number2 = condition[(condition.find('~'))+1:]
			if int(number1) > int(number2):
				temp = number1
				number1 = number2
				number2 = temp
			
			for i in data:
				try:
					if int(data[i][which]) > int(number1) and int(data[i][which]) < int(number2):
						result.append(i)
				except:
					pass
		
		return result
		
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#

	def Ask(self, choice):
	
		#i made all users stupid...
		i = 0
		conditions = []
		while True:
			BSDialog = wx.SingleChoiceDialog(None, u"這是'"+choice+u"'第'"+str(i+1)+u"'個條件, 請選擇買量 or 賣量"
			, "Choice", ['Buy', 'Sell'])
			
			if BSDialog.ShowModal() == wx.ID_OK:
				cDialog = wx.SingleChoiceDialog(None, u"這是'"+choice+u"'第'"+str(i+1)+u"'個條件, 請選擇大於 or 之間 or 小於"
				, "Choice", ['>', '~', '<'])
			
				if cDialog.ShowModal() == wx.ID_OK:
					if cDialog.GetSelection() == 1:
						tDialog1 = wx.TextEntryDialog(None, u"這是'"+choice+u"'第'"+str(i+1)+u"'個條件, 請輸入'多少'"+cDialog.GetStringSelection()+u"？"
						, "Text Entry", "100", style=wx.OK|wx.CANCEL)
						tDialog2 = wx.TextEntryDialog(None, u"這是'"+choice+u"'第'"+str(i+1)+u"'個條件, 請輸入"+cDialog.GetStringSelection()+u"'多少'？"
						, "Text Entry", "100", style=wx.OK|wx.CANCEL)
					
						if tDialog1.ShowModal() == wx.ID_OK and tDialog2.ShowModal() == wx.ID_OK:
							conditions.append(BSDialog.GetStringSelection()+tDialog1.GetValue()+cDialog.GetStringSelection()+tDialog2.GetValue())
							BSDialog.Destroy()
							cDialog.Destroy()
							tDialog1.Destroy()
							tDialog2.Destroy()
							checkDialog = wx.MessageDialog(None, u"請問還需要更多條件嗎？", "Ask", style=wx.OK|wx.CANCEL)
							if checkDialog.ShowModal() == wx.ID_OK:
								checkDialog.Destroy()
								i+=1
							else:
								checkDialog.Destroy()
								break
						else:
							BSDialog.Destroy()
							cDialog.Destroy()
							tDialog1.Destroy()
							tDialog2.Destroy()
							break					
					else:
						tDialog = wx.TextEntryDialog(None, u"這是'"+choice+u"'第'"+str(i+1)+u"'個條件, 請輸入"+cDialog.GetStringSelection()+u"多少？"
						, "Text Entry", "100", style=wx.OK|wx.CANCEL)
			
						if tDialog.ShowModal() == wx.ID_OK:
							conditions.append(BSDialog.GetStringSelection()+cDialog.GetStringSelection()+tDialog.GetValue())
							BSDialog.Destroy()
							cDialog.Destroy()
							tDialog.Destroy()
							checkDialog = wx.MessageDialog(None, u"請問還需要更多條件嗎？", "Ask", style=wx.OK|wx.CANCEL)
							if checkDialog.ShowModal() == wx.ID_OK:
								checkDialog.Destroy()
								i+=1
							else:
								checkDialog.Destroy()
								break
						else:
							BSDialog.Destroy()
							cDialog.Destroy()
							tDialog.Destroy()
							break
				else:
					BSDialog.Destroy()
					cDialog.Destroy()
					break
			else:
				BSDialog.Destroy()
				break

		return conditions

#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#

	def GetThreeCom(self):
		
		try:
			url = "http://cathaysec.megatime.com.tw/asp/market/ranktop.asp"
			mainValues, selfValues, JPValues = {}, {}, {}
		
			#----main----
			if self.mainChoice.GetCurrentSelection() != -1:
				mainValues['m'] = 'mainbuysell'
				if self.mainChoice.GetCurrentSelection() == 0:
					mainValues['d'] = '1'
				elif self.mainChoice.GetCurrentSelection() == 1:
					mainValues['d'] = '5'

				mainData = urllib.urlencode(mainValues)
				mainReq = urllib2.Request(url, mainData)
				mainPage = urllib2.urlopen(mainReq).read()
				mainData = self.GetThreeComParser(mainPage, 1)
			else:
				del mainData
			#------------
			
			#----self----
			if self.selfChoice.GetCurrentSelection() != -1:
				selfValues['m'] = 'selfbuysell'
				if self.selfChoice.GetCurrentSelection() == 0:
					selfValues['d'] = '1'
				elif self.selfChoice.GetCurrentSelection() == 1:
					selfValues['d'] = '5'
			
				selfData = urllib.urlencode(selfValues)
				selfReq = urllib2.Request(url, selfData)
				selfPage = urllib2.urlopen(selfReq).read()
				selfData = self.GetThreeComParser(selfPage, 2)
			else:
				del selfData
			#------------
		
			#----JP----
			if self.JPChoice.GetCurrentSelection() != -1:
				JPValues['m'] = 'jpbuysell'
				if self.JPChoice.GetCurrentSelection() == 0:
					JPValues['d'] = '1'
				elif self.JPChoice.GetCurrentSelection() == 1:
					JPValues['d'] = '5'
				elif self.JPChoice.GetCurrentSelection() == 2:
					JPValues['d'] = '10'
				elif self.JPChoice.GetCurrentSelection() == 3:
					JPValues['d'] = '20'
				elif self.JPChoice.GetCurrentSelection() == 4:
					JPValues['d'] = '60'
			
				JPData = urllib.urlencode(JPValues)
				JPReq = urllib2.Request(url, JPData)
				JPPage = urllib2.urlopen(JPReq).read()
				JPData = self.GetThreeComParser(JPPage, 3)
			else:
				del JPData
			#----------
			return mainData, selfData, JPData
		
		except:
			box=wx.MessageDialog(None, u"網頁忙碌, 請稍候在試", "ERROR", style=wx.CANCEL)
			box.ShowModal()
			box.Destroy()
			return None

#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#

	def GetThreeComParser(self, page, whichOne):
		
		if whichOne == 3:
			lineSeparater = 3
		else:
			lineSeparater = 4
		
		bwc = re.compile('<td nowrap class="bwc9">([0-9]*|-*)<\/td>')
		bpc = re.compile('<td nowrap class="bpc9">([0-9]*|-*)<\/td>')
		bsc = re.compile('<td nowrap class="bsc9">([0-9]*|-*)<\/td>')
		bwr = re.compile('<td  nowrap class="bwr9">(.[0-9]*\.[0-9]*|.[0-9]*|-*)<\/td>')
		bpr = re.compile('<td  nowrap class="bpr9">(.[0-9]*\.[0-9]*|.[0-9]*|-*)<\/td>')
		bsr = re.compile('<td  nowrap class="bsr9">(.[0-9]*\.[0-9]*|.[0-9]*|-*)<\/td>')
		bwcm = bwc.findall(page)
		bpcm = bpc.findall(page)
		bscm = bsc.findall(page)
		bwrm = bwr.findall(page)
		bprm = bpr.findall(page)
		bsrm = bsr.findall(page)
		
		#print bwcm, bpcm, bscm, bwrm, bprm, bsrm, len(bwcm), len(bpcm), len(bscm), len(bwrm), len(bprm), len(bsrm)
		
		data, dataBWC, dataBPC, dataBSC = {}, [], [], []
		bwrBuy, bprBuy, bsrBuy, bwrSell, bprSell, bsrSell = [], [], [], [], [], []
		for i in range(1, len(bwcm), 2):
			dataBWC.append(bwcm[i])
		for i in range(1, len(bpcm), 2):
			dataBPC.append(bpcm[i])
		for i in range(1, len(bscm), 2):
			dataBSC.append(bscm[i])
			
		for i in range(0, len(bwrm), lineSeparater):
			bwrBuy.append(bwrm[i])
			bwrSell.append(bwrm[i+1])
		for i in range(0, len(bprm), lineSeparater):
			bprBuy.append(bprm[i])
			bprSell.append(bprm[i+1])
		for i in range(0, len(bsrm), lineSeparater):
			bsrBuy.append(bsrm[i])
			bsrSell.append(bsrm[i+1])
			
		for i in range(0, len(dataBWC)):
			data[dataBWC[i]] = {}
			data[dataBWC[i]]['buy'] = bwrBuy[i]
			data[dataBWC[i]]['sell'] = bwrSell[i]
		for i in range(0, len(dataBPC)):
			data[dataBPC[i]] = {}
			data[dataBPC[i]]['buy'] = bprBuy[i]
			data[dataBPC[i]]['sell'] = bprSell[i]
		for i in range(0, len(dataBSC)):
			data[dataBSC[i]] = {}
			data[dataBSC[i]]['buy'] = bsrBuy[i]
			data[dataBSC[i]]['sell'] = bsrSell[i]
			
		return data

#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#

	def GetStockPrice(self):
	
		#----init to get web source----
		url = "http://cathaysec.megatime.com.tw/asp/stockinfo/ps_historyprice.asp"
		values = {}
		values['stockid'] = self.scText.GetValue()
		values['template'] = '1'
		
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		page = urllib2.urlopen(req).read()
		#------------------------------
		
		#----re to get the dates range----
		try:
			p = re.compile("<option>(.*)<\/option>")
			m = p.findall(page)
			values['start'] = m[len(m)-1]
			values['end'] = m[0]
			data = urllib.urlencode(values)
			req = urllib2.Request(url, data)
			page = urllib2.urlopen(req).read()		
		#--------------------------------
		
		#----re to find the dates and closePrice----
			wp = re.compile("<td class=bwr9 Align=right>([0-9]*\.[0-9]*|[0-9]*|[0-9]*\/[0-9]*\/[0-9]*\s+|-*)<\/td>")
			sp = re.compile("<td class=bsr9 Align=right>([0-9]*\.[0-9]*|[0-9]*|[0-9]*\/[0-9]*\/[0-9]*\s+|-*)<\/td>")
			wm = wp.findall(page)
			sm = sp.findall(page)
			m, date, comDate = [], [], []

			for i in range(0, len(wm), 9):
				date.append(wm[i].strip())
				if i < len(sm):
					date.append(sm[i].strip())
			
			for i in range(4, len(wm), 9):
				m.append(float(wm[i]))
				if i < len(sm):
					m.append(float(sm[i]))
			
			n = m[::-1]
			d = date[::-1]
			#----------------------------------------
			return d, n
		
		except:
			box=wx.MessageDialog(None, u"無此代號的股票", "ERROR", style=wx.CANCEL)
			box.ShowModal()
			box.Destroy()
			return None
			
#--------------------------------------------------------------------------------------------#   		

	def OnAbout(self, event):
		box=wx.MessageDialog(None
		, u"這是一個簡單的股票程式\n所有判斷資料擷取自'國泰證券'\n提供河流圖和三大主力買賣量判別\n如有問題請聯繫本人\nEmail: somewhereibeing@gmail.com\n感謝"
		, "About", style=wx.OK)
		box.ShowModal()
		box.Destroy()
		
	def clearButtonClicked(self, event):
		self.textCtrl.Clear()
	
	def OnCloseWindow(self, event):
		self.Destroy()
	
	def OnClose(self, event):
		self.Close()

if __name__ == '__main__':
	app = wx.PySimpleApp(True)
	frame = MyFrame(None, "A Little Stock Program")
	frame.Center()
	frame.Show()
	app.MainLoop()
