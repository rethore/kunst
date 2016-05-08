import { Mongo } from 'meteor/mongo';
import { Connection } from 'autobahn';

// local collection because of the null
var Trollbox = new Mongo.Collection(null);

Template.trollbox.onCreated(function() {
  const connection = new Connection({
    url: "wss://api.poloniex.com",
    realm: "realm1"
  });

  const trollboxEvent = (args, kwargs) => {
    const doc = {
      type: args[0],
      id: args[1],
      name: args[2],
      message: args[3]
    }
    console.log('new item', doc)
    Trollbox.insert(doc)
  }

  connection.onopen = (session) => {
    session.subscribe('trollbox', trollboxEvent);
    console.log("Websocket connection opened")
  }

  connection.onclose = (reason, details) => {
    console.log("Websocket connection closed:", reason);
  }

  connection.open();
});

Template.trollbox.helpers({
  myHelper: () => Trollbox.find({}),
});
