#!/usr/bin/env python3
import firebase_admin
from firebase_admin import credentials

from google.cloud import firestore
import json

if __name__ == "__main__":
 
    # Let's load the masters
    with open("../data/masters.json") as file:
        masters = json.load(file)

    # Open the DB connection
    db = firestore.Client()
    collection = db.collection("masters")

    # Iterate over the masters
    for master in masters:
        id = master["id"]

        # Let's remove the id key (to avoid conflict?)
        del master["id"]
        collection.document(id).set(master)
        print("Added: {}".format(master["name"]))

