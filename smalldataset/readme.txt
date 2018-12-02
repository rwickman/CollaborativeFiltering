data.txt format: movie-id,user-id,rating
predictions.txt format: movie-id,user-id,predicted_rating (I used all other items (with a valid non-zero weight) as neighbors for prediction since this is a small dataset)
Weights.txt format: movieid-movieid: weight (I used the python pearsonr function. This computes the correlation-coefficient only when there are more than 2 common users for a movie, also in cases where a user has the movie has the same rating by all users, the coefficient is returned as Nan which I have ignored)

Your results may vary from mine due to many reasons, don’t worry about it..this is just for a reference.