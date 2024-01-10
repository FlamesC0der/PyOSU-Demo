def get_rating(score, rating_scale):
    for threshold, grade in sorted(rating_scale.items(), reverse=True):
        if score >= threshold:
            return grade
