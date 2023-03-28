"""Tests for the simulation result."""

import numpy as np
import pytest

from src.epp_final_project.analysis.model import _covariance, _x_init, compare_est


# ===============================================
# FIXTURES
# ===============================================
@pytest.fixture()
def inputs_cov():
    return {"rng": np.random.default_rng(925408), "n_params": 6}


@pytest.fixture()
def inputs_x_init():
    return {
        "rng": np.random.default_rng(92),
        "mean": np.zeros(len(np.ones(6))),
        "cov": _covariance(rng=np.random.default_rng(925408), n_params=6),
        "n_obs": 50,
    }


@pytest.fixture()
def inputs_cunit():
    return {
        "n_sim": 50,
        "n_obs": 40,
        "true_params": np.ones(6),
        "seed": 3,
        "t_per": 10,
        "c_unit": 0.4,
        "c_time": 0,
        "c_trend": 0,
        "c_var": 0.25,
    }


@pytest.fixture()
def inputs_cvar():
    return {
        "n_sim": 50,
        "n_obs": 40,
        "true_params": np.ones(6),
        "seed": 3,
        "t_per": 10,
        "c_unit": 0.4,
        "c_time": 0,
        "c_trend": 0,
        "c_var": 0.05,
    }


@pytest.fixture()
def inputs_ctrend():
    return {
        "n_sim": 50,
        "n_obs": 40,
        "true_params": np.ones(6),
        "seed": 3,
        "t_per": 10,
        "c_unit": 0.4,
        "c_time": 0,
        "c_trend": 0.5,
        "c_var": 0.25,
    }


@pytest.fixture()
def inputs_ctime():
    return {
        "n_sim": 50,
        "n_obs": 40,
        "true_params": np.ones(6),
        "seed": 3,
        "t_per": 10,
        "c_unit": 0.4,
        "c_time": 0.3,
        "c_trend": 0,
        "c_var": 0.25,
    }


# ================================================
# TESTS
# ================================================
def test_cov(inputs_cov):
    cov = _covariance(**inputs_cov)
    assert np.all(np.linalg.eigvals(cov) > 0)


def test_x_init(inputs_x_init):
    x_init = _x_init(**inputs_x_init)
    assert x_init.shape == (50, 6)


def test_cunit(inputs_cunit):
    """The endogenous results should be bigger for pooled estimator in many case."""

    result = compare_est(**inputs_cunit)
    percent_larger = (result["beta_OLS"] > result["beta_one_way"]).mean()
    assert percent_larger > 0.9
    assert result["beta_one_way"].mean() == pytest.approx(1, abs=0.2)


def test_cvar(inputs_cvar):
    """Due to low variation across time variance of two-way estimator should be bigger
    than both of the other estimators."""

    result = compare_est(**inputs_cvar)
    assert result["beta_two_way"].var() > result["beta_one_way"].var()
    assert result["beta_two_way"].var() > result["beta_OLS"].var()


def test_ctrend(inputs_ctrend):
    """When there is a high trend other estimators should break down except two-way
    estimator."""

    result = compare_est(**inputs_ctrend)
    assert result["beta_two_way"].var() < result["beta_one_way"].var()
    assert result["beta_two_way"].var() < result["beta_OLS"].var()


def test_ctime(inputs_ctime):
    """When there is an endogenous time constant two-way estimator should perform
    better."""

    result = compare_est(**inputs_ctime)
    assert abs(result["beta_two_way"].mean() - 1) < abs(
        result["beta_one_way"].var() - 1,
    )
    assert abs(result["beta_two_way"].mean() - 1) < abs(result["beta_OLS"].var() - 1)
    assert result["beta_two_way"].mean() == pytest.approx(1, abs=0.2)
