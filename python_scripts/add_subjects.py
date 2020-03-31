#!/usr/bin/env python3
import firebase_admin
from firebase_admin import credentials

from google.cloud import firestore
import json

if __name__ == "__main__":
 
    # Let's load the masters
    with open("../data/subjects.json") as file:
        subjects = json.load(file)

    # Open the DB connection
    db = firestore.Client()
    collection = db.collection("subjects")

    # Iterate over the masters
    for subject in subjects:
        id = subject["id"]

        # Let's remove the id key (to avoid conflict?)
        del subject["id"]
        collection.document(id).set(subject)
        print("Added: {}".format(subject["name"]))