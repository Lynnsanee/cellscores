from matplotlib import pyplot as plt

def generate_plot(enl, res, output_name, cell):

    x_labels = [0, 5, 10, 15, 20, 25, 30, 35]
    x_spread = []
    for i in range (0, len(enl)):
        x_spread.append(i)

    plt.plot(x_spread, res,  color='blue')
    plt.plot(x_spread, enl,  color="green")
    plt.fill_between(x_spread, res, color="blue", alpha=0.4)
    plt.fill_between(x_spread, enl, color="lightgreen", alpha=0.4)
    plt.grid(axis="y", linestyle="dotted")

    plt.xticks(x_labels)
    plt.xlabel("Checkpoints")
    plt.ylabel("MU")
    plt.title(f"{output_name} {cell}")
    plt.ticklabel_format(useOffset=False, style="plain")
    plt.savefig(f"{output_name}.png")
    plt.close()
