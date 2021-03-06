import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import integrate


def capPlot(y_values, y_preds_proba, column, percent=0.5):
    y_cap = np.c_[y_values, y_preds_proba]
    y_cap_df_s = pd.DataFrame(data=y_cap)
    y_cap_df_s = y_cap_df_s.sort_values([1], ascending=False).reset_index(level=y_cap_df_s.index.names, drop=True)

    num_pos_obs = np.sum(y_values)
    num_count = len(y_values)

    xx = np.arange(num_count) / float(num_count - 1)
    yy = np.cumsum(y_cap_df_s[0]) / float(num_pos_obs)
    yy = np.append([0], yy[0:num_count - 1])  # add the first curve point (0,0) : for xx=0 we have yy=0

    row_index = int(np.trunc(num_count * percent))
    val_y1 = yy[row_index]
    val_y2 = yy[row_index + 1]
    if val_y1 == val_y2:
        val = val_y1 * 1.0
    else:
        val_x1 = xx[row_index]
        val_x2 = xx[row_index + 1]
        val = val_y1 + ((val_x2 - percent) / (val_x2 - val_x1)) * (val_y2 - val_y1)

    sigma_ideal = 1 * xx[num_pos_obs - 1] / 2 + (xx[num_count - 1] - xx[num_pos_obs]) * 1
    sigma_model = integrate.simps(yy, xx)
    sigma_random = integrate.simps(xx, xx)
    ar_value = (sigma_model - sigma_random) / (sigma_ideal - sigma_random)

    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(xx, yy, color='red', label=column)
    ax.plot(xx, xx, color='blue', label='Random Model')
    ax.plot([percent, percent], [0.0, val], color='green', linestyle='--', linewidth=1)
    ax.plot([0, percent], [val, val], color='green', linestyle='--', linewidth=1,
            label=str(int(val * 100)) + '% of positive obs at ' + str(percent * 100) + '%')
    plt.xlim(0, 1.02)
    plt.ylim(0, 1.02)
    plt.title("CAP Curve - a_r value = %.2f" % ar_value)
    plt.xlabel('% of the data')
    plt.ylabel('% of positive obs')
    plt.legend()
    plt.show()
    return


if __name__ == "__main__":
    df = pd.read_csv("E:\\Download\\query-impala-78565.csv")
    y1 = df.loc[:, ["label"]].values
    y2 = df.loc[:, ["prediction"]].values
    capPlot(y1, y2, "prediction")
