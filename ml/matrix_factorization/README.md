This is an implementation of the group recommender algorithms described by Ortega et al. (2016) a the paper titled ["Recommending items to group of users using Matrix Factorization based Collaborative Filtering"](https://www.sciencedirect.com/science/article/pii/S0020025516300196). The base MF algorithms was inspired by [ExplicitMF](https://www.ethanrosenthal.com/2016/01/09/explicit-matrix-factorization-sgd-als/).

# How to use

1. Put the trained MF model in the data folder (for example "../../data/model_sgd_mf_v4_50__1666837325.pkl"), same thing for anime_encoder.csv, and group rating file ("../../data/group_rating_real.csv"). 
2. Run group_mf_development.ipynb

# Approach

We use a 2 steps approach:

1. Step 1: Offline training:
- Train the model on the entire dataset to get a set of item embeddings. We use stochastic gradient descent to train a MF model with bias term (described in the paper).
- Each anime is represented by a 128-dimensional vector.

2. Step 2: Online calculation:
- Applying ridge regression (described in the paper) to find the embedding of the virtual user.
- Calculate predicted rating of the virtual user, filter to get the un-watched animes and return the top 10 recommendation.
