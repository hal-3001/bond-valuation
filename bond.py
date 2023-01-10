import numpy as np
from scipy.optimize import newton
class Bond:
    def __init__(self,facevalue,coupon,cpay,bm):
        """facevalue:The Bond’s Face Value
        coupon:Coupon rate (in decimals terms)
        cpay:Number of payments per period (e.g., m=2 for semiannually payments)
        bm:Number of years to maturity"""
        self.facevalue=facevalue
        self.coupon=coupon
        self.cpay=cpay
        self.bm=bm
        self.price=None
        self.ytm=None
    def bprice(self):
        if self.price:
            return self.price
        
        total_coupons=self.bm*self.cpay
        # total no of times a coupon is payed till maturity
        coupon_payments=np.array([self.facevalue*self.coupon/self.cpay]*total_coupons)
        coupon_payments[-1]+=self.facevalue
        # all the coupon payments from the bond without discounting
        discounts=np.array([1+self.ytm/self.cpay]*total_coupons)**np.arange(1,total_coupons+1,1)
        # discounting factors for the coupon_payments
        bondprice=(coupon_payments/discounts)
        self.price=np.sum(bondprice)
        return self.price
    
    def ytmfunc(self,grate):
        # this a helper function which discounts the cashflows at a given rate:grate
        total_coupons=self.bm*self.cpay
        coupon_payments=np.array([self.facevalue*self.coupon/self.cpay]*total_coupons)
        coupon_payments[-1]+=self.facevalue
        discounts=np.array([1+grate/self.cpay]*total_coupons)
        bondprice=(coupon_payments/(discounts**np.arange(1,total_coupons+1)))
        return bondprice

    def bytm(self):
        if self.ytm:
            return self.ytm
        yi=newton(lambda y: np.sum(Bond.ytmfunc(self,y))-self.price,0.02)
        self.ytm=yi*self.cpay
        return self.ytm


    def macaulay_duration(self):
        time=np.arange(1/self.cpay,(self.bm)+1/self.cpay,1/self.cpay)
        change=np.sum((time*Bond.ytmfunc(self,self.ytm))/Bond.bprice(self))
        return change
        
    def modified_duration(self):
        macd=Bond.macaulay_duration(self)
        return macd/(1+(self.ytm/self.cpay))
        
    def convexity(self):
        time=(np.arange(1/self.cpay,(self.bm)+1/self.cpay,1/self.cpay)**2)+np.arange(1/self.cpay,(self.bm)+1/self.cpay,1/self.cpay)
        c=np.sum(time*Bond.ytmfunc(self,self.ytm))
        return c/((Bond.bprice(self)*(1+self.ytm)**2))

    def price_pct_change(self,yieldchange=0.01):
        bd=Bond.macaulay_duration(self)
        ca=Bond.convexity(self)*100*(yieldchange**2)
        return bd*yieldchange+ca

    
    def __repr__(self):
        return f"bond price:{Bond.bprice(self)},facevalue: {self.facevalue}, coupon: {self.coupon}, no of coupon payments in a year: {self.cpay}, no of year's till maturity: {self.bm}, ytm:{self.ytm}"