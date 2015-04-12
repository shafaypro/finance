import sys
import os
import pandas as pd
from nose.tools import eq_
p = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'lib')
if p in sys.path:
    pass
else:
    sys.path.append(p)
from ti import TechnicalIndicators
from classifier import Classifier

def testdata():
    days = 91
    filename = os.path.join(os.path.dirname(
                            os.path.abspath(__file__)),
                            'stock_N225.csv')
    stock_tse = pd.read_csv(filename,
                            index_col=0, parse_dates=True)
    return stock_tse.asfreq('B')[days:]

def test_classify():
    stock_d = testdata()
    ti = TechnicalIndicators(stock_d)

    filename = 'test_N225.pickle'
    clffile = os.path.join(os.path.dirname(
                           os.path.abspath(__file__)),
                           '..', 'clf',
                           filename)

    if os.path.exists(clffile):
        os.remove(clffile)

    clf = Classifier(filename)
    ti.calc_ret_index()
    ret = ti.stock['ret_index']

    train_X, train_y = clf.train(ret)

    r = round(train_X[-1][-1], 5)
    expected = 1.35486
    eq_(r, expected)

    r = round(train_X[0][0], 5)
    expected = 1.19213
    eq_(r, expected)

    expected = [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1,
                0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1,
                0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1,
                1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0,
                1, 1, 0]
    for r, e in zip(train_y, expected):
        eq_(r, e)

    expected = 14
    r = len(train_X[0])
    eq_(r, expected)

    expected = 75
    r = len(train_X)
    eq_(r, expected)

    expected = 1
    test_y = clf.classify(ret)
    eq_(test_y[0], expected)

    train_X, train_y = clf.train(ret)

    r = round(train_X[-1][-1], 5)
    expected = 1.35486
    eq_(r, expected)

    r = round(train_X[0][0], 5)
    expected = 1.30311
    eq_(r, expected)

    expected = 0
    eq_(train_y[0], expected)

    expected = 14
    r = len(train_X[0])
    eq_(r, expected)

    expected = 1
    r = len(train_X)
    eq_(r, expected)

    expected = 0
    test_y = clf.classify(ret)
    eq_(test_y[0], expected)

    if os.path.exists(clffile):
        os.remove(clffile)

if __name__ == '__main__':
    test_classify()
