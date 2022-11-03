This is an implementation of the group recommender algorithms described by Ortega et al. (2016) a the paper titled ["Recommending items to group of users using Matrix Factorization based Collaborative Filtering"](https://www.sciencedirect.com/science/article/pii/S0020025516300196). The base MF algorithms was inspired by [ExplicitMF](https://www.ethanrosenthal.com/2016/01/09/explicit-matrix-factorization-sgd-als/).

# How to use

1. Put the trained MF model in the data folder (for example "../../data/model_sgd_mf_v4_50__1666837325.pkl"), same thing for anime_encoder.csv, and group rating file ("../../data/group_rating_real.csv"). 
2. Run group_mf_development.ipynb

