# pylint: disable=E0401
"""Recommendation service."""

from typing import List

import numpy as np
from core.config import TOP_K, embedd_metadata, embeded_images, labels, map_track_ids


class RecommendationService:
    """Recommendation service."""

    def __init__(self):
        pass

    @staticmethod
    def get_recommendation(track_id: str, existed_ids: List[str] = None) -> List[str]:
        """Get recommendation."""
        prediction_anchor_1, prediction_anchor_2 = [], []
        prediction_songs = []
        predictions_metadata = []
        predictions_label = []
        distance_array = []
        list_recommend_ids = []
        recommendations = 0

        # Calculate the latent feature vectors for all the songs.
        for idx, label in enumerate(labels):
            if label == map_track_ids[track_id]:
                prediction_anchor_1 = embeded_images[idx]
                prediction_anchor_2 = embedd_metadata[label]
            else:
                predictions_label.append(label)
                prediction_songs.append(embeded_images[idx])
                predictions_metadata.append(embedd_metadata[label])
        prediction_anchor_2 = np.array(prediction_anchor_2)
        predictions_metadata = np.array(predictions_metadata)

        # Count is used for averaging the latent feature vectors.
        for idx, prediction_song in enumerate(prediction_songs):
            # Cosine Similarity - Computes a similarity score of all songs with respect
            # to the anchor song.
            distance_1 = np.sum(prediction_anchor_1 * prediction_song) / (
                np.sqrt(np.sum(prediction_anchor_1**2)) * np.sqrt(np.sum(prediction_song**2))
            )
            distance_2 = np.sum(prediction_anchor_2 * predictions_metadata[idx]) / (
                np.sqrt(np.sum(prediction_anchor_2**2)) * np.sqrt(np.sum(predictions_metadata[idx] ** 2))
            )
            distance_array.append(distance_1 * 0.6 + distance_2 * 0.4)

        distance_array = np.array(distance_array)

        while recommendations < TOP_K:
            index = np.argmax(distance_array)
            if (
                predictions_label[index] != map_track_ids[track_id]
                and predictions_label[index] not in list_recommend_ids
                and predictions_label[index] not in existed_ids
            ):
                list_recommend_ids.append(predictions_label[index])
                recommendations = recommendations + 1

            distance_array[index] = -np.inf

        return list_recommend_ids


recommendation_service = RecommendationService()
