const admin = require("firebase-admin");
const fs = require("fs");
const firestoreService = require("firestore-export-import");
const firebaseConfig = require("./config.js");
//const serviceAccount = require("./serviceAccount.json")

let serviceAccount = require("./serviceAccount.json");
admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: "https://uc3m-it-1920-16147-g3.firebaseio.com"
  });
let db = admin.firestore();

(async () => {
  try {
      // Read JSON from file
      let rawdata = fs.readFileSync("./data/subjects.json");
      let example = JSON.parse(rawdata);

      
      example.forEach(async(element) => {
        
        // Add data to Firestore in native mode
        await db.collection("subjects").doc(element["id"]).set(element);
        console.log("Added JSON to Firestore:", element["id"]);
      
        
      });
      
      // Read data
      //let readDoc = await db.collection("json").doc("./data/masters").get();
      //console.log("Read JSON from Firestore:", readDoc);
      //console.log("Accesing to data:", readDoc.data().firstName, readDoc.data().lastName);

  } catch (error) {
      console.error("Error happened:", error);
  }
})();