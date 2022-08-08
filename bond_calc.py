
import numpy as np
import pandas as pd
from scipy.optimize import newton
import matplotlib.pyplot as plt
import math as m

class Bond:
    def __init__(self):
        self.coupon_rate=float(input("coupon_rate per_annum:"))
        self.maturity=float(input("enter bond's maturity:"))
        self.par_value=float(input("enter face value of the bond"))
        self.freq=float(input("how many times doesthe bond p ayout coupon in an year:"))
        self.price=float(input("price of the bond: "))
        self.nper=int(self.maturity*self.freq)


    def helper(self,intrate):
        cp=np.full(self.nper,(self.coupon_rate/self.freq)*self.par_value)
        cp[-1]+=self.par_value
        yields=np.fromfunction(lambda y:(1+intrate/self.freq)**-(y+1),(self.nper,))
        return np.array(cp*yields)


    def b_price(self,drate=0.01):
        p=np.sum(Bond.helper(self,drate))                      
        return p
        
    def ytm(self):
        yi=newton(lambda y: Bond.b_price(self,y)-self.price,0.05)
        return yi
        
        
    def m_duration(self,intrate):
        t=np.arange(1/self.freq,self.maturity+1/self.freq,1/self.freq)
        d=np.sum(t*Bond.helper(self,intrate))/self.price
        return d

    def duration(self,intrate):
        return Bond.m_duration(self,intrate)*(1+intrate/self.freq)**-1

    def convexity(self,intrate):
        t=np.arange(1/self.freq,self.maturity+1/self.freq,1/self.freq)**2+np.arange(1/self.freq,self.maturity+1/self.freq,1/self.freq)/self.freq
        d=np.sum(t*Bond.helper(self,intrate))/self.price
        c=d*(1+intrate/self.freq)**-2
        return c
    def price_change_pcg(self,delta_y):
        pct_change=Bond.duration(self,Bond.ytm(self))*delta_y+0.5*Bond.convexity(self,Bond.ytm(self))*delta_y**2
        return -pct_change
