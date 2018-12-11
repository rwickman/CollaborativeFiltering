# CollaborativeFiltering
## What is it?
It is an item-item collaborative filtering algorithm that is trained on a subset of the Netflix dataset. Given a valid user ID and movie ID it will use k-nearest neighbors algorithm to predict the rating that the user would give the movie.
## How to run
I built everthing from scratch so no dependencies required! Just do:
```python
python collab_filiter.py
```
1. Enter the a value of k to use (for the KNN algorithm). Just press enter if you want to use the default.
2. It will perfrom preprocessing steps, such as reading in the data and computing the weights. You may need to wait a few seconds for it to finish.
3. Enter a valid movie ID and user ID (these can be found in the dataset under data/data-full.txt).
4. If you did the previous steps correctly, then you should see a predicted rating! 
