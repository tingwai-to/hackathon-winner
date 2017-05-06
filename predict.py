import sys
from sklearn.externals import joblib

model = joblib.load('model.pkl')


def get_prob_winning(text):
    return model.predict_proba([text])[0][1]


if __name__ == '__main__':
    print('probability of winning {:.2%}'.format(get_prob_winning(sys.argv[1])))
