import xmlrpc.client

# Ask the user for their login and password (or API key)
login = input("Enter your login: ")
password = input("Enter your password: ")

# Connect to the instance of ODOO via XML-RPC
url = "http://localhost:8069"
db = "dev01"
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

# Authenticate the user
try:
    uid = common.authenticate(db, login, password, {})
except xmlrpc.client.Fault as error:
    print("An error occurred while authenticating:", error)

# Reference the "model" object
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Keep searching for apartments as long as the user wants to
searching = True
while searching:
    # Ask the user for the name of the apartment they want to search for
    name = input("Enter the name of the apartment you want to search for: ")

    # Search for the apartment
    try:
        apartment_ids = models.execute_kw(db, uid, password, 'realtor.apartment', 'search', [[['name', '=', name]]])
        if apartment_ids:
            # If the search returned any results, display them
            for apartment in apartment_ids:
                apartment_details = models.execute_kw(db, uid, password, 'realtor.apartment', 'read', [apartment_ids])
                print("Apartment found:")
                print('Name : {} Price: {} Description :{}'.format(apartment_details[0].get('name'),
                apartment_details[0].get('expected_price'),apartment_details[0].get('description')))
        else:
            # If the search didn't return any results, inform the user
            print("No apartments found with the name '{}'".format(name))
    except xmlrpc.client.Fault as error:
        print("An error occurred while searching:", error)

    # Ask the user if they want to search again
    response = input("Do you want to search again? (y/n) ")
    if response.lower() != 'y':
        searching = False