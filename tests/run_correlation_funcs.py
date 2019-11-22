

import numpy as np
from scipy import io
from tests import correlation_funcs as cf


data = io.loadmat("UVA0001_rr", squeeze_me = True)
rr = np.asarray(data['rr'])

ids = [6738,
 6797,
 6798,
 6800,
 6802,
 6803,
 6804,
 6809,
 6811,
 6812,
 6813,
 6817,
 6821,
 6823,
 6824,
 6828,
 6829,
 6836,
 6840,
 6842,
 6843,
 6845,
 6848,
 6849,
 6852,
 6853,
 6857,
 6861,
 6862,
 6868,
 6870,
 6872,
 6874,
 6880,
 6883,
 6893,
 6899,
 6903,
 6907,
 6909,
 6914,
 6916,
 6919,
 6920,
 6926,
 6927,
 6930,
 6931,
 6934,
 6937,
 6938,
 6939,
 6944,
 6946,
 6947,
 6949,
 6953,
 6957,
 6963,
 6964,
 6967,
 6968,
 6970,
 6974,
 6975,
 6983,
 6985,
 6988,
 6990,
 6992,
 6993,
 6994,
 7000,
 7005,
 7006,
 7007,
 7008,
 7009,
 7011,
 7012,
 7013,
 7014,
 7016,
 7017,
 7019,
 7020,
 7021,
 7022,
 7024,
 7026,
 7029,
 7033,
 7035,
 7040,
 7042,
 7046,
 7047,
 7048,
 7050,
 7055,
 7056,
 7058,
 7060,
 7067,
 7068,
 7069,
 7070,
 7073,
 7076,
 7077,
 7079,
 7080,
 7086,
 7089,
 7090,
 7094,
 7100,
 7103,
 7104,
 7105,
 7107,
 7113,
 7114,
 7116,
 7117,
 7118,
 7119,
 7120,
 7121,
 7122,
 7125,
 7128,
 7129,
 7131,
 7132,
 7134,
 7135,
 7136,
 7138,
 7139,
 7141,
 7144,
 7145,
 7146,
 7147,
 7148,
 7150,
 7151,
 7152,
 7153,
 7154,
 7155,
 7156,
 7157,
 7158,
 7159,
 7160,
 7161,
 7162,
 7163,
 7164,
 7165,
 7166,
 7167,
 7168,
 7169,
 7170,
 7171,
 7173,
 7174,
 7175,
 7176,
 7177,
 7178,
 7179,
 7180,
 7181,
 7182,
 7183,
 7184,
 7185,
 7186,
 7187,
 7188,
 7189,
 7190,
 7191,
 7192,
 7193,
 7195,
 7199,
 7204,
 7208]

cf.do_it_all(ids, 'HR', '/HR Results')


