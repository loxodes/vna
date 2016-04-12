# generate registers for lmx2592
FREF = 100e6

def lmx_init():
    reg0 = BIT1 # reset
    reg64 # default
    reg48 = # default
    reg47 = # default
    reg46 = 2 << MASH_ORDER 
    reg45 # default, pll num
    reg44 # default, pll denom
    reg43, reg42 # default
    reg41 # frac denom lsb
    reg39 # default
    reg40 # frac denom msb
    reg38 # default, freq
    reg37 # default, n div 20
    reg36/reg35/reg34 # chdiv
    reg31 &= ~VCO_DISTB_PD
    reg31 |= VCO_DISTA_PD
    # efault reg30, 29, 28, 24, 23 19, 14, 13, 10, 11, 12, 10, 96
    # default 8, 7, 10
    reg0 = LD_EN | FCAL_EN | MUXOUT_SEL
    
    
    
    set_pow(b, 15)
    powerup(b, ENABLE)
    power
def powerup(channel, ENABLE):
    if(ENABLE):
    if channel == CHANNELA:
        reg46 &= ~(OUTA_PD)
     if channel == CHANNELB:
        reg46 &= ~(OUTA_PD)
def set_pow(channel, pow):
    if channel == CHANNELB:
        reg47 |= pow << POWB
    elif channel == CHANNELA:
        reg46 |= pow << POWA
def enable_channel(ch):
    pass

def output()
    pass # set chdiv/vco
    
def set_freq(f):
    
def prog_reg(reg, value):
    
# change n
# change frac
# recal    

# goal, 9 GHz to 20 MHz in 100 kHz steps
# vco, 3.55 to 7.10
# use 3.8 to 7

# okay


# so, fpd = 100 MHz
# frac is 200000
# 1 khz resolution
# min N is 18
min_n = 16
pre_n = 2
fpd = 100e6
frac_dem = 200000


def calc_n(f, n_step, div):
    return int(f / (n_step / div))
    
def calc_frac(f, n, n_step, frac_step, div):
    int((f - n * (n_step / div)) / (frac_step / div))
    
def set_freq(f):
    # use second order filter
    div_seg1_range = [1,2,3]
    div_seg2_range = [2,4,6,8]
    div_seg3_range = [2,4,6,8]
    
    f_vco_min = fpd * min_n * pre_n
    f_vco_max = 7000
    
    n_step = fpd * pre_n
    frac_step = n_step / frac_dem
    # second order mash fractional
    
    # if the output frequency is below the minimum vco freq,
    # then we need to use output dividers
    if f < f_vco_min:
        f_vco_max / 
        if f >= (f_vco_min / 2): # use div1
            div1 = 2
            div2 = 1
            div3 = 1
            n = calc_n(f, n_step, 2)
            frac = calc_frac(f, n, n_step, frac_step, 2)
        elif f >= f(f_vco_min / 3):
            div1 = 3
            div2 = 1
            div3 = 1
            div = (div1 * div2 * div3)
            n = calc_n(f, n_step, div)
            frac = calc_frac(f, n, n_step, frac_step, div)
        elif f >= f(f_vco_min / 4):
            div1 = 2
            div2 = 2
            div3 = 1
            div = (div1 * div2 * div3)
            n = calc_n(f, n_step, div)
            frac = calc_frac(f, n, n_step, frac_step, div)            
        elif f >= f(f_vco_min / 6):
            div1 = 3
            div2 = 2
            div3 = 1
            div = (div1 * div2 * div3)
            n = calc_n(f, n_step, div)
            frac = calc_frac(f, n, n_step, frac_step, div)          
        elif f >= f(f_vco_min / 8):
            div1 = 2
            div2 = 4
            div3 = 1
            div = (div1 * div2 * div3)
            n = calc_n(f, n_step, div)
            frac = calc_frac(f, n, n_step, frac_step, div)     
        elif f >= f(f_vco_min / 12):
            div1 = 3
            div2 = 4
            div3 = 1
            div = (div1 * div2 * div3)
            n = calc_n(f, n_step, div)
            frac = calc_frac(f, n, n_step, frac_step, div)
        elif f >= f(f_vco_min / 24):
            div1 = 3
            div2 = 8
            div3 = 1
            div = (div1 * div2 * div3)
            n = calc_n(f, n_step, div)
            frac = calc_frac(f, n, n_step, frac_step, div)
        elif f >= f(f_vco_min / 48):
            div1 = 3
            div2 = 8
            div3 = 2
            div = (div1 * div2 * div3)
            n = calc_n(f, n_step, div)
            frac = calc_frac(f, n, n_step, frac_step, div)
        elif f >= f(f_vco_min / 96):
            div1 = 3
            div2 = 8
            div3 = 4
            div = (div1 * div2 * div3)
            n = calc_n(f, n_step, div)
            frac = calc_frac(f, n, n_step, frac_step, div)
        elif f >= f(f_vco_min / 144):
            div1 = 3
            div2 = 8
            div3 = 6
            div = (div1 * div2 * div3)
            n = calc_n(f, n_step, div)
            frac = calc_frac(f, n, n_step, frac_step, div)
        else:
            div1 = 3
            div2 = 8
            div3 = 8
            div = (div1 * div2 * div3)
            n = calc_n(f, n_step, div)
            frac = calc_frac(f, n, n_step, frac_step, div)
    # if output frequency is above the max vco freq, use doubler
    elif f > f_vco_max: # 7 GHz to 9 GHz
        # TODO: support VCO doubler
        # set pre_n to 4, set vco doubler..
        div1 = 1
        div2 = 1
        div3 = 1
        
    
    else: # 4 GHz to 7 GHz
        div1 = 1
        div2 = 1
        div2 = 1
        n = calc_n(f, n_step, 1)
        frac = calc_frac(f, n, n_step, frac_step, 1)

        
        