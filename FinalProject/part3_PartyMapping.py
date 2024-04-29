import config as cfg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

USE_NEO4J = False

# Load config file and identify file paths
config = cfg.loadConfig()
data_path = config['paths']['data']
save_path = config['paths']['save']

# Load data
if USE_NEO4J:

else:
    data = pd.read_csv(f'{data_path}/HSall_custom.csv')

data_old = data[data['congress'].isin(range(4, 15))]
data_new = data[data['congress'].isin(range(108, 119))]

print('Parties of first decade of Congress:')
print(data_old['party_name'].unique())
print('Parties of most recent decade of Congress:')
print(data_new['party_name'].unique())

stdev_DR = data_old['nominate_dim1'][data_old['party_name']=='Democrat-Republican'].std()
mean_DR  = data_old['nominate_dim1'][data_old['party_name']=='Democrat-Republican'].mean()
stdev_Fd = data_old['nominate_dim1'][data_old['party_name']=='Federalist'].std()
mean_Fd  = data_old['nominate_dim1'][data_old['party_name']=='Federalist'].mean()

stdev_D = data_new['nominate_dim1'][data_new['party_name']=='Democrat'].std()
mean_D  = data_new['nominate_dim1'][data_new['party_name']=='Democrat'].mean()
stdev_R = data_new['nominate_dim1'][data_new['party_name']=='Republican'].std()
mean_R  = data_new['nominate_dim1'][data_new['party_name']=='Republican'].mean()

def calcXYnorm(std_dev, mean):
    x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 1000)
    y = (1/(std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)
    return x,y

x_DR,y_DR = calcXYnorm(stdev_DR, mean_DR)
x_Fd,y_Fd = calcXYnorm(stdev_Fd, mean_Fd)
x_D,y_D = calcXYnorm(stdev_D, mean_D)
x_R,y_R = calcXYnorm(stdev_R, mean_R)

plt.plot(x_D, y_D, color='#0000FF', label='Democrat')
plt.fill_between(x_D, y_D, color='#0000FF', alpha=0.1)

plt.plot(x_R, y_R, color='#FF0000', label='Republican')
plt.fill_between(x_R, y_R, color='#FF0000', alpha=0.1)

plt.plot(x_DR, y_DR, color='#007FFF', label='Democratic Republican')
plt.fill_between(x_DR, y_DR, color='#007FFF', alpha=0.4)

plt.plot(x_Fd, y_Fd, color='#FF7F00', label='Federalist')
plt.fill_between(x_Fd, y_Fd, color='#FF7F00', alpha=0.4)


plt.xlim(-1, 1)
plt.title('Normal Distribution')
plt.xlabel('X')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True)
plt.show()




