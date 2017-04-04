import matplotlib
import matplotlib.pyplot as plt


def save_and_close_fig(fig, filebasename, exts=['.png', '.eps', '.svg'], dpi=100):
    for ext in exts:
        filepath = filebasename + ext
        plt.savefig(filepath, dpi=100)
    plt.close()
