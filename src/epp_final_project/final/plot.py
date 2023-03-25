

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



# plotting_monte_carlo(
# def plot_compare(data, column_list, label_name, c_values):


# def plotting_monte_carlo(data, column_list, label_name):


# def plot_monte_carlo(data):

#     # Plot each distribution
#     for element, name in zip(column_list, label_name):
#         sns.distplot(data[element], hist = False, kde = True,
#                     label = name, ax = axes[i])

#     # # Plot formatting


# """Functions plotting results."""


# def plot_regression_by_age(data, data_info, predictions, group):
#     """Plot regression results by age.

#     Args:
#         data (pandas.DataFrame): The data set.
#         data_info (dict): Information on data set stored in data_info.yaml. The
#             following keys can be accessed:
#             - 'outcome': Name of dependent variable column in data
#             - 'outcome_numerical': Name to be given to the numerical version of outcome
#             - 'columns_to_drop': Names of columns that are dropped in data cleaning step
#             - 'categorical_columns': Names of columns that are converted to categorical
#             - 'column_rename_mapping': Old and new names of columns to be renamend,
#                 stored in a dictionary with design: {'old_name': 'new_name'}
#             - 'url': URL to data set
#         predictions (pandas.DataFrame): Model predictions for different age values.
#         group (str): Categorical column in data set. We create predictions for each
#             unique value in column data[group]. Cannot be 'age' or 'smoke'.

#     Returns:
#         plotly.graph_objects.Figure: The figure.

#     """


#         plot_data,

#     fig.add_traces(
#         go.Scatter(
#         ),
