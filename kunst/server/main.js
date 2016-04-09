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
  'hue.activate'(state='none'){
    let hue_status = Hue.findOne({name:'active'})
    if (hue_status) {
      Hue.update({name:'active'}, {$set:{val:true, panel:state}});
    } else {
      Hue.insert({name:'active', val:true, panel:state});
    }
  },
  'hue.deactivate'(){
    let hue_status = Hue.findOne({name:'active'})
    if (hue_status) {
      Hue.update({name:'active'}, {$set:{val:false, panel:'none'}});
    } else {
      Hue.insert({name:'active', val:false, panel:'none'});
    }
  },
  'sunshow'(cmap){
    Meteor.call("hue.activate", 'sunshow');
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
    Meteor.call("hue.activate", 'rungame');
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
    Meteor.call("hue.activate", 'download');
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
  },
  'on'(){
    let url = `http://${IP}/on`;
    HTTP.get(url, function(error, result){
      if(error){
        console.log("error", error);
      }
      if(result){
         console.log("result", result)
         if (result.content == 'done') {
           console.log('plot detected:', result.content)
         } else {
           console.log('error:', result)
         }
      }
    });
  },
  'off'(){
    let url = `http://${IP}/off`;
    HTTP.get(url, function(error, result){
      if(error){
        console.log("error", error);
      }
      if(result){
         console.log("result", result)
         if (result.content == 'done') {
           console.log('lights are off', result.content)
         } else {
           console.log('error:', result)
         }
      }
    });
  },
  'effect'(effect_type){
    let url = `http://${IP}/effect/${effect_type}`;
    HTTP.get(url, function(error, result){
      if(error){
        console.log("error", error);
      }
      if(result){
         console.log("result", result)
         if (result.content == 'done') {
           console.log('lights effect is changed', result.content)
         } else {
           console.log('error:', result)
         }
      }
    });
  },
});
