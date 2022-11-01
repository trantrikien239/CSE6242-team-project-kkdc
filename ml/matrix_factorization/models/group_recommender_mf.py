import numpy as np
from scipy.sparse import csr_matrix
from explicit_mf_with_bias import SGDExplicitBiasMF

class GroupRecommenderMF(SGDExplicitBiasMF):
    def __init__(self, **kwargs):
        self.global_bias = 0 # To implement
        self.item_embeddings = 0 # To implement, shape=(N_ITEM, D)
        self.item_bias = 0 # To implement
        self.n_items = self.item_embeddings
        pass

    def recommend_group(self, group_rating_df):
        """
        Input: group_rating_df (3 columns: user_name, item_id, rating)
        Say we have a group of 5 people: different names
        """
        self.n_users_in_group = int(group_rating_df["user_name"].nunique())
        group_rating_df_encoded = self.item_encode(group_rating_df)
        
        virtual_user_rating = self.agg_group(group_rating_df_encoded)
        virtual_user_embedding = self.train_virtual(virtual_user_rating)
        predicted_virtual = self.predict_vitual(virtual_user_embedding)
        top_10_encoded = self.sort_and_filter(predicted_virtual)
        top_10 = self.item_decode(top_10_encoded)
        return top_10

    def train_virtual(self, virtual_user_rating):
        """
        Input:
            - virtual_user_rating: Compressed Sparse Row matrix containing the rating 

        """
        raise NotImplementedError

    def agg_group(self, group_rating_df_encoded):
        """
        Input: group_rating_df_encoded (3 columns: user_name, item_id_encoded, rating)
        Output: 
            - virtual_user_rating: Compressed Sparse Row matrix containing the rating 
        """
        # virtual_user_rating = csr_matrix(
        #     (df_enc_train.rating, (df_enc_train.user_id, df_enc_train.anime_id)), 
        #     shape=(N_USER, N_ANIME))
        return virtual_user_rating

    
    def item_encode(self, group_rating_df):
        raise NotImplementedError