from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

cafe = Blueprint('cafe', __name__)

def get_cafes():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    #query
    query = '''
            SELECT name, street, city, state, zip, Ratings.price 
            FROM Cafe c JOIN Ratings r ON c.cafe_id = r.cafe_id
        '''

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# --------------
#ENDPOINT 8
# --------------

# 8. METHOD 1 GET 
# Get all details of a cafe including its address 
@cafe.route('/cafe/<cafe_id>', methods=['GET'])
def get_cafe_details(cafe_id):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    #query the database for cafe details
    query = ('''
            SELECT * 
            FROM Cafe c JOIN Ratings r ON c.cafe_id = r.cafe_id JOIN Reviews re ON c.cafe_id = re.cafe_id 
            WHERE id = ''' + str(cafe_id))
    
    #Executing the query
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)


#8. METHOD 2 PUT
# Updating cafe information
@cafe.route('/cafe/<cafe_id>', methods=['PUT'])
def update_cafe_details(cafe_id):
    # Collecting data from the request object
    updated_data = request.json
    current_app.logger.info(updated_data)

    # Extracting variables
    # Assuming your cafe table has columns like time, days, website_link, etc.
    # Adjust these variable names based on your actual column names
    time = updated_data.get('time')
    days = updated_data.get('days')
    website_link = updated_data.get('website_link')
    name = updated_data.get('name')
    street = updated_data.get('street')
    city = updated_data.get('city')
    zip_code = updated_data.get('zip')
    state = updated_data.get('state')
    has_wifi = updated_data.get('has_wifi')
    has_outlets = updated_data.get('has_outlets')

    # Constructing the SQL UPDATE query
    query = f'''
        UPDATE cafes
        SET
            time = "{time}",
            days = "{days}",
            website_link = "{website_link}",
            name = "{name}",
            street = "{street}",
            city = "{city}",
            zip = "{zip_code}",
            state = "{state}",
            has_wifi = {has_wifi},
            has_outlets = {has_outlets}
        WHERE cafe_id = {cafe_id}
    '''
    current_app.logger.info(query)

    # Executing and committing the update statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Update successful'


#8.METHOD 3 DELETE
#Deleting cafe
@cafes.route('/cafe/<cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    # Constructing the SQL DELETE query
    query = f'''
        DELETE FROM cafes
        WHERE cafe_id = {cafe_id}
    '''
    current_app.logger.info(query)

    # Executing and committing the delete statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Cafe deleted'

# --------------
#ENDPOINT 10
# --------------


#10. METHOD 1 GET
#Getting social media links

@cafes.route('/cafe/<cafe_id>/<social_links>', methods=['GET'])
def get_cafe_social_links(cafe_id):
    # Constructing the SQL SELECT query to retrieve social media and website links
    query = f'''
        SELECT website_link
        FROM cafes
        WHERE cafe_id = {cafe_id}
    '''
    current_app.logger.info(query)

    # Executing the select statement
    cursor = db.get_db().cursor()
    cursor.execute(query)

    # Fetching the data from the cursor
    data = cursor.fetchone()

    # Checking if the cafe exists
    if not data:
        return jsonify({'error': 'Cafe not found'}), 404

    # Extracting the social media and website links
    website_link, social_media_link1, social_media_link2, social_media_link3 = data

    # Constructing the response JSON
    response_data = {
        'cafe_id': cafe_id,
        'website_link': website_link,
    }

    return jsonify(response_data)







