__DESCRIPTION__="""take_measures is a class to handle measures taken on plots.
#create the plot
from matplotlib   import pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.random.rand(10))
show()
#connect to take_measures
tm=take_measures(fig)

now you may work with the mouse (press key h to see an help)

Author: M.Maris - 1.0 - 13 Dec 2012 -
"""

class _template_event_handler :
   def __init__(self,fig,verbose) :
      self.fig=fig
      self.verbose=verbose
      self.cid={}
      self.cid['button_press_event'] = fig.canvas.mpl_connect('button_press_event', self.button_press_event)
      self.cid['button_release_event'] = fig.canvas.mpl_connect('button_release_event', self.button_release_event)
      self.cid['key_press_event'] = fig.canvas.mpl_connect('key_press_event', self.key_press_event)
      self.cid['key_release_event'] = fig.canvas.mpl_connect('key_release_event', self.key_release_event)
      self.cid['motion_notify_event'] = fig.canvas.mpl_connect('motion_notify_event', self.motion_notify_event)
      self.cid['pick_event'] = fig.canvas.mpl_connect('pick_event', self.pick_event)
      self.cid['resize_event'] = fig.canvas.mpl_connect('resize_event', self.resize_event)
      self.cid['scroll_event'] = fig.canvas.mpl_connect('scroll_event', self.scroll_event)
      self.cid['figure_enter_event'] = fig.canvas.mpl_connect('figure_enter_event', self.figure_enter_event)
      self.cid['figure_leave_event'] = fig.canvas.mpl_connect('figure_leave_event', self.figure_leave_event)
      self.cid['axes_enter_event'] = fig.canvas.mpl_connect('axes_enter_event', self.axes_enter_event)
      self.cid['axes_leave_event'] = fig.canvas.mpl_connect('axes_leave_event', self.axes_leave_event)
      self.enable()
   def enable(self) :
      self.enabled=True
   def disable(self) :
      self.enabled=False
   def toggle_enabled(self) :
      self.enabled=self.enabled==False
   def isenabled(self) :
      return self.enabled
   def button_press_event(self,event):pass
   def button_release_event(self,event):pass
   def key_press_event(self,event):pass
   def key_release_event(self,event):pass
   def motion_notify_event(self,event):pass
   def pick_event(self,event):pass
   def resize_event(self,event):pass
   def scroll_event(self,event):pass
   def figure_enter_event(self,event):pass
   def figure_leave_event(self,event):pass
   def axes_enter_event(self,event):pass
   def axes_leave_event(self,event):pass
   
class take_measures_on_plot(_template_event_handler) :
   class _struct :
      def __init__(self) : pass
      def keys(self) : return self.__dict__.keys()
      def __len__(self) : return len(self.keys())
   class _myevent :
      def __init__(self,*arg) :
         if len(arg)==0 : return
         if len(arg)==1 : 
            self.button=event.button
            self.x=event.x
            self.y=event.y
            self.xdata=event.xdata 
            self.ydata=event.ydata
         self.button=int(arg[0])
         self.x=float(arg[1])
         self.y=float(arg[2])
         self.xdata=float(arg[3])
         self.ydata=float(arg[4])
   def __init__(self,fig,filename='take_measures.csv',marker='o',ax=None,verbose=True,vbar=None,restore=None,dot=True,dot_at_restore=False,xscale=None,yscale=None) :
      from matplotlib   import pyplot as plt
      import numpy as np
      _template_event_handler.__init__(self,fig,verbose)
      self.marker=marker
      self.filename=filename
      self.imarker=[]
      self.table_markers=[]
      self.ilast=-1
      self.order=[]
      self.event_tuples=[]
      self.ax=plt.gca() if ax == None else ax
      self.vbar=vbar
      self.dot=dot==True
      self.xscale=xscale
      self.yscale=yscale
      a=plt.axis()
      self.yrange=np.array([a[2],a[3]])
      self.xrange=np.array([a[0],a[1]])
      if type(restore)==type('') :
         isfirst=True
         self.dot=dot_at_restore==True
         for k in open(restore,'r') :
            if not isfirst :
               line=k.split(',')
               self.mark(self._myevent(1,line[1],line[2],line[3],line[4]))
            else :
               isfirst=False
      elif type(restore)==type({}) :
         self.dot=dot_at_restore==True
         for k in range(len(restore['xdata'])) :
            self.mark(self._myevent(1,restore['x'][k],restore['y'][k],restore['xdata'][k],restore['ydata'][k]))
      self.dot=dot==True
   def __len__(self) :
      return self.ilast+1
   def tolist(self) :
      import numpy as np
      if len(self) == 0 : return
      out=self._struct()
      out.xmouse = np.zeros(len(self))
      out.ymouse = np.zeros(len(self))
      out.xdata = np.zeros(len(self))
      out.ydata = np.zeros(len(self))
      out.xscaled= np.zeros(len(self))
      out.yscaled= np.zeros(len(self))
      for i in self.order :
         out.xmouse[i]=self.event_tuples[i].x
         out.ymouse[i]=self.event_tuples[i].y
         out.xdata[i]=self.event_tuples[i].xdata
         out.ydata[i]=self.event_tuples[i].ydata
      if type(self.xscale) == type([]) :
         out.xscaled=out.xdata*self.xscale[0]+self.xscale[1]
      elif type(self.xscale) == type({}) :
         out.xscaled=out.xdata*self.xscale['delta']+self.xscale['min']
      else :
         out.xscaled=out.xdata*1
      if type(self.yscale) == type([]) :
         out.yscaled=out.ydata*self.yscale[0]+self.yscale[1]
      elif type(self.yscale) == type({}) :
         out.yscaled=out.ydata*self.yscale['delta']+self.yscale['min']
      else :
         out.yscaled=out.ydata*1
      return out
   def store(self,event) :
      self.event_tuples.append(event)
   def button_press_event(self,event):
      import numpy as np
      import copy
      from matplotlib   import pyplot as plt
      if self.enabled:
         if event.inaxes != None :
            if self.verbose : print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(event.button, event.x, event.y, event.xdata, event.ydata)
            if event.button == 1 :
               self.mark(event)
               #plt.plot(event.xdata, event.ydata,self.marker)
               #mm=[]
               #mm.append(len(self.ax.lines)-1)
               #if self.vbar :
                  #plt.plot(event.xdata*np.ones(2),self.yrange,'k--')
                  #mm.append(len(self.ax.lines)-1)
               #self.push_event(event,mm)
               print self.ilast
            elif event.button == 3 and len(self) > 0:
               self.unmark()
               #print self.table_markers[self.ilast]
               print self.ilast
   def mark(self,event) :
      from matplotlib   import pyplot as plt
      import numpy as np
      mm=[]
      if self.dot :
         plt.plot(event.xdata, event.ydata,self.marker)
         mm.append(len(self.ax.lines)-1)
      if self.vbar!=None :
         plt.plot(event.xdata*np.ones(2),self.yrange,'k--',color=self.vbar)
         mm.append(len(self.ax.lines)-1)
      self.push_event(event,mm)
   def unmark(self) :
      from matplotlib   import pyplot as plt
      import numpy as np
      for k in range(len(self.table_markers[self.ilast])-1,-1,-1) : 
         i=self.table_markers[self.ilast][k]
         del self.ax.lines[i]
      plt.draw()
      self.pop_event()
   def key_press_event(self,event):
      import numpy as np
      import copy
      if event.key.lower() == 't' :
         self.toggle_enabled()
         print 'enabled' if self.enabled else 'disabled'
         return
      elif event.key.lower() == 'h' :
         print
         print "Keys : "
         print "  h : print an help"
         print "  t : toggle the measurer on or off"
         print
         print """

  w : write to disk the measures
  n : number of measures stored
  x : sort the list of measures in increasing x
  y : sort the list of measures in increasing y
  p : print the list on screen
  r : remove all the measures
  
Mouse Buttons:
Left  : take a measure
Right : remove last measure in the list

Beware: 
  Right Mouse Button after x and y may cause failure in some functions
  
"""
      if self.enabled:
         if self.verbose : print 'key=%s, x=%d, y=%d, xdata=%f, ydata=%f'%(event.key, event.x, event.y, event.xdata, event.ydata)
         if event.key.lower() == 'w':
            if not len(self) :
               print 'nothing to save'
               return
            else :
               print 'saving values into csv file ',self.filename
               self.tofile(self.filename)
               return
         if event.key.lower() == 'p':
            if not len(self) : 
               print 'nothing to print'
               return
            else :
               self.show()
               return
         if event.key.lower() == 'r':
            if not len(self) : 
               print 'nothing to remove'
               return
            else :
               for i in range(len(self)) :
                  del self.ax.lines[self.imarker[self.ilast]]
               plt.draw()
               self.clean()
               return
         elif event.key.lower() == 'n' :
            print 'number of stored values ',len(self)
            return
         elif event.key.lower() == 'x' and len(self) :
            print "sort by increasing x"
            self.x_sort()
            return
         elif event.key.lower() == 'y' and len(self) :
            print "sort by increasing x"
         else :
            pass
   def clean(self) :
      import numpy as np
      import copy
      self.event_tuples=[]
      self.imarker=[]
      self.order=[]
      self.ilast=len(self.order)-1
   def pop_event(self) :
      import numpy as np
      import copy
      self.table_markers.pop()
      self.event_tuples.pop()
      self.imarker.pop()
      self.order.pop()
      self.ilast=len(self.order)-1
   def push_event(self,event,mm) :
      self.table_markers.append(mm)
      self.imarker.append(len(self.ax.lines)-1)
      self.store(event)
      self.ilast=len(self.order)
      self.order.append(self.ilast)
   #def tofile(self,filename) :
      #if len(self) == 0 : return
      #try :
         #f=open(filename,'w')
      #except :
         #print "impossible to open '%s'"%filename
         #return
      #f.write('sample,xscreen,yscreen,xdata,ydata\n')
      #for i in self.order :
         #line=[str(i)]
         #line.append(str(self.event_tuples[i].x))
         #line.append(str(self.event_tuples[i].y))
         #line.append(str(self.event_tuples[i].xdata))
         #line.append(str(self.event_tuples[i].ydata))
         #f.write(','.join(line)+'\n')
      #f.close()
      #return
   def tofile(self,filename) :
      if len(self) == 0 : return
      try :
         f=open(filename,'w')
      except :
         print "impossible to open '%s'"%filename
         return
      f.write('sample,xscreen,yscreen,xdata,ydata,xscaled,yscaled\n')
      lst=self.tolist()
      for i in range(len(self)) :
         line=[str(i)]
         line.append(str(lst.xmouse[i]))
         line.append(str(lst.ymouse[i]))
         line.append(str(lst.xdata[i]))
         line.append(str(lst.ydata[i]))
         line.append(str(lst.xscaled[i]))
         line.append(str(lst.yscaled[i]))
         f.write(','.join(line)+'\n')
      f.close()
      return
   def show(self) :
      line='sample,xscreen,yscreen,xdata,ydata,xscaled,yscaled'.split(',')
      for i in range(len(line)) : line[i] = (line[i]+'            ')[0:12]
      print
      print ' '.join(line)
      if len(self) == 0 : return
      lst=self.tolist()
      for i in range(len(self)) :
         line=[str(i)]
         line.append(str(lst.xmouse[i]))
         line.append(str(lst.ymouse[i]))
         line.append(str(lst.xdata[i]))
         line.append(str(lst.ydata[i]))
         line.append(str(lst.xscaled[i]))
         line.append(str(lst.yscaled[i]))
         #line.append(str(self.event_tuples[i].x))
         #line.append(str(self.event_tuples[i].y))
         #line.append(str(self.event_tuples[i].xdata))
         #line.append(str(self.event_tuples[i].ydata))
         for il in range(len(line)) : line[il] = (line[il].strip()+'                   ')[0:12]
         print ' '.join(line)
      print
   def x_sort(self) :
      import numpy as np
      if len(self) == 0 : return
      order=np.array(self.order)
      x=np.zeros(len(self))
      for i in range(len(self)) : x[i]=self.event_tuples[i].x
      ix=np.argsort(x)
      self.order=(order[ix]).tolist()
   def y_sort(self) :
      import numpy as np
      if len(self) == 0 : return
      order=np.array(self.order)
      x=np.zeros(len(self))
      for i in range(len(self)) : x[i]=self.event_tuples[i].y
      ix=np.argsort(x)
      self.order=(order[ix]).tolist()

if __name__=='__main__' :
   from matplotlib   import pyplot as plt
   fig = plt.figure()
   ax = fig.add_subplot(111)
   ax.plot(np.random.rand(10))
   show()
   tm=take_measures(fig)
