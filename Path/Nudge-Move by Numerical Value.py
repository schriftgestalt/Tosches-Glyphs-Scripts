#MenuTitle: Nudge-move by Numerical Value...
# -*- coding: utf-8 -*-
__doc__="""
(GUI) Nudge-moves selected nodes by the values specified in the window. Vanilla required.
"""

import vanilla
import GlyphsApp

GSSteppingTextField = objc.lookUpClass("GSSteppingTextField")
class ArrowEditText (vanilla.EditText):
	nsTextFieldClass = GSSteppingTextField
	def _setCallback(self, callback):
		super(ArrowEditText, self)._setCallback(callback)
		if callback is not None and self._continuous:
			self._nsObject.setContinuous_(True)
			self._nsObject.setAction_(self._target.action_)
			self._nsObject.setTarget_(self._target)

class ParametricEstimated( object ):
	def __init__( self ):
		# Window 'self.w':
		edX = 40
		edY = 17
		txX = 20
		txY = 17
		slX = 200
		spX = 10
		spY = 10
		btnY = 17
		btnX = 60
		windowWidth  = spX*3+txX+edX+slX
		windowHeight = spY*6+txY*2+btnY*4
		windowWidthResize = 500
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Nudge-Move", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight ), # maximum size (for resizing)
			autosaveName = "com.Tosche.Nudge-movebyNumericalValue(GUI).mainwindow" # stores last window position and size
		)
		
		# UI elements:
		self.w.txX = vanilla.TextBox( (spX, spY, txX, txY), "X:", sizeStyle='small')
		self.w.txY = vanilla.TextBox( (spX, spY*2+txY, txX, txY), "Y:", sizeStyle='small')

		self.w.edX = ArrowEditText( (spX+txX, spY, edX, edY), "10", sizeStyle='small', callback=self.textChange)
		self.w.edY = ArrowEditText( (spX+txX, spY*2+txY, edX, edY), "10", sizeStyle='small', callback=self.textChange)
	
		self.w.slX = vanilla.Slider( (spX*2+txX+edX, spY, -spX, edY), sizeStyle='small', minValue=0, maxValue=50, value=10, callback=self.sliderChange)
		self.w.slY = vanilla.Slider( (spX*2+txX+edX, spY*2+txY, -spX, edY), sizeStyle='small', minValue=0, maxValue=50, value=10, callback=self.sliderChange)

		# Run Button:
		self.w.tl = vanilla.SquareButton((spX, spY*3+txY*2, btnX, btnY), u"↖", sizeStyle='small', callback=self.nudgeMove )
		self.w.l = vanilla.SquareButton((spX, spY*4+txY*2+btnY, btnX, btnY), u"←", sizeStyle='small', callback=self.nudgeMove )
		self.w.dl = vanilla.SquareButton((spX, spY*5+txY*2+btnY*2, btnX, btnY), u"↙", sizeStyle='small', callback=self.nudgeMove )

		self.w.t = vanilla.SquareButton((spX*2+btnX, spY*3+txY*2, btnX, btnY), u"↑", sizeStyle='small', callback=self.nudgeMove )
		self.w.d = vanilla.SquareButton((spX*2+btnX, spY*5+txY*2+btnY*2, btnX, btnY), u"↓", sizeStyle='small', callback=self.nudgeMove )

		self.w.tr = vanilla.SquareButton((spX*3+btnX*2, spY*3+txY*2, btnX, btnY), u"↗", sizeStyle='small', callback=self.nudgeMove )
		self.w.r = vanilla.SquareButton((spX*3+btnX*2, spY*4+txY*2+btnY, btnX, btnY), u"→", sizeStyle='small', callback=self.nudgeMove )
		self.w.dr = vanilla.SquareButton((spX*3+btnX*2, spY*5+txY*2+btnY*2, btnX, btnY), u"↘", sizeStyle='small', callback=self.nudgeMove )

		self.LoadPreferences()

		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
		
	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["com.tosche.Nudge-movebyNumericalValue(GUI).fieldX"] = self.w.edX.get()
			Glyphs.defaults["com.tosche.Nudge-movebyNumericalValue(GUI).fieldY"] = self.w.edY.get()
		except:
			return False
		return True

	def LoadPreferences( self ):
		try:
			self.w.edX.set( Glyphs.defaults["com.tosche.Nudge-movebyNumericalValue(GUI).fieldX"] )
			self.w.edY.set( Glyphs.defaults["com.tosche.Nudge-movebyNumericalValue(GUI).fieldY"] )
			self.w.slX.set( int(Glyphs.defaults["com.tosche.Nudge-movebyNumericalValue(GUI).fieldX"]) )
			self.w.slY.set( int(Glyphs.defaults["com.tosche.Nudge-movebyNumericalValue(GUI).fieldY"]) )
		except:
			return False
		return True

	def sliderChange(self, sender):
		try:
			self.w.edX.set(int(self.w.slX.get()))
			self.w.edY.set(int(self.w.slY.get()))
		except Exception, e:
			Glyphs.showMacroWindow()
			print "Nudge-Move By Numerical Value... Error (sliderChange): %s" % e

	def textChange( self, sender ):
		try:
			edXvalue = int(self.w.edX.get()) if self.w.edX.get() != "" else 0
			self.w.slX.set(edXvalue)
			edYvalue = int(self.w.edY.get()) if self.w.edY.get() != "" else 0
			self.w.slY.set(edYvalue)
		except Exception, e:
			Glyphs.showMacroWindow()
			print "Nudge-Move By Numerical Value... Error (textChange): %s" % e

	def nudge(self, onMv, off1, off2, onSt, offsetX, offsetY):
		try:
			# onST = starting on-curve
			# onMv = moving on-curve
			distanceX = onMv.x - onSt.x
			distanceX1 = onMv.x - off1.x
			distanceX2 = off2.x - onSt.x
			if distanceX != 0:
				valueX1 = distanceX1/distanceX
				valueX2 = distanceX2/distanceX
			else:
				valueX1 = 0
				valueX2 = 0
			if distanceX1 != 0:
				off1.x += (1-valueX1)*offsetX
			else:
				off1.x += offsetX
		
			if distanceX2 != 0:
				off2.x += (valueX2)*offsetX
		
			distanceY = onMv.y - onSt.y
			distanceY1 = onMv.y - off1.y
			distanceY2 = off2.y - onSt.y
			if distanceY1 != 0:
				off1.y += (1-distanceY1/distanceY)*offsetY
			else:
				off1.y += offsetY
		
			if distanceY2 != 0:
				off2.y += (distanceY2/distanceY)*offsetY
		except Exception, e:
			pass
			# Glyphs.showMacroWindow()
			# print "Nudge-move by Numerical Value Error (nudge): %s" % e

	def nudgeMove( self, sender ):
		try:
			if sender in [self.w.tl, self.w.l, self.w.dl]:
				offsetX = -float(self.w.edX.get())
			elif sender in [self.w.tr, self.w.r, self.w.dr]:
				offsetX = float(self.w.edX.get())
			else:
				offsetX = 0.0

			if sender in [self.w.tl, self.w.t, self.w.tr]:
				offsetY = float(self.w.edY.get())
			elif sender in [self.w.dl, self.w.d, self.w.dr]:
				offsetY = -float(self.w.edY.get())
			else:
				offsetY = 0.0
		except:
			Glyphs.displayDialog_withTitle_("You seem to have entered a value that is not a number. Period is fine.", "Numbers only!")

		try:
			Font = Glyphs.font # frontmost font
			Font.disableUpdateInterface()
			listOfSelectedLayers = Font.selectedLayers
			for thisLayer in Font.selectedLayers:
				glyph = thisLayer.parent
				glyph.beginUndo()
				for thisPath in thisLayer.paths:
					numOfNodes = len(thisPath.nodes)
					for i in range(numOfNodes):
						node = thisPath.nodes[i]
						if node in thisLayer.selection:
							nodeBefore = thisPath.nodes[i-1]
							if (nodeBefore != None) and (not nodeBefore in thisLayer.selection):
								if nodeBefore.type == GSOFFCURVE: # if on-curve is the edge of selection
									if thisPath.nodes[i-2].type == GSOFFCURVE:
										oncurveMv = node
										offcurve1 = nodeBefore
										offcurve2 = thisPath.nodes[i-2]
										oncurveSt = thisPath.nodes[i-3]
										self.nudge(oncurveMv, offcurve1, offcurve2, oncurveSt, offsetX, offsetY)
									elif thisPath.nodes[i-2].type == GSCURVE: # if off-curve is the edge of selection
										oncurveMv = thisPath.nodes[i+1]
										offcurve1 = node
										offcurve2 = nodeBefore
										oncurveSt = thisPath.nodes[i-2]
										self.nudge(oncurveMv, offcurve1, offcurve2, oncurveSt, offsetX, offsetY)
										node.x -= offsetX
										node.y -= offsetY

							nodeAfter = thisPath.nodes[i+1]
							if (nodeAfter != None) and (not nodeAfter in thisLayer.selection):
								if nodeAfter.type == GSOFFCURVE: # if on-curve is the edge of selection
									if thisPath.nodes[i+2].type == GSOFFCURVE:
										oncurveMv = node
										offcurve1 = nodeAfter
										offcurve2 = thisPath.nodes[i+2]
										oncurveSt = thisPath.nodes[i+3]
										self.nudge(oncurveMv, offcurve1, offcurve2, oncurveSt, offsetX, offsetY)
									elif thisPath.nodes[i+2].type == GSCURVE: # if off-curve is the edge of selection
										thisPath.nodes[i-1].x -= offsetX
										thisPath.nodes[i-1].y -= offsetY
										oncurveMv = thisPath.nodes[i-1]
										offcurve1 = node
										offcurve2 = nodeAfter
										oncurveSt = thisPath.nodes[i+2]
										self.nudge(oncurveMv, offcurve1, offcurve2, oncurveSt, offsetX, offsetY)
										thisPath.nodes[i-1].x += offsetX
										thisPath.nodes[i-1].y += offsetY
										node.x -= offsetX
										node.y -= offsetY		
							node.x += offsetX
							node.y += offsetY
				glyph.endUndo()
				Font.enableUpdateInterface()
			
			if not self.SavePreferences( self ):
				print "Note: 'Nudge-move by Numerical Value' could not write preferences."
			
		except Exception, e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print "Nudge-move by Numerical Value Error: %s" % e

ParametricEstimated()