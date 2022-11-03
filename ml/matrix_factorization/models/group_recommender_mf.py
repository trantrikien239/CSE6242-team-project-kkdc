from turtle import shape
import numpy as np
from scipy.sparse import csr_matrix
import pandas as pd
import pickle

from .explicit_mf_with_bias import SGDExplicitBiasMF

class GroupRecommenderMF(SGDExplicitBiasMF):
    def __init__(self, full_model_file_path, item_encoder_file_path):
        with open(full_model_file_path, "rb") as f:
            mf_full_model = pickle.load(file=f)
        self.item_bias = mf_full_model.item_bias
        self.item_vecs = mf_full_model.item_vecs
        self.global_bias = mf_full_model.global_bias
        self.n_factors = mf_full_model.item_vecs.shape[1]
        self.item_encoder_df = pd.read_csv(item_encoder_file_path)
        self.item_encoder_df.rename(columns={
            "Orignal Id":"original_id",
            "Encoded Id":"encoded_id"
            }, inplace=True)
    

    def recommend_group(self, group_rating_df, reg):
        """
        Input: group_rating_df (3 columns: user_name, item_id, rating)
        Say we have a group of 5 people: different names
        """
        self.n_users_in_group = int(group_rating_df["user_name"].nunique())
        group_rating_df_encoded = self.item_encode(group_rating_df)
        
        virtual_user_rating = self.agg_group(group_rating_df_encoded)

        virtual_user_embedding, virtual_user_bias = self.train_virtual(
            virtual_user_rating, reg)
        predicted_virtual = self.predict_virtual(virtual_user_embedding, virtual_user_bias)
        df_top_10_encoded = self.sort_and_filter(predicted_virtual, virtual_user_rating)
        top_10 = self.item_decode(df_top_10_encoded)
        return top_10

    def item_decode(self, df_top_10_encoded):
        """
        Input:
            - df_top_10_encoded: (2, 10), columns = ["item_id_encoded", "rating"]
        Output:
            - top_10: (2, 10), columns = ["item_id", "rating"]
        """
        top_10 = df_top_10_encoded.merge(
            self.item_encoder_df, 
            left_on="item_id_encoded", 
            right_on="encoded_id"
            )
        top_10 = top_10[["original_id", "rating"]]
        top_10.rename(columns={
            "original_id":"item_id",
            "rating":"rating"
            }, inplace=True)
        top_10.sort_values(by="rating", ascending=False, inplace=True)
        return top_10

    def sort_and_filter(self, predicted_virtual, virtual_user_rating):
        """
        Input:
            - predicted_virtual: (1, n_items_all)
            - virtual_user_rating: Compressed Sparse Row matrix containing the rating 
                shape = (n_users_in_group + 1, n_items_all)
        Output:
            - df_top_10_encoded: (2, 10), columns = ["item_id_encoded", "rating"]
        """
        predicted_virtual = predicted_virtual.flatten()
        virtual_user_rating = virtual_user_rating.flatten()
        predicted_virtual[virtual_user_rating > 0] = -np.inf
        top_10_encoded = np.argsort(predicted_virtual)[-10:]
        top_10_rating = predicted_virtual[top_10_encoded]
        df_top_10_encoded = pd.DataFrame({
            'item_id_encoded': top_10_encoded,
            'rating': top_10_rating
        })
        return df_top_10_encoded

    def predict_virtual(self, virtual_user_embedding, virtual_user_bias):
        """`
        Input:
            - virtual_user_embedding: (1, n_factors)
            - virtual_user_bias: (1,1)
        Output:
            - predicted_virtual: (1, n_items_all)
        """
        predicted_virtual = self.global_bias + virtual_user_bias + \
            self.item_bias + virtual_user_embedding.dot(self.item_vecs.T)
        
        return predicted_virtual

    def train_virtual(self, virtual_user_rating, reg):
        """
        Input:
            - virtual_user_rating: Compressed Sparse Row matrix containing the rating 
                shape = (n_users_in_group + 1, n_items_all)
        """
        n_items_in_group = int((virtual_user_rating > 0).sum()) # num items that's rated by group users
        item_indices = np.argwhere(virtual_user_rating > 0)[:,1].flatten()
        r_ = np.array(virtual_user_rating.T[item_indices])[:,0].flatten()
        b_i_ = self.item_bias[item_indices]
        s_ = r_ - self.global_bias - b_i_
        s_ = s_.reshape(-1, 1)
        A_ = self.item_vecs[item_indices]
        A_ = np.hstack((A_, np.ones((n_items_in_group, 1))))

        pb_g = np.linalg.inv(
            A_.T.dot(A_) + reg * np.eye(N=self.n_factors+1)
            ).dot(A_.T).dot(s_) # (n_factors + 1,1)
        p_g = pb_g[:-1,0].T # (1, n_factors)
        b_g = pb_g[-1,0] # (1,1)
        
        return p_g, b_g

    def agg_group(self, group_rating_df_encoded):
        """
        Input: group_rating_df_encoded (3 columns: user_name, item_id_encoded, rating)
        Output: 
            - virtual_user_rating: Numpy array containing the rating, shape = (1, num_anime_total)
        """
        agg_df = group_rating_df_encoded.groupby("item_id")["rating"].mean()
        num_anime_total = self.item_vecs.shape[0]
        virtual_user_rating = np.zeros(shape=(num_anime_total, 1))
        virtual_user_rating[agg_df.index] = agg_df.values.reshape(-1,1)
        virtual_user_rating = virtual_user_rating.T
        return virtual_user_rating

    
    def item_encode(self, group_rating_df):
        """
        Keep consistent with encoding, access encoding dictionary
        """
        group_df = group_rating_df.copy()
        encode_df = self.item_encoder_df.set_index(
            "original_id")["encoded_id"].to_dict()
        group_df["item_id"] = group_df.item_id.apply(encode_df.get)

        return group_df