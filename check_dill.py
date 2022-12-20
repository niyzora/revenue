import joblib
import dill

input_file = 'model.bin'

with open(input_file, 'rb') as f_in:
    sc, model = joblib.load(f_in)

dill.dump_module('sc_mode.pkl')
