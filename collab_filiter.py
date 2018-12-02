class CollaborativeFilter:
    def __init__(self, csvfile, k = 3):
        self.user_ratings_dict = dict() #Dictionary of dictionary of user ratings ({user_id : {MovieID (string) : rating(float)}})
        self.average_movie_ratings = dict()
        self.weights = dict() # (movieID_i, moveID_j)(tuple) : weight (flaot)
                              ## The smaller movieID is first
        self.k = k
        self.readInCsv(csvfile)
        self.computWeights()
        

    def readInCsv(self, csvfile):
        print("READING IN DATA...")
        movie_ratings = dict() #Stores the total amount that this user has given in ratings
        with open(csvfile) as datafile:
            row = datafile.readline()

            while row:
                movieID, userID, rating = row.split(",") # FORMAT: MovieID,UserID,Rating
                
                #Remove newline
                if "\n" in rating:
                    rating = rating[:-1]

                rating = float(rating)

                if userID not in self.user_ratings_dict:
                    self.user_ratings_dict[userID] = dict()

                self.user_ratings_dict[userID][movieID] = rating # Add a user rating
                
                if movieID not in movie_ratings:
                    movie_ratings[movieID] = list()
                movie_ratings[movieID].append(rating)

                row = datafile.readline()
        
        self.computeAverageMovieRatings(movie_ratings)

    def computeAverageMovieRatings(self, movie_ratings):
        for moveID, ratings in movie_ratings.items():
            self.average_movie_ratings[moveID] = sum(ratings) / len(ratings)

    def computWeights(self):
        print("COMPUTING WEIGHTS...")
        print("(This may take a few seconds)")
        for movieID_i, avg_rating_i in self.average_movie_ratings.items():
            for movieID_j, avg_rating_j in self.average_movie_ratings.items():
                if movieID_i == movieID_j:
                    continue
                if (movieID_i, movieID_j) in self.weights or (movieID_j, movieID_i) in self.weights:
                    continue
                
                users = self.findUsersWhoRatedBoth(movieID_i, movieID_j)
                weight = 0
                if users:    
                    # The actual weight computation for movieID_i and moveieID_j
                    numer = denom_i = denom_j = 0        
                    for userID in users:
                        diff_i = self.user_ratings_dict[userID][movieID_i] - avg_rating_i
                        diff_j = self.user_ratings_dict[userID][movieID_j] - avg_rating_j
                        numer +=  diff_i * diff_j
                        denom_i += diff_i ** 2
                        denom_j += diff_j ** 2
                    if denom_i == 0 or denom_j == 0:
                        weight = 0
                    else:
                        weight = numer / ( ( denom_i ** 0.5) * ( denom_j ** 0.5 ) )
                        #if weight < 0:
                        #   print("MOVIE 1: ", movieID_i, " MOVIE 2: ", movieID_j, weight)
                    
                # Storing the weight
                if int(movieID_i) < int(movieID_j):
                    self.weights[(movieID_i, movieID_j)] = weight
                else:
                    self.weights[(movieID_j, movieID_i)] = weight

    def predict(self, userID, movieID):
        if userID not in self.user_ratings_dict:
            print("ERROR: INVALID USER ID")
            return -1
        elif movieID in self.user_ratings_dict[userID]:
            print("ERROR: User has already given this movie a rating of ", self.user_ratings_dict[userID][movieID])
            return -1
        elif movieID not in self.average_movie_ratings.keys():
            print("ERROR: INVALID MOVIE ID")
            return -1
        
        print("PREDICTING RATING...")
        return self.predictRating(userID, self.findKNearestWeights(userID, movieID))

    def findKNearestWeights(self, userID, movieID_i):
        k = min(self.k, len(self.user_ratings_dict[userID])) # k can't be greater than the number of ratings the user has made
        user_rating_weights = [] # The weights of the movies that the user has rated

        for movieID_j, rating in self.user_ratings_dict[userID].items():
            if int(movieID_i) < int(movieID_j):
                movie_tuple = (movieID_i, movieID_j)
            else:
                movie_tuple = (movieID_j, movieID_i)
            if movie_tuple in self.weights:
                user_rating_weights.append( (rating, self.weights[movie_tuple]) )
            else:
                print("ERROR THIS SHOULDNT APPEAR")

        user_rating_weights_sorted = sorted(user_rating_weights, key=lambda d: d[1], reverse=True) # Sort by weight in ascending order
        return user_rating_weights_sorted[:k] # return the k closest weights
    
    def predictRating(self, userID, user_rating_weights):
        weight_sum = 0
        weighted_rating_sum = 0
        for rating, weight in user_rating_weights:
            weighted_rating_sum += rating * weight
            weight_sum += weight

        return weighted_rating_sum / weight_sum

    def findUsersWhoRatedBoth(self, movieID_i, movieID_j):
        users = []
        for userID, ratings_dict in self.user_ratings_dict.items():
            if movieID_i in ratings_dict and movieID_j in ratings_dict:
                users.append(userID)
        return users

def main():
    k_selected = False
    while not k_selected:
        try:
            init_k = 3
            init_k_ans = input("What value of k do you want to use?(default=3): ")
            if init_k_ans:
               init_k = int(init_k_ans) 
            if init_k <= 0:
                raise Exception("k must be greater than 0")
            k_selected = True
        except Exception as e:
            print("ERROR: ", e)
            print("Please enter a valid value for k")

    cf = CollaborativeFilter("data/data-full.txt")
    exit_ans_list = ["n", "no", "nope", "nah", "q", "quit", "exit", "stop", "probably not"]
    print("\nPreprocessing steps complete. You can now make predictions")
    print("-----------------------------------------------------------")
    while True:
        print()
        movieID = input("Please enter in a movie ID: ")
        userID = input("Please enter in a user ID: ")
        prediction = cf.predict(userID, movieID)
        if prediction != -1:
            print("Predicted rating: ", prediction)
        
        user_ans = input("Want to make another prediction?(y/n): ").lower()
        if user_ans in exit_ans_list or len(user_ans) == 0:
            print("Goodbye.")
            break

if __name__ == "__main__":
    main()