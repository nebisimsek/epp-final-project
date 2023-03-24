import math

import numpy as np
import pandas as pd


# Covariance function
def _covariance(rng, n_params):
    """A function that creates a covariance matrix.

    Args:
        rng (obj): random generator
        n_params (int): number of parameters.

    Returns:
        A covariance matrix.

    """
    helper = rng.uniform(low=-1, high=1, size=(n_params, n_params))
    return helper @ helper.T + np.eye(n_params)


# Generating initial x covariates
def _x_init(rng, mean, cov, n_obs):
    """A function that generates data from multivariate normal distribution .

    Args:
        rng (obj): random generator
        mean (array): the mean of X values
        cov (array): the covariance matrix
        n_obs (int): number of observations.

    Returns:
        A dataframe for number of n_obs.

    """
    x_initial = pd.DataFrame(rng.multivariate_normal(mean=mean, cov=cov, size=n_obs))
    return x_initial


# Generating variation over time
def _x_time(rng, mean, cov, t_per):
    """A function that generates data for variation over time .

    Args:
        rng (obj): random generator
        mean (array): the mean of X values
        cov (array): the covariance matrix
        t_per(int): the number of periods

    Returns:
        A dataframe for number of n_obs.

    """
    x_time = pd.DataFrame(rng.multivariate_normal(mean=mean, cov=cov, size=t_per))
    return x_time


# Function for panel data
def _xpanel(x_initial, x_time, t_per, rng, mean, cov, n_obs, c_var):
    """A function that build a panel data for n_obs observations and t_per period.

    Args:
        x_initial(dataframe): initial x covariates
        x_time(dataframe): variations across time
        t_per(int): the number of periods
        rng (obj): random generator
        mean (array): the mean of X values
        cov (array): the covariance matrix
        n_obs (int): number of observations.
        c_var(int): correlation variables

    Returns:
        A data frame for n_obs and t_per periods.

    """
    x_panel = pd.DataFrame()
    for per in range(1, t_per + 1):
        x = (
            x_initial
            + x_time.loc[per - 1, :]
            + c_var
            * pd.DataFrame(rng.multivariate_normal(mean=mean, cov=cov, size=n_obs))
        )
        # + c_trend*per*x_trend
        x["time"] = per
        x["obs"] = np.arange(1, (n_obs + 1))
        x_panel = pd.concat([x_panel, x])
    return x_panel.set_index("time")


def _transform_one_way(x, n_obs, t_per):
    """A function that makes one way transformation.

    Args:
        x(dataframe): panel data
        n_obs (int): number of observations
        t_per(int): the number of periods

    Returns:
        one-way transformed dataframe for n_obs and t_per periods.

    """
    x_df = x.copy()
    x_df["obs"] = np.tile(np.arange(1, (n_obs + 1)), t_per)
    x_mean = x_df.groupby("obs").mean()
    x_panel_mean = pd.DataFrame(np.tile(x_mean, (t_per, 1)))
    return x_df.drop("obs", axis=1) - x_panel_mean


# Define function for two-way transformation
def _transform_two_way(x, n_obs, t_per):
    """A function that makes two way transformation.

    Args:
        x(dataframe): panel data
        n_obs (int): number of observations
        t_per(int): the number of periods

    Returns:
        two-way transformed dataframe for n_obs and t_per periods.

    """
    # Generate the columns that tell observation and the time
    x_df = x.copy()
    x_df["obs"] = np.tile(np.arange(1, (n_obs + 1)), t_per)
    x_df["time"] = np.repeat(np.arange(0, t_per), n_obs)

    # Averaged each unit over time
    x_mean_unit = x_df.drop("time", axis=1).groupby("obs").mean()
    x_panel_unit = pd.DataFrame(np.tile(x_mean_unit, (t_per, 1)))

    # Averaged each time over unit
    x_mean_time = x_df.drop("obs", axis=1).groupby("time").mean()
    x_panel_time = pd.DataFrame(np.repeat(x_mean_time.values, n_obs, axis=0))

    # Transforming
    return (
        x_df.drop(["time", "obs"], axis=1)
        - x_panel_unit
        - x_panel_time
        + x_df.drop(["time", "obs"], axis=1).mean()
    )


# Function for additive time trend structure
def _time_trend(n_obs, rng, t_per, c_trend, seed):
    """A function that generates time trend.

    Args:
        n_obs (int): number of observations
        rng (obj): random generator
        t_per(int): the number of periods
        c_trend(int): trend constant

    Returns:
        two-way transformed dataframe for n_obs and t_per periods.

    """
    rng = np.random.default_rng(seed)
    # Generate the normally distributed w
    tw_i = []
    w_i = rng.normal(2, 0.5, size=n_obs)
    for k in range(1, t_per + 1):
        tw_i.extend(np.multiply(w_i, k * c_trend))
    return np.array(tw_i)


# Generate error terms and structure the y values
def _error_terms(
    x_panel,
    x_initial,
    x_time,
    rng,
    n_obs,
    t_per,
    c_unit,
    c_time,
    n_params,
    true_params,
    c_trend,
    seed,
):
    """A function that generates error terms.

    Args:
        x_panel(dataframe): panel data
        x_initial(dataframe): initial x covariates
        x_time(dataframe): variations across time
        rng (obj): random generator
        n_obs (int): number of observations.
        t_per(int): the number of periods
        c_unit(int): constant for unit endogeneity
        c_time(int): constant for time endogeneity
        n_params: number of parameters
        true_params: true parameters
        c_trend(int): trend constant

    Returns:
        a one dimensional dataframe that includes y values

    """
    # Generate time variant(epsilon_it) and time invariant(u_i) under fixed effect assumptions
    epsilon_it = rng.normal(size=n_obs * t_per)
    # Generate time invariant and unit invariant fixed error terms
    u_i = np.tile((x_initial[1] * c_unit) + rng.uniform(size=n_obs), t_per)
    v_t = np.repeat((x_time[1] * c_time) + rng.uniform(size=t_per), n_obs).to_numpy()
    tw_i = _time_trend(n_obs, rng, t_per, c_trend, seed)  # *x_panel[1] * 0.2
    # Extract x and y values
    x_panel_data = x_panel.loc[:, 0 : (n_params - 1)]
    return pd.DataFrame(x_panel_data @ true_params + u_i + v_t + tw_i + epsilon_it)


# Generate the function for OLS regression
def _est_OLS(y_it, x_panel, n_params):
    """A function for OLS regression and obtaining resulting estimaton.

    Args:
        y_it(dataframe): one-dimensional y dataframe
        x_panel(df): the panel data for X
        n_params (int): number of parameters.

    Returns:
        estimated parameter for the beta_1 and
        standard deviation for beta_1

    """
    # Assign the x and y values
    x_panel_data = x_panel.loc[:, 0 : (n_params - 1)]

    # Apply pooled estimator and show consistency, show how many times CI had the real Beta
    beta_est = np.linalg.inv(x_panel_data.transpose() @ x_panel_data) @ (
        x_panel_data.transpose() @ y_it
    )

    # Generate estimated y values
    y_est = x_panel_data @ beta_est

    # Extract errors
    e_it_sq = ((y_est - y_it) ** 2).iloc[:, 0]

    # Using theory obtain the covariance matrix
    var_pooled = (
        np.linalg.inv(x_panel_data.T @ x_panel_data)
        @ (x_panel_data.T @ np.diag(e_it_sq) @ x_panel_data)
        @ np.linalg.inv(x_panel_data.T @ x_panel_data)
    )

    # Extract the first value of the covariance matrix
    beta1_sd = math.sqrt(var_pooled.iloc[1, 1])
    return beta_est.loc[1, 0], beta1_sd


# Function one-way fixed error estimation
def _est_one_way(y_it, x_panel, n_obs, t_per, n_params):
    """"A function for one-way estimator.

    Args:
        y_it(dataframe): one-dimensional y dataframe
        x_panel(df): the panel data for X
        n_obs (int): number of observations.
        t_per(int): the number of periods
        n_params (int): number of parameters.

    Returns:
        estimated parameter for the beta_1 and
        standard deviation for beta_1

    """
    # Assign the x and y values
    x_panel_data = x_panel.loc[:, 0 : (n_params - 1)]

    # Transform x and y values
    x_panel_t = _transform_one_way(x_panel_data, n_obs, t_per=t_per)
    y_panel_t = _transform_one_way(y_it, n_obs, t_per=t_per)

    # Estimated values
    beta_est = np.linalg.inv(x_panel_t.transpose() @ x_panel_t) @ (
        x_panel_t.transpose() @ y_panel_t
    )

    # Generate estimated y values
    y_est = x_panel_data @ beta_est

    # Extract errors
    e_est_sq = ((y_est - y_it) ** 2).iloc[:, 0]

    # Using theory obtain the covariance matrix
    var_fixed = (
        np.linalg.inv(x_panel_t.T @ x_panel_t)
        @ (x_panel_t.T @ np.diag(e_est_sq) @ x_panel_t)
        @ np.linalg.inv(x_panel_t.T @ x_panel_t)
    )

    # Extract the first value of the covariance matrix
    beta1_sd = math.sqrt(var_fixed.iloc[1, 1])
    return beta_est.loc[1, 0], beta1_sd


def _est_two_way(y_it, x_panel, n_obs, t_per, n_params):
    """"A function for two-way estimator.

    Args:
        y_it(dataframe): one-dimensional y dataframe
        x_panel(df): the panel data for X
        n_obs (int): number of observations.
        t_per(int): the number of periods
        n_params (int): number of parameters.

    Returns:
        estimated parameter for the beta_1 and
        standard deviation for beta_1

    """
    # Generate the x and y variables
    x_panel_data = x_panel.loc[:, 0 : (n_params - 1)]

    # Transform x and y values
    x_panel_t = _transform_two_way(x_panel_data, n_obs, t_per)
    y_panel_t = _transform_two_way(y_it, n_obs, t_per)

    # Estimated values
    beta_est = np.linalg.inv(x_panel_t.transpose() @ x_panel_t) @ (
        x_panel_t.transpose() @ y_panel_t
    )

    # Generate estimated y values
    y_est = x_panel_data @ beta_est

    # Extract errors
    e_est_sq = ((y_est - y_it) ** 2).iloc[:, 0]

    # Using theory obtain the covariance matrix
    var_fixed = (
        np.linalg.inv(x_panel_t.T @ x_panel_t)
        @ (x_panel_t.T @ np.diag(e_est_sq) @ x_panel_t)
        @ np.linalg.inv(x_panel_t.T @ x_panel_t)
    )

    # Extract the first value of the covariance matrix
    beta1_sd = math.sqrt(var_fixed.iloc[1, 1])
    return beta_est.loc[1, 0], beta1_sd


def _CI(beta, sd):
    """Function to create dataframe from lists and create CI for the beta_1 estimate.

    Args:
        beta(float): The estimate of beta for each simulation
        sd(float): The estimate for standard deviation for each sim.

    Returns:
        two arrays that consists of upper and lower limit of
        Confidence Intervals

    """
    # Generate the bounds for Confidence Intervals
    CI_upper = np.add(beta, np.multiply(sd, 1.96))
    CI_lower = np.add(beta, np.multiply(sd, -1.96))
    return CI_upper, CI_lower


def compare_est(
    n_sim=500,
    n_obs=200,
    true_params=np.ones(6),
    seed=3,
    t_per=40,
    c_unit=0.4,
    c_time=0.4,
    c_trend=0.3,
    c_var=0.15,
):
    """A function to compare three different estimators given different parameters.

    Args:
        n_sim (int): number of simulations
        n_obs (int): number of observations.
        true_params (int): The real value of parameters
        seed(int): seed for drawing random numbers.
        t_per(int): the number of periods
        c_unit(int): constant for unit endogeneity
        c_time(int): constant for time endogeneity
        c_trend(int): trend constant
        c_var(int): variation factor over time

    Returns:
        A dataframe that contains estimates for beta_1

    """
    # Assign mean and covariance matrix to X values
    n_params = len(true_params)
    mean = np.zeros(n_params)
    rng = np.random.default_rng(seed)
    cov = _covariance(rng, n_params)

    beta_OLS = []
    beta_sd_OLS = []
    rmse_OLS = []

    beta_one_way = []
    beta_sd_one_way = []
    rmse_one_way = []

    beta_two_way = []
    beta_sd_two_way = []
    rmse_two_way = []

    for _ in range(n_sim):
        # Generate initial X values
        x_initial = _x_init(rng, mean, cov, n_obs)
        x_time = _x_time(rng, mean, cov, t_per)

        # Generate X values for n observations and for t time
        x_panel = _xpanel(
            x_initial,
            x_time,
            t_per,
            rng,
            mean,
            cov,
            n_obs,
            c_var,
        ).reset_index()
        y_it = _error_terms(
            x_panel,
            x_initial,
            x_time,
            rng,
            n_obs,
            t_per,
            c_unit,
            c_time,
            n_params,
            true_params,
            c_trend,
            seed,
        )

        # Apply OLS estimator
        beta_est_OLS, sd_OLS = _est_OLS(y_it, x_panel, n_params)

        # Apply one-way fixed effect estimator
        beta_est_one_way, sd_one_way = _est_one_way(
            y_it,
            x_panel,
            n_obs,
            t_per,
            n_params,
        )

        # Apply two-way fixed effect estimator
        beta_est_two_way, sd_two_way = _est_two_way(
            y_it,
            x_panel,
            n_obs,
            t_per,
            n_params,
        )

        # Storing \beta_1 OLS info
        beta_OLS.append(beta_est_OLS)
        beta_sd_OLS.append(sd_OLS)
        rmse_OLS.append((beta_est_OLS - true_params[1]) ** 2)

        # Storing beta_1 one-way info
        beta_one_way.append(beta_est_one_way)
        beta_sd_one_way.append(sd_one_way)
        rmse_one_way.append((beta_est_one_way - true_params[1]) ** 2)

        # Storing beta_1 two-way info
        beta_two_way.append(beta_est_two_way)
        beta_sd_two_way.append(sd_two_way)
        rmse_two_way.append((beta_est_two_way - true_params[1]) ** 2)

    CI_upper_OLS, CI_lower_OLS = _CI(beta=beta_OLS, sd=beta_sd_OLS)
    CI_upper_one_way, CI_lower_one_way = _CI(beta=beta_one_way, sd=beta_sd_one_way)
    CI_upper_two_way, CI_lower_two_way = _CI(beta=beta_two_way, sd=beta_sd_two_way)

    dict = {
        "beta_OLS": beta_OLS,
        "beta_sd_OLS": beta_sd_OLS,
        "rmse_OLS": rmse_OLS,
        "CI_upper_OLS": CI_upper_OLS,
        "CI_lower_OLS": CI_lower_OLS,
        "beta_one_way": beta_one_way,
        "beta_sd_one_way": beta_sd_one_way,
        "rmse_one_way": rmse_one_way,
        "CI_upper_one_way": CI_upper_one_way,
        "CI_lower_one_way": CI_lower_one_way,
        "beta_two_way": beta_two_way,
        "beta_sd_two_way": beta_sd_two_way,
        "rmse_two_way": rmse_two_way,
        "CI_upper_two_way": CI_upper_two_way,
        "CI_lower_two_way": CI_lower_two_way,
    }
    df = pd.DataFrame(dict)

    return df


# Run the function with default values
if __name__ == "__main__":
    result = compare_est(
        n_sim=50,
        n_obs=100,
        true_params=np.ones(6),
        seed=3,
        t_per=10,
        c_unit=0.4,
        c_time=0.4,
        c_trend=0.3,
    )
