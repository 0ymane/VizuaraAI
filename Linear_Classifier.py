import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt

    return (np,)


@app.cell
def _(np):
    np.random.seed(0)
    return


@app.cell
def _(np):
    # Dogs: higher ears flapiness index with lower whisker length
    dogs_whisker_length = np.random.normal(loc=5, scale=1, size=10)
    dogs_ear_flappiness_index = np.random.normal(loc=8, scale=1, size=10)
    return


@app.cell
def _(np):
    # Cats: lower ears flapiness index and higher whisker length
    cats_whisker_length = np.random.normal(loc=5, scale=1, size=10)
    cats_ears_flapiness_index = np.random.normal(loc=5, scale=1, size=10)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
