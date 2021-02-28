var firebaseConfig = {
  apiKey: "",
  authDomain: "",
  projectId: "",
  storageBucket: "",
  messagingSenderId: "",
  appId: "",
  measurementId: ""
};
firebase.initializeApp(firebaseConfig);
var firestore = firebase.firestore();

const docRef = firestore.collection("samples").doc("sandwichData")
const outputHeader = document.querySelector("#hotDogOutput");
const inputTextField = document.querySelector("#latestHotDogStatus");
const saveButton = document.querySelector("#saveButton");
const loadButton = document.querySelector("#loadButton");

saveButton.addEventListener("click", function() {
  const textToSave = inputTextField.value;
  console.log("I am going to save " + textToSave + " to FireStore");
  docRef.set({
    hotDogStatus: textToSave
  }).then(function() {
    console.log("Status saved!");
  }).catch(function(error) {
    console.log("Got an error: ", error);
  })
});

loadButton.addEventListener("click", function() {
  docRef.get().then(function(doc) {
    if(doc && doc.exists) {
      const myData = doc.data();
      outputHeader.innerText = "Hot dog status: " + myData.hotDogStatus;
    }
  }).catch(function(error) {
    console.log("Got an error: ", error);
  });
});

getRealtimeUpdates = function() {
  docRef.onSnapshot(function(doc) {
   if(doc && doc.exists) {
     const myData = doc.data();
     console.log("Check out this document I received ", doc);
     outputHeader.innerText = "Hot dog status: " + myData.hotDogStatus;
   }
  })
}

getRealtimeUpdates();