import pytask

from epp_final_project.analysis.model import compare_est
from epp_final_project.config import (
    BLD,
    c_time_values,
    c_trend_values,
    c_unit_values,
    c_var_values,
)

for c_unit in c_unit_values:
    kwargs = {
        "produces": BLD / "python" / "data" / "c_unit" / f"{c_unit}.csv",
        "group": c_unit,
    }

    @pytask.mark.task(kwargs=kwargs)
    def task_monte_carlo(produces, group):
        """Simulate the underlying model for different c_unit values."""
        df = compare_est(
            n_sim=25,
            n_obs=30,
            t_per=10,
            true_params=[1, 5, 3, 3, 3],
            c_unit=group,
            c_time=0,
            seed=42,
            c_trend=0,
            c_var=0.25,
        )
        df.to_csv(produces, index=False)


for c_var in c_var_values:
    kwargs = {
        "produces": BLD / "python" / "data" / "c_var" / f"{c_var}.csv",
        "group": c_var,
    }

    @pytask.mark.task(kwargs=kwargs)
    def task_monte_carlo(produces, group):
        """Simulate the underlying model for different c_var values."""
        df = compare_est(
            n_sim=25,
            n_obs=30,
            t_per=10,
            true_params=[1, 5, 3, 3, 3],
            c_unit=0.4,
            c_time=0,
            seed=42,
            c_trend=0,
            c_var=group,
        )
        df.to_csv(produces, index=False)


for c_trend in c_trend_values:
    kwargs = {
        "produces": BLD / "python" / "data" / "c_trend" / f"{c_trend}.csv",
        "group": c_trend,
    }

    @pytask.mark.task(kwargs=kwargs)
    def task_monte_carlo(produces, group):
        """Simulate the underlying model for different c_trend values."""
        df = compare_est(
            n_sim=25,
            n_obs=30,
            t_per=10,
            true_params=[1, 5, 3, 3, 3],
            c_unit=0.4,
            c_time=0,
            seed=42,
            c_trend=group,
            c_var=0.25,
        )
        df.to_csv(produces, index=False)


for c_time in c_time_values:
    kwargs = {
        "produces": BLD / "python" / "data" / "c_time" / f"{c_time}.csv",
        "group": c_time,
    }

    @pytask.mark.task(kwargs=kwargs)
    def task_monte_carlo(produces, group):
        """Simulate the underlying model for different c_time values."""
        df = compare_est(
            n_sim=25,
            n_obs=30,
            t_per=10,
            true_params=[1, 5, 3, 3, 3],
            c_unit=0.4,
            c_time=group,
            seed=42,
            c_trend=0,
            c_var=0.25,
        )
        df.to_csv(produces, index=False)
