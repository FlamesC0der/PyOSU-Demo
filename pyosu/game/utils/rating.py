def get_rating(score: int, rating_scale: dict):
    for threshold, grade in sorted(rating_scale.items(), reverse=True):
        if score >= threshold:
            return grade
