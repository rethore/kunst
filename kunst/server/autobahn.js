// import autobahn from 'autobahn';
//
// Meteor.publish('trollboxtest', function() {
//   const wsuri = "wss://api.poloniex.com";
//
//   const connection = new autobahn.Connection({
//     url: wsuri,
//     realm: "realm1"
//   });
//
//   const trollboxEvent = (args, kwargs) => {
//     const doc = {
//       type: args[0],
//       id: args[1],
//       name: args[2],
//       message: args[3]
//     }
//     console.log('new item', doc)
//     this.added('trollbox1', Random.id(), doc);
//     this.ready();
//   }
//
//   connection.onopen = (session) => {
//     session.subscribe('trollbox', trollboxEvent);
//     console.log("Websocket connection opened")
//   }
//
//   connection.onclose = (reason, details) => {
//     console.log("Websocket connection closed:", reason);
//   }
//
//   connection.open();
// });
// console.log('this was loaded');
