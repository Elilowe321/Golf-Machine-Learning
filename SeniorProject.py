#Takes in player name, year, and first three scores of a tournament then predicts the last day with different ML models
import requests
import time
import json
import csv
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.svm import SVC, SVR
from lightgbm import LGBMClassifier, LGBMRegressor
import joblib

class player:


    def __init__(self):
        self.name = None
        self.height = None
        self.weight = None
        self.country = None
        self.id = None

    #Print out obj
    def __str__(self):
        return f"player(name={self.name}, height={self.height}, weight={self.weight}, country={self.country}, id={self.id})"

    #Getter methods
    def get_name(self):
        return self.name
    def get_height(self):
        return self.height
    def get_weight(self):
        return self.weight
    def get_country(self):
        return self.country
    def get_id(self):
        return self.id

    #Setter methods
    def name(self, value):
        self.name = value
    def height(self, value):
        self.height = value
    def weight(self, value):
        self.weight = value
    def country(self, value):
        self.country = value
    def id(self, value):
        self.id = value

class tournament_data:
    def __init__(self):
        self.name = None
        self.id = None
        self.day1 = None
        self.day2 = None
        self.day3 = None
        self.day4 = None
        self.par = None
        self.yardage = None
        self.rating = None
        self.written = None

    #Print out obj
    def __str__(self):
        return f"tournament_data(name={self.name}, id={self.id}), day1={self.day1}, day2={self.day2}, day3={self.day3}, day4={self.day4}"

    #Getter methods
    def get_name(self):
        return self.name
    def get_id(self):
        return self.id
    def get_day1(self):
        return self.day1
    def get_day2(self):
        return self.day2
    def get_day3(self):
        return self.day3
    def get_day4(self):
        return self.day4
    def get_par(self):
        return self.par
    def get_yardage(self):
        return self.yardage
    def get_rating(self):
        return self.rating

    #Setter methods
    def name(self, value):
        self.name = value
    def id(self, value):
        self.id = value
    def day1(self, value):
        self.day1 = value
    def day2(self, value):
        self.day2 = value
    def day3(self, value):
        self.day3 = value
    def day4(self, value):
        self.day4 = value
    def par(self, value):
        self.par = value
    def yardage(self, value):
        self.yardage = value
    def rating(self, value):
        self.rating = value

def predictions(filename, day1, day2, day3, fullname, tournament_name):
    # Load the data containing the first three rounds and the corresponding outcomes
    data = pd.read_csv(filename)  # Replace file with your actual data file
    tournament_data = pd.read_csv("CourseData.csv")

    #TODO:: If it is a major besides the masters, need to imput manually

    # Filter rows based on a condition (e.g., tournament_name equals "Tournament A")
    filtered_rows = tournament_data[tournament_data['Tournament Name'] == tournament_name]
    tourney_yardage = filtered_rows["Yardage"].values
    tourney_par = filtered_rows["Par"].values
    tourney_rating = filtered_rows["Rating"].values

    yarage_value = tourney_yardage[0]
    par_value = tourney_par[0]
    rating_value = tourney_rating[0]

    # Split the data into features (first three rounds) and target variable (fourth game outcome)
    #X = data[['day1', 'day2', 'day3', 'Yardage', 'Par', 'Rating']]
    #y = data['day4']
    X = data[['Yardage', 'Par', 'Rating']]
    y = data['day1']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.1, random_state=42)
    #new_game = [[day1, day2, day3, yarage_value, par_value, rating_value]]
    new_game = [[yarage_value, par_value, rating_value]]


    #LGBMClassifier, LGBMRegressor
    LGBMClassifier_model = LGBMClassifier()
    LGBMRegressor_model = LGBMRegressor()
    LGBMClassifier_model.fit(X_train.values, y_train)
    LGBMRegressor_model.fit(X_train.values, y_train)
    LGBMClassifier_model_prediction = LGBMClassifier_model.predict(new_game)
    LGBMRegressor_model_prediction = LGBMRegressor_model.predict(new_game)

    #SVC, SVR
    svc_model = SVC()
    svr_model = SVR()
    svc_model.fit(X_train.values, y_train)
    svr_model.fit(X_train.values, y_train)
    svc_model_prediction = svc_model.predict(new_game)
    svr_model_prediction = svr_model.predict(new_game)

    #RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
    random_forest_classifier_model = RandomForestClassifier()
    random_forest_regressor_model = RandomForestRegressor()
    gradien_boosting_classifier_model = GradientBoostingClassifier()
    gradient_boosting_regressor_model = GradientBoostingRegressor()
    random_forest_classifier_model.fit(X_train.values, y_train)
    random_forest_regressor_model.fit(X_train.values, y_train)
    gradien_boosting_classifier_model.fit(X_train.values, y_train)
    gradient_boosting_regressor_model.fit(X_train.values, y_train)
    random_forest_classifier_model_prediction = random_forest_classifier_model.predict(new_game)
    random_forest_regressor_model_prediction = random_forest_regressor_model.predict(new_game)
    gradien_boosting_classifier_model_prediction = gradien_boosting_classifier_model.predict(new_game)
    gradient_boosting_regressor_model_prediction = gradient_boosting_regressor_model.predict(new_game)

    #Linear
    linear_regression_model = LinearRegression()
    linear_regression_model.fit(X_train.values, y_train)
    linear_regression_model_prediction = linear_regression_model.predict(new_game)

    #Averages
    linear_average = (linear_regression_model_prediction[0])
    random_forest_average = (random_forest_classifier_model_prediction[0] + random_forest_regressor_model_prediction[0]) / 2
    gradient_boosting_average = (gradien_boosting_classifier_model_prediction[0] + gradient_boosting_regressor_model_prediction[0]) / 2
    SVM_average = (svc_model_prediction[0] + svr_model_prediction[0]) / 2
    LGBM_average = (LGBMClassifier_model_prediction[0] + LGBMRegressor_model_prediction[0]) / 2

    average = (linear_average + random_forest_average + gradient_boosting_average + LGBM_average + SVM_average) / 5

    filename = "FirstRoundPredictionsTest.csv"
    fieldnames = ["Name", "Lin Regression", "Random Forest Class", "Random Forest Regress", "Gradien Boost Class", "Gradien Boost Regress",
                  "SVC", "SVR", "LGBMClass", "LGBMRegress", "Linear Ave", "Random Forest Ave", "Gradien Boost Ave", "SVM Ave", 
                  "LGBM Ave", "Total Ave"]
    

    # Check if the file is empty
    file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0


    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header only if the file is empty
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "Name": fullname,
            "Lin Regression": linear_regression_model_prediction[0],
            "Random Forest Class": random_forest_classifier_model_prediction[0],
            "Random Forest Regress": random_forest_regressor_model_prediction[0],
            "Gradien Boost Class": gradien_boosting_classifier_model_prediction[0],
            "Gradien Boost Regress": gradient_boosting_regressor_model_prediction[0],
            "SVC": svc_model_prediction[0],
            "SVR": svr_model_prediction[0],
            "LGBMClass": LGBMClassifier_model_prediction[0],
            "LGBMRegress":LGBMRegressor_model_prediction[0],
            "Linear Ave": linear_average,
            "Random Forest Ave": random_forest_average,
            "Gradien Boost Ave": gradient_boosting_average,
            "SVM Ave": SVM_average,
            "LGBM Ave": LGBM_average,
            "Total Ave": average
        })
                
    print("CSV file created successfully.")
    
    #return svr_model_prediction[0]

    #MLP does different values every time
    print("Linear Regression Model = ", str(linear_regression_model_prediction[0]))
    print("Random Forest Classifier Model = ", str(random_forest_classifier_model_prediction[0]), "\nRandom Forest Regressor Model = ", str(random_forest_regressor_model_prediction[0]))
    print("Gradien Boosting Classifier Model = ", str(gradien_boosting_classifier_model_prediction[0]), "\nGradient Boosting Regressor Model = ", str(gradient_boosting_regressor_model_prediction[0]))
    print("SVC Model = ", str(svc_model_prediction[0]), "\nSVR Model = ", str(svr_model_prediction[0]))
    print("LGBMClassifier Model = ", str(LGBMClassifier_model_prediction[0]), "\nLGBMRegressor Model = ", str(LGBMRegressor_model_prediction[0]))

    print("Linear Average = " , linear_average)
    print("Random Forest Average = ", random_forest_average)
    print("Gradient Boosting Avergae = ", gradient_boosting_average)
    print("SVM Average = ", SVM_average)
    print("LGBM Average = ", LGBM_average)

    print("Total Average = " , average)
    

def data_retrieval(target_player_full_name, target_year, day1, day2, day3, tournament_name):

    names = target_player_full_name.split()  # Split the full name by whitespace

    first_name_initial = names[0][0]  # Extract the first letter of the first name
    last_name = names[-1] 
    csv_file = first_name_initial + "." + last_name + ".csv"
    course_data = pd.read_csv("CourseData.csv")
    
    #Already existing file for player
    if os.path.exists(csv_file):
        print("Loading Model...")
        return predictions(csv_file, day1, day2, day3, target_player_full_name, tournament_name)
    
    #No existing model
    else:
        #API for player ids
        print("Loading Model...")

        #TODO::Find way to get all player ids
        req_id = requests.get('http://api.sportradar.us/golf/trial/pga/v3/en/2023/players/profiles.json?api_key=ya2hjdx7bs68uk7mg8heexkw')
        time.sleep(1) # Wait for 1 second (can't do multiple api calls at once)

        player_obj = player()

        # Successful request
        if(req_id.status_code == 200): 
            id_data = req_id.json()

            #Get Player id
            for i in id_data["players"]:
                if(target_player_full_name == i["first_name"] + " " + i["last_name"]):
                    player_obj.name = i["abbr_name"]
                    player_obj.id = i["id"]
            print(player_obj.name)
        #Player not found
        if player_obj.name is None:
            error = "Player '" + target_player_full_name + "' Not Found"
            return error

        else:

            #API call to get all data for a player
            url = f'http://api.sportradar.us/golf/trial/v3/en/players/{player_obj.id}/profile.json?api_key=ya2hjdx7bs68uk7mg8heexkw'
            player_data = requests.get(url)
            if(player_data.status_code == 200): # Successful request
                player_data = player_data.json()
        
                #Get tournaments only in the correct year for specific player
                tournament_array = []
        
                for tournament in player_data["previous_tournaments"]:
                    seasons = tournament["seasons"]
                    for season in seasons: 
                        if(season["year"] == int(target_year)):
                                        
                            #Check if Cut PLyer is cut 
                            #position needs to be first or errors in reading
                            """
                            if(tournament["seasons"]["tour"]["alias"] == "LIV"):
                                tournament_obj = tournament_data()
                                tournament_obj.name = tournament["name"]

                                if(tournament_obj.name in course_data["Tournament Name"].values):
                                    print(tournament_obj.name)
                                   
                                    filtered_rows = course_data[course_data['Tournament Name'] == tournament_obj.name]

                                    # Iterate over the filtered rows and assign values to variables
                                    for index, row in filtered_rows.iterrows():
                                        tournament_obj.yardage = row['Yardage']
                                        tournament_obj.par = row['Par']
                                        tournament_obj.rating = row['Rating']
                                

                                    tournament_obj.id = tournament["id"]

                                    #Get strokes and stuff
                                    for i in range(0, 3):
                                        strokes_data = tournament["leaderboard"]["rounds"][i]
                                        setattr(tournament_obj, f"day{i+1}", strokes_data["strokes"])

                                    tournament_array.append(tournament_obj)
                            """
                            if("position" not in tournament["leaderboard"] or tournament["leaderboard"]["position"] > 72 or len(tournament["leaderboard"]["rounds"]) < 4):
                                # PLayer was cut, Do not use these data points
                                continue
                            else:  

                                #Get Tournament data 
                                #TODO:: Doesn't work for majors besides Masters
                                tournament_obj = tournament_data()
                                tournament_obj.name = tournament["name"]

                                if(tournament_obj.name in course_data["Tournament Name"].values):
                                    print(tournament_obj.name)
                                   
                                    filtered_rows = course_data[course_data['Tournament Name'] == tournament_obj.name]

                                    # Iterate over the filtered rows and assign values to variables
                                    for index, row in filtered_rows.iterrows():
                                        tournament_obj.yardage = row['Yardage']
                                        tournament_obj.par = row['Par']
                                        tournament_obj.rating = row['Rating']
                                

                                    tournament_obj.id = tournament["id"]

                                    #Get strokes and stuff
                                    for i in range(0, 4):
                                        strokes_data = tournament["leaderboard"]["rounds"][i]
                                        setattr(tournament_obj, f"day{i+1}", strokes_data["strokes"])

                                    tournament_array.append(tournament_obj)
                            
                #Put data into csv file
                filename = player_obj.name + ".csv"
                fieldnames = ["Tournament Name", "day1", "day2", "day3", "day4", "Yardage", "Par", "Rating"]
                already_written = {}
                with open(filename, mode="w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()

                    for data in tournament_array:
                
                        if data.get_id() not in already_written.keys():
                            writer.writerow({
                                "Tournament Name": data.get_name(),
                                "day1": data.get_day1(),
                                "day2": data.get_day2(),
                                "day3": data.get_day3(),
                                "day4": data.get_day4(),
                                "Yardage": data.get_yardage(),
                                "Par": data.get_par(),
                                "Rating": data.get_rating(),
                            })
                            already_written[data.get_id()] = True
                    
                print("CSV file created successfully.")


            return predictions(filename, day1, day2, day3, target_player_full_name, tournament_name)



# Define the main function
def main():
    # Prompt the user for input


    target_player_full_name = "Collin Morikawa"
    target_year = 2023
    day1 = 70
    day2 = 70
    day3 = 67
    tournament_name = "U.S. Open"

    # Call the data_retrieval function
    #print(data_retrieval(target_player_full_name, target_year, day1, day2, day3, tournament_name))
    data_retrieval(target_player_full_name, target_year, day1, day2, day3, tournament_name)

# Call the main function to start the program
if __name__ == "__main__":
    main()
