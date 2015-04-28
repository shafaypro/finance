import sys
import os
p = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'lib')
if p in sys.path:
    pass
else:
    sys.path.append(p)
from analysis import Analysis
from file_io import FileIO
from ti import TechnicalIndicators

def demo(stock='N225',
         name='日経平均株価',
         start='2014-01-01',
         days=180,
         csvfile=os.path.join(os.path.dirname(
             os.path.abspath(__file__)),
             '..',
             'test',
             'stock_N225.csv'),
         update=False):

    # Handling ti object example.
    io = FileIO()
    stock_d = io.read_from_csv(stock,
                               csvfile)
    ti = TechnicalIndicators(stock_d)
    ti.calc_ret_index()

    print(ti.stock['ret_index'].tail(10))
    io.save_data(io.merge_df(stock_d, ti.stock),
                 stock, 'demo_')

    # Run analysis code example.
    analysis = Analysis(stock=stock,
                        name=name,
                        start=start,
                        days=days,
                        csvfile=csvfile,
                        update=True)
    return analysis.run()

if __name__ == '__main__':
    argsmin = 0
    version = (3, 0)
    if sys.version_info > (version):
        if len(sys.argv) > argsmin:
            demo()
        else:
            print("This program needs at least %(argsmin)s arguments" %
                  locals())
    else:
        print("This program requires python > %(version)s" % locals())
