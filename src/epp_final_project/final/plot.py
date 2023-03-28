def plotting_monte_carlo(data, column_list, label_name):
    """A function to produce density plot from certain columns in a dataframe by also
    assigning labels.

    Args:
        data (dataframe): A dataframe that contains estimates
        column_list (list): A list that contains the names of the columns
        label_name (list): A list that contains the labels we want to assign
        for the respective columns

    Returns:
        A density plot.

    """
    df = data
    ax = df[column_list].plot.density(linewidth=2)
    ax.legend(label_name, prop={"size": 10}, title="Estimator", title_fontsize=10)
    ax.set_xlabel("")
    ax.tick_params(axis="both", which="major", labelsize=10)
    ax.set_ylabel("")
    ax.axvline(5, color="midnightblue")
    ax.set_ylim(bottom=0)
    return ax
