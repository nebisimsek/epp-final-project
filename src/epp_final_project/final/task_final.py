import pandas as pd
import pytask

from epp_final_project.config import (
    BLD,
    c_time_values,
    c_trend_values,
    c_unit_values,
    c_var_values,
)
from epp_final_project.final.plot import plotting_monte_carlo

for c_unit in c_unit_values:
    kwargs = {
        "group": c_unit,
        "depends_on": BLD / "python" / "data" / "c_unit" / f"{c_unit}.csv",
        "produces": BLD / "python" / "figures" / "c_unit" / f"{c_unit}.png",
    }

    @pytask.mark.task(kwargs=kwargs)
    def task_plot_results(depends_on, group, produces):
        """Plot the simulation results for different c_unit values."""
        column_list = ["beta_OLS", "beta_one_way", "beta_two_way"]
        label_name = ["Pooled", "one-way", "two-way"]
        data = pd.read_csv(depends_on)
        ax = plotting_monte_carlo(
            data=data,
            column_list=column_list,
            label_name=label_name,
        )
        ax.set_title(rf"$c_{{unit}}=${group}", fontsize=15)
        ax.figure.savefig(produces)


for c_time in c_time_values:
    kwargs = {
        "group": c_time,
        "depends_on": BLD / "python" / "data" / "c_time" / f"{c_time}.csv",
        "produces": BLD / "python" / "figures" / "c_time" / f"{c_time}.png",
    }

    @pytask.mark.task(kwargs=kwargs)
    def task_plot_results(depends_on, group, produces):
        """Plot the simulation results for different c_time values."""
        column_list = ["beta_OLS", "beta_one_way", "beta_two_way"]
        label_name = ["Pooled", "one-way", "two-way"]
        data = pd.read_csv(depends_on)
        ax = plotting_monte_carlo(
            data=data,
            column_list=column_list,
            label_name=label_name,
        )
        ax.set_title(rf"$c_{{time}}=${group}", fontsize=15)
        ax.figure.savefig(produces)


for c_var in c_var_values:
    kwargs = {
        "group": c_var,
        "depends_on": BLD / "python" / "data" / "c_var" / f"{c_var}.csv",
        "produces": BLD / "python" / "figures" / "c_var" / f"{c_var}.png",
    }

    @pytask.mark.task(kwargs=kwargs)
    def task_plot_results(depends_on, group, produces):
        """Plot the simulation results for different c_var values."""
        column_list = ["beta_OLS", "beta_one_way", "beta_two_way"]
        label_name = ["Pooled", "one-way", "two-way"]
        data = pd.read_csv(depends_on)
        ax = plotting_monte_carlo(
            data=data,
            column_list=column_list,
            label_name=label_name,
        )
        ax.set_title(rf"$c_{{var}}=${group}", fontsize=15)
        ax.figure.savefig(produces)


for c_trend in c_trend_values:
    kwargs = {
        "group": c_trend,
        "depends_on": BLD / "python" / "data" / "c_trend" / f"{c_trend}.csv",
        "produces": BLD / "python" / "figures" / "c_trend" / f"{c_trend}.png",
    }

    @pytask.mark.task(kwargs=kwargs)
    def task_plot_results(depends_on, group, produces):
        """Plot the simulation results for different c_trend values."""
        column_list = ["beta_OLS", "beta_one_way", "beta_two_way"]
        label_name = ["Pooled", "one-way", "two-way"]
        data = pd.read_csv(depends_on)
        ax = plotting_monte_carlo(
            data=data,
            column_list=column_list,
            label_name=label_name,
        )
        ax.set_title(rf"$c_{{trend}}=${group}", fontsize=15)
        ax.figure.savefig(produces)


# @pytask.mark.depends_on(BLD / "python" / "data" / "data_clean.csv")
# @pytask.mark.produces(BLD / "python" / "figures" / "heatmap.png")
# @pytask.mark.latex(script="document.tex", document="document.pdf")
# def task_compile_latex_document():
#     pass


# for c_trend in c_trend_values:
#     @pytask.mark.task(kwargs=kwargs)
#     def task_plot_results(depends_on, group, produces):


# for group in GROUPS:


#     @pytask.mark.depends_on(
#         },
#     @pytask.mark.task(id=group, kwargs=kwargs)
#     def task_plot_results_by_age_python(depends_on, group, produces):


# @pytask.mark.depends_on(BLD / "python" / "models" / "model.pickle")
# @pytask.mark.produces(BLD / "python" / "tables" / "estimation_results.tex")
# def task_create_results_table_python(depends_on, produces):
#     with open(produces, "w") as f:


# for values, names in zip(c_values, c_names):
#     for value in values:
#         @pytask.mark.task(kwargs=kwargs)
#         def task_plot_results(depends_on, produces, group):
#             """Plotting the densities of the respective columns."""
