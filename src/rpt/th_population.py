from src.setup.setup import setup_tradehub

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import font_manager, rc
import matplotlib

# Setup
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
plt.rc('font', family=font_name)
matplotlib.rcParams['axes.unicode_minus'] = False

"""
빅데이터 분석 1 : 상권_상주인구
결론 :
ㅁㄴㅇㅁㄴㅇ
"""
상권_상주인구 = setup_tradehub('상권_상주인구.csv')