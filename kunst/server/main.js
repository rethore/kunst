import { Meteor } from 'meteor/meteor';
import { Hue } from '../imports/api/hue.js';

const IP = 'ip322.alb283.cust.comxnet.dk:6785';


Meteor.startup(() => {
  // code to run on server at startup

  // Set the backend python as inactive
  Meteor.call('hue.deactivate');
  if (!Hue.findOne({name:'url'})) {
    Hue.insert({name:'url', url:'https://plot.ly/~piredtu/36'});
  }
});

Meteor.methods({
  'hue.activate'(){
    let hue_status = Hue.findOne({name:'active'})
    if (hue_status) {
      Hue.update({name:'active'}, {$set:{val:true}});
    } else {
      Hue.insert({name:'active', val:true});
    }
  },
  'hue.deactivate'(){
    let hue_status = Hue.findOne({name:'active'})
    if (hue_status) {
      Hue.update({name:'active'}, {$set:{val:false}});
    } else {
      Hue.insert({name:'active', val:false});
    }
  },
  'sunshow'(cmap){
    Meteor.call("hue.activate");
    //event.preventDefaults();
      HTTP.get(`http://${IP}/sun/${cmap}`, function(error, result){
        if(error){
          console.log("error", error);
        }
        if(result){
           console.log("result", result)
           if (result.content === "done") {
             Meteor.call("hue.deactivate");
           }
        }
      });
  },
  'rungame'(speed, tours){
    Meteor.call("hue.activate");
    let url = `http://${IP}/run/${speed}/${tours}`;
    console.log(event, instance, url, speed);
    HTTP.get(url, function(error, result){
      if(error){
        console.log("error", error);
      }
      if(result){
         console.log("result", result)
         if (result.content === "done") {
           Meteor.call("hue.deactivate");
         }
      }
    });
  },
  'download'(day, month, year){
    Meteor.call("hue.activate");
    let url = `http://${IP}/download/${day}/${month}/${year}`;
    HTTP.get(url, function(error, result){
      if(error){
        console.log("error", error);
      }
      if(result){
         console.log("result", result)
         if (result.content.includes('plot')) {
           console.log('plot detected:', result.content)
           Hue.insert({name:'data', day, month, year, url:result.content});
         } else {
           console.log('error:', result)
         }
         Meteor.call("hue.deactivate");
      }
    });
  }

});
