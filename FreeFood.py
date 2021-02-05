import requests,pprint,os
from configparser import ConfigParser

class FreeFood(object):
    # Variables to dynamically build api endpoint
    API_KEY = os.environ.get('API_KEY')
    API_KEY_NAME = ''
    BASE_END_POINT = ''
    RECIPE_SUMMARY_END_POINT = ''
    RECIPE_PRICE_END_POINT = ''
    RECIPE_BY_INGREDIENTS_END_POINT = ''
    
    # Final user Shopping List
    user_shopping_dict = []
    
    def load_configurations(self):
        """Load config.properties 
        :return: None
        """
        config = ConfigParser()
        config.read('./config/config.properties')
        self.API_KEY_NAME = config.get('PRD','API_KEY_NAME')
        self.BASE_END_POINT = config.get('PRD','BASE_END_POINT')
        self.RECIPE_SUMMARY_END_POINT = config.get('PRD','RECIPE_SUMMARY_END_POINT')
        self.RECIPE_BY_INGREDIENTS_END_POINT = config.get('PRD','RECIPE_BY_INGREDIENTS_END_POINT')
        self.RECIPE_PRICE_END_POINT = config.get('PRD','RECIPE_PRICE_END_POINT')
        return 

    def get_response(self, payload, http_method):
        """Given http_method address retuens the JSON response
        Args:
            param1: http_method to invoke
        Returns:
            Returns JSON response for the GET method
        """
        try:
            final_endpoint = self.BASE_END_POINT+http_method+self.API_KEY_NAME+self.API_KEY
            response = requests.get(final_endpoint, params=payload, timeout=6.0)
            # Raise HTTPError in case HTTP request returned an unsuccessful status code
            response.raise_for_status()
        except requests.ConnectionError as e:
            print("ERROR: Connection Error, check your network connection (internet issue)\n")
            print(f"ERROR: ErrorTrace for debugging:\n {str(e)}")
        except requests.exceptions.HTTPError as err:
            print("ERROR: Invalid HTTP Response")
            print(f"ERROR: ErrorTrace for debugging:\n {str(err)}")
        except requests.Timeout as e:
            print("ERROR: Timeout Error")
            print(f"ERROR: ErrorTrace for debugging:\n {str(e)}")
        except requests.RequestException as e:
            print("ERROR: General Errors")
            print(f"ERROR: ErrorTrace for debugging:\n {str(e)}")
        else:
            return response.json()
    
    def get_recipe_by_ingredients(self, ingredients):
        """Given comma seperated string of ingredients, return recipes
        Args:
            param1: string of ingredients ex: apple,banana
        Returns:
            Returns list of JSON Recipes
        """
        payload = {
            'ingredients': ingredients,
            'number': 100,
            'limit_license': False,
            'ranking': 1,
            'ignore_pantry': True
        }
        return self.get_response(payload, self.RECIPE_BY_INGREDIENTS_END_POINT)
    
    def get_recipe_summary(self, recipe_id):
        """Given a recipe_id get's the summary of recipe
        Args:
            param1: int value of recipe_id
        Returns:
            Returns JSON containing Recipe Summary
        """
        payload = {
            'id': recipe_id
        }
        return self.get_response(payload, self.RECIPE_SUMMARY_END_POINT.replace('{id}', str(recipe_id)))
    
    def get_ingredient_price(self, recipe_id):
        """Given a recipe_id get's the price of every ingredients in recipe
        Args:
            param1: int value of recipe_id
        Returns:
            Returns JSON containing Recipe Price Summary
        """
        payload = {
            'id': recipe_id
        }
        return self.get_response(payload, self.RECIPE_PRICE_END_POINT.replace('{id}', str(recipe_id)))
    
    def process_price_response(self, price_response):
        """Given a price_response returns dictionary of ingredients name and price
        Args:
            param1: JSON price response
        Returns:
            Returns dictionary containing ingredient's name & price
        """
        return { price["name"]: price["price"] for price in price_response["ingredients"] }
        
    def process_recipe_response(self, ingredients_response):
        """Given a JSON ingredients_response provess the response
        Args:
            param1: JSON value of ingredient response
        Returns:
            Returns JSON response of Shopping List
        """
        # Loop through the API response until the user is satisfied with a recipe
        for recipe in ingredients_response:
            # Get a Recipe Summary for the given Recipe ID
            recipe_summary = self.get_recipe_summary(recipe["id"])
            print(f"\nHere is the summary of a new Recipe: {recipe['title']} \n")
            pprint.pprint(recipe_summary['summary'])
            
            # Ask User if he/she is satisfied with the recipe
            user_satisfaction = input('\nDo you like this recipe??, please enter yes or no: ')
            while user_satisfaction.lower() not in ['yes','no']:
                print('Invalid Input')
                user_satisfaction = input('Do you like this recipe??, please enter yes or no: ')
            if user_satisfaction.lower() == 'yes':
                
                # Price dictionary consists of pricing for every ingredient in the recipe
                price_dictionary = self.process_price_response(self.get_ingredient_price(recipe["id"]))
                
                # Add Meta prefixes, and check
                for missedIngrd in recipe['missedIngredients']:
                    # Check if ingredient is available in Price Dictionary
                    if missedIngrd['name'] in price_dictionary:
                        ingredient_price = price_dictionary[missedIngrd['name']]
                    else:
                        # Now check appending Meta Tags
                        for metaTag in missedIngrd["meta"]:
                            if metaTag+" "+missedIngrd['name'] in price_dictionary:
                                ingredient_price = price_dictionary[metaTag+" "+missedIngrd['name']]
                        
                    
                    self.user_shopping_dict.append(
                        {
                            'ingredientName': missedIngrd['name'],
                            'aisleName': missedIngrd['aisle'],
                            'quantity': missedIngrd['amount'],
                            'estimatedCost': ingredient_price
                        }
                    )
                break

if __name__ == "__main__":
    # Instantiate Ingredients class
    my_recipe = FreeFood()
    
    # Load configFiles
    my_recipe.load_configurations()
    
    # Step1: Get UserInputs from CLI
    ingredients_str = input('Enter comma seperated list of ingredients ex. apple,banana: ')
    
    # Step2: Given Ingredients now get the Recipes
    ingredients_response = my_recipe.get_recipe_by_ingredients(ingredients_str)
    
    # Step3: Get Recipe Summary, and factor user choices
    if bool(ingredients_response):
        my_recipe.process_recipe_response(ingredients_response)
        print("\nPlease find below the Shopping List to buy this item: \n")
        pprint.pprint(my_recipe.user_shopping_dict)
    # If the User's list of ingredients did not yield any Recipes
    else:
        print("\n No Recipes found for the given list of ingredients \n")