import requests

class Fruit_elaman:
    def __init__(self, fruit_id, name, family, genus, order, carbohydrates, protein, fat, calories):
        self.fruit_id = fruit_id
        self.name = name
        self.family = family
        self.genus = genus
        self.order = order
        self.carbohydrates = carbohydrates
        self.protein = protein
        self.fat = fat
        self.calories = calories

    def display_info(self):
        print(f"ID: {self.fruit_id}")
        print(f"{self.name} - {self.family}")
        print(f"Genus: {self.genus}")
        print(f"Order: {self.order}")
        print(f"Nutritional Information:")
        print(f"  Carbohydrates: {self.carbohydrates}")
        print(f"  Protein: {self.protein}")
        print(f"  Fat: {self.fat}")
        print(f"  Calories: {self.calories}")
        print()

class FruityviceAPI:
    def __init__(self):
        self.api_url = 'https://www.fruityvice.com/api/fruit/all'
        self.fruits_data = None

    def fetch_data(self):
        try:
            # Make a GET request to the Fruityvice API
            response = requests.get(self.api_url)

            # Check if the request was successful (status code 200)
            response.raise_for_status()

            # Parse the JSON response
            self.fruits_data = response.json()

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print("Please check your internet connection or try again later.")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            print("Please check your internet connection or try again later.")
        except ValueError as json_err:
            print(f"JSON parsing error occurred: {json_err}")
            print("Unexpected response from the server. Please try again later.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please try again later.")

    def create_fruit_objects(self):
        fruits = []
        if self.fruits_data:
            for fruit_data in self.fruits_data:
                fruit = Fruit_elaman(
                    fruit_id=fruit_data['id'],
                    name=fruit_data['name'],
                    family=fruit_data['family'],
                    genus=fruit_data.get('genus', 'N/A'),
                    order=fruit_data.get('order', 'N/A'),
                    carbohydrates=fruit_data.get('nutritions', {}).get('carbohydrates', 'N/A'),
                    protein=fruit_data.get('nutritions', {}).get('protein', 'N/A'),
                    fat=fruit_data.get('nutritions', {}).get('fat', 'N/A'),
                    calories=fruit_data.get('nutritions', {}).get('calories', 'N/A')
                )
                fruits.append(fruit)
        return fruits

    def find_fruit_by_id(self, fruit_id):
        for fruit in self.create_fruit_objects():
            if fruit.fruit_id == fruit_id:
                return fruit
        return None

    def find_fruit_by_name(self, name):
        for fruit in self.create_fruit_objects():
            if fruit.name.lower() == name.lower():
                return fruit
        return None

    def find_fruit_by_family(self, family):
        for fruit in self.create_fruit_objects():
            if fruit.family.lower() == family.lower():
                return fruit
        return None
def get_user_choice():
    print("Choose the type of information you want:")
    print("1. Best fruits for weight loss")
    print("2. Best fruits for weight gain")
    print("3. Search fruit by ID")
    print("4. Search fruit by name")
    print("5. Search fruit by family")

    try:
        choice = int(input("Enter the number of your choice: "))
        return choice
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

def main():
    fruityvice = FruityviceAPI()
    fruityvice.fetch_data()

    user_choice = get_user_choice()

    if user_choice is not None:
        if user_choice == 1:
            weight = float(input("Enter your weight: "))
            print()
            if weight < 50:
                print("Considering your weight, you may want to eat fruits with calories greater than 50.")
                high_calorie_fruits = [fruit for fruit in fruityvice.create_fruit_objects() if fruit.calories > 50]
                if not high_calorie_fruits:
                    print("No fruits with calories greater than 50 available.")
                else:
                    print("Fruits with calories greater than 50:")
                    for index, fruit in enumerate(high_calorie_fruits, start=1):
                        print(f"{index}. {fruit.name} (ID: {fruit.fruit_id})")
            else:
                print("Considering your weight, you may want to eat a balanced diet of fruits.")
                for index, fruit in enumerate(fruityvice.create_fruit_objects(), start=1):
                    print(f"{index}. {fruit.name} (ID: {fruit.fruit_id})")
        elif user_choice == 2:
            print("Considering your weight, you may want to eat a balanced diet of fruits.")
            for index, fruit in enumerate(fruityvice.create_fruit_objects(), start=1):
                print(f"{index}. {fruit.name} (ID: {fruit.fruit_id})")
        elif user_choice == 3:
            try:
                fruit_id = int(input("Enter the ID of the fruit you want to view: "))
                selected_fruit = fruityvice.find_fruit_by_id(fruit_id)
                if selected_fruit:
                    selected_fruit.display_info()
                else:
                    print("Fruit not found.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        elif user_choice == 4:
            fruit_name = input("Enter the name of the fruit: ")
            selected_fruit = fruityvice.find_fruit_by_name(fruit_name)
            if selected_fruit:
                selected_fruit.display_info()
            else:
                print("Fruit not found.")
        elif user_choice == 5:
            fruit_family = input("Enter the family of the fruit: ")
            selected_fruit = fruityvice.find_fruit_by_family(fruit_family)
            if selected_fruit:
                selected_fruit.display_info()
            else:
                print("Fruit not found.")
        else:
            print("Invalid choice. Exiting.")
            return

if __name__ == "__main__":
    main()
