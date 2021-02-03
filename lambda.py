import random
import urllib
import re
import json
import random
import boto3
from botocore.exceptions import ClientError

sns = boto3.client('sns')


def restaurantPicker(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('restaurantpicker')
    
    intent = 'none'
    if ('intent' in event['request']):
        intent = event['request']['intent']['name']
        
    
    
    drinks = ["The Aardvark",
        "ALa Cart",
        "Bear and Peacock Brewstillery",
        "Buster's Bistro for belgian beers",
        "CityWorks at Disney Springs",
        "Ivanhoe Brewing",
        "Brew Theory",
        "GB Bottle Shop",
        "Geek Easy",
        "Genetic Brewing",
        "Half Barrel beer project",
        "Cloak and Blaster",
        "Motorworks Brewing",
        "The Nook",
        "Ravenous Pig Brewery",
        "Redlight Redlight",
        "Trader Sams Tiki place at Disneys Polynesian",
        "Thirsty Topher for a quiet good beer",
        "Tactical Brewing",
        "Wine Room",
        "Whippoorwill"]
        
    desserts = ["Gideons",
        "Allens ice cream",
        "Cocacola factory for a float flight",
        "Culvers",
        "The glass knife for tiny cake",
        "Hollarbachs for spaghetti ice cream",
        "Hop Daddys Shakes",
        "Everglazed Donuts - Disney Springs",
        "Kellys Ice Cream",
        "Krungthep tasty toast things",
        "Maggianos for Tiramisu",
        "The Macaron store in Winter Park",
        "Sugar Rush Marhsmallows Store",
        "P is for Pie",
        "Planet hollywood for cotton candy shake",
        "Salty Donut",
        "Shaka Donuts but remember that they close at 6",
        "Uncle Julios for the chocolate pinata",
        "Vallhalla Bakery because yolo",
        "wondermade marshmallows" ]

    restaurants = [        "Agave Azul for margaritas",
        "Asharwad or the Woodlands for indian food",
        "Art Smith Home Cooking (Shinebar)",
        "Ace Cafe",
        "A La Cart for food trucks",
        "Annas Polish Restaurant",
        "Bulla for potato chip fun",
        "Bosphorous for puffy bread",
        "Domu",
        "Downtown WOB",
        "Earls for midcentury modern",
        "The Edison",
        "Ethos for vegan",
        "Flemings for great service",
        "Gnarley Barley for tasty beers",
        "Habaneros mmmm chimichangas",
        "Highball and Harvest",
        "Lazy Moon",
        "LemonShark Poke",
        "King Bao",
        "Krungthep",
        "Maggianos for great drinks and food",
        "Market on South for vegan",
        "Meatball shoppe",
        "Pig Floyds",
        "Pizza Bruno for garlic knots",
        "Pho Hoa",
        "Poke Hana",
        "The Porch",
        "Rock N Brews",
        "Slate",
        "Smiling Bison",
        "Santiagos Bodega",
        "Taco Cheena",
        "Tin and Taco",
        "Thai food",
        "Sush-Hi",
        "Spoleto",
        "Wine Barn for pizza",
        "Yard house",
        "Yellow Dog Eats"]
        
    newrestaurants = ["Black Rooster Taquaria",
        "Baos Castle",
        "Chicken fire for Nashville hot chicken",
        "Mangos",
        "Hollarbachs Willow Tree",
        "Femme de Fromage for a cheese tray",
        "Hop daddys for burgers and shakes",
        "Hash house a go go",
        "Hillstone for a nice dinner on the lake",
        "Hungry Pants",
        "Kabuki sushi",
        "Maxines on Shine",
        "Mrs Potato for a roasty",
        "Pizza Press for pizza and beer",
        "QKenan Venezualan",
        "Seven Bites",
        "Salam Ethiopian",
        "Sticky Rice Lao street food",
        "Ravenous Pig",
        "Whisper creek for fancy"]
        
    if intent == 'newrestaurant':
        restaurants = newrestaurants
    else:
        newlist = newrestaurants + restaurants
        restaurants = newlist
    
            
    rest1 = random.randint(0, len(restaurants) - 1)
    restaurants.pop(rest1)
    rest2 = random.randint(0, len(restaurants) - 1)
    
    drink = random.randint(0, len(drinks) - 1)
    dessert = random.randint(0, len(desserts) - 1)

    responseText = 'You can select either ' + restaurants[rest1] + ' or ' + restaurants[rest2] + ', get drinks at ' + drinks[drink] + ", and dessert at " + desserts[dessert]
        
    
    if intent == "dessert":
        responseText = "Why not have dessert at " + desserts[dessert] + "?"
    elif intent == "drinks":
        responseText = "You should relax and have a drink at " + drinks[drink] + "."
    elif intent == "textme":

        try:
            response = table.get_item(Key={'last': "last"})
            print response['Item']['message']
            print("notifying sns")
            sns.publish(TargetArn='arn:aws:sns:us-east-1:619096257283:NotifyBestOfNetflix', Message=(response['Item']['message']) )
            responseText = "I texted you."
        except ClientError as e:
            print(e.response['Error']['Message'])
            
    if intent != "textme":
        try:
            table.put_item(Item={'last': "last", "message": responseText})    
        except ClientError as e:
                print(e.response['Error']['Message'])
                
    
   #responseText = responseText + ". The intent was " + intent        
    response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': responseText
            }
        }
    }
    
    return response

