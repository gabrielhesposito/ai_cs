import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
# from matplotlib.widgets import Slider, Button, RadioButtons

#Read in correction data & propagation delay data as command-line arguments
#propagation delay data as argv[1]
#correction data as argv[2]
def collect_data():
    global xd, yd, x, pdin, pdout
    x, pdin, pdout = np.loadtxt(sys.argv[1], delimiter=",", unpack=True)
    xd, yd = np.loadtxt(sys.argv[2], delimiter=",", unpack=True)
    for i in range(len(xd)):
        xd[i] = xd[i]/10000

    for j in range(len(x)):
        x[j] = x[j]/10000

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

#find lines of best fit (degree 1):
def line_of_best_fit():
    PDout_Weights=[]
    PDin_Weights=[]

    for num in my_range(0, len(x), 1000):
        x_d = x[num:num+1000]
        pdin_d = pdin[num:num+1000]
        pdout_d = pdout[num:num+1000]

        par_pdin = np.polyfit(x_d, pdin_d, 1, full=True)
        par_pdout = np.polyfit(x_d, pdout_d, 1, full=True)

        slope_pdin = par_pdin[0][0]
        slope_pdout = par_pdout[0][0]

        intercept_pdin = par_pdin[0][1]
        intercept_pdout = par_pdout[0][1]

        line_equation_out={}
        line_equation_out['k'] = (x_d[0], x_d[len(x_d)-1])
        line_equation_out['w1_out']= slope_pdout
        line_equation_out['w0_out']= intercept_pdout
        PDout_Weights.append(line_equation_out)

        line_equation_in={}
        line_equation_in['k'] = (x_d[0], x_d[len(x_d)-1])
        line_equation_in['w1_in']= slope_pdin
        line_equation_in['w0_in']= intercept_pdin
        PDin_Weights.append(line_equation_in)

    return (PDout_Weights, PDin_Weights)


def plot_data():
    par_ck = np.polyfit(xd, yd, 1, full=True)
    par_pdin = np.polyfit(x, pdin, 1, full=True)
    par_pdout = np.polyfit(x, pdout, 1, full=True)

    slope_ck = par_ck[0][0]
    slope_pdin = par_pdin[0][0]
    slope_pdout = par_pdout[0][0]

    intercept_ck = par_ck[0][1]
    intercept_pdin = par_pdin[0][1]
    intercept_pdout = par_pdout[0][1]

    x_ck = [min(xd), max(xd)]
    y_ck = [slope_ck*xx + intercept_ck for xx in x_ck]
    x_pdin = x_pdout = [min(x), max(x)]
    y_pdin = [slope_pdin*xx + intercept_pdin for xx in x_pdin]
    y_pdout = [slope_pdout*xx + intercept_pdout for xx in x_pdout]

    # coefficient of determination: C(k)
    variance_ck = np.var(yd)
    residuals_ck = np.var([(slope_ck*xx + intercept_ck - yy) for xx, yy in zip(xd,yd)])
    Rsqr_ck = np.round(1-residuals_ck/variance_ck, decimals=2)

    # coefficient of determination: PDin
    variance_pdin = np.var(pdin)
    residuals_pdin = np.var([(slope_pdin*xx + intercept_pdin - yy) for xx, yy in zip(x,pdin)])
    Rsqr_pdin = np.round(1-residuals_pdin/variance_pdin, decimals=2)

    # coefficient of determination: PDout
    variance_pdout = np.var(pdout)
    residuals_pdout = np.var([(slope_pdout*xx + intercept_pdout - yy) for xx, yy in zip(x,pdout)])
    Rsqr_pdout = np.round(1-residuals_pdout/variance_pdout, decimals=2)


    plt.figure(1)

    plt.subplot(221)
    plt.scatter(xd, yd, s=30, alpha=0.15, marker='.')
    plt.plot(x_ck, y_ck, 'r--')
    plt.text(.8*max(xd)+.1*min(xd),.9*max(yd)+.5*min(yd), '$R^2 = %0.2f$'% Rsqr_ck, fontsize=16)
    plt.text(.6*max(xd)+.1*min(xd),.9*max(yd), '$y = %fx%0.2f$'%(slope_ck, intercept_ck), fontsize=16)
    plt.title('C(k)')
    plt.xlabel('Time Interval(ms)')
    plt.ylabel('(PDout-PDin)/2')
    plt.grid(True)

    plt.subplot(222)
    plt.scatter(x, pdin, s=30, alpha=0.15, marker='.')
    plt.plot(x_pdin, y_pdin, 'g--')
    plt.text(.8*max(x)+.1*min(x),.7*max(pdin)+.5*min(pdin), '$R^2 = %0.2f$'% Rsqr_pdin, fontsize=16)
    plt.text(.6*max(x)+.1*min(x),.85*max(pdin)+.1*min(pdin), '$y = %fx+%0.2f$'%(slope_pdin, intercept_pdin), fontsize=16)
    plt.title('Propagation Delays: PDin')
    plt.xlabel('Time Interval(ms)')
    plt.ylabel('PDin')
    plt.grid(True)

    plt.subplot(223)
    plt.scatter(x, pdout, s=30, alpha=0.15, marker='.')
    plt.plot(x_pdout, y_pdout, 'g--')
    plt.text(.85*max(x)+.1*min(x),.8*max(pdout)+.5*min(pdout), '$R^2 = %0.2f$'% Rsqr_pdout, fontsize=16)
    plt.text(.6*max(x)+.1*min(x),.9*max(pdout)+.1*min(pdout), '$y = %fx+%0.2f$'%(slope_pdout, intercept_pdout), fontsize=16)
    plt.title('Propagation Delays: PDout')
    plt.xlabel('Time Interval(ms)')
    plt.ylabel('PDout')
    plt.grid(True)

    plt.show()

def weights_to_csv(pdout_weights, pdin_weights):
    handle_pdout = open('pdoutweights.csv', 'w')
    handle_pdin = open('pdinweights.csv', 'w')
    for i in pdout_weights:
        for key in i.keys():
            handle_pdout.write(str(i[key]) + ",")
        handle_pdout.write('\n')
    handle_pdout.close()
    for j in pdin_weights:
        for key in j.keys():
            handle_pdin.write(str(j[key]) + ",")
        handle_pdin.write('\n')
    handle_pdin.close()

def main():
    collect_data()
    pdout_params, pdin_params = line_of_best_fit()
    # weights_to_csv(pdout_params, pdin_params)
    plot_data()

if __name__ == "__main__":
    main()
