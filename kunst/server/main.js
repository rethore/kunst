import { Meteor } from 'meteor/meteor';
import { Hue } from '../imports/api/hue.js';
import { HTTP } from 'meteor/http';

//const IP = 'ip322.alb283.cust.comxnet.dk:6785';

const IP = process.env.API_URL;
console.log('API', IP);

Meteor.publish('hue', function hue() {
    return Hue.find();
});

Meteor.startup(() => {
  // code to run on server at startup

  // Set the backend python as inactive
  Meteor.call('hue.deactivate');
  if (!Hue.findOne({name:'url'})) {
    Hue.insert({name:'url', url:'https://plot.ly/~piredtu/36.embed'});
  }

  // Init active
  Hue.remove({name:'active'});
  Hue.insert({name:'active', val:false, panel:'none', data:{}});

  // Init heartbeat
  Hue.remove({name:'heartbeat'});
  var hb_id = Hue.insert({name:'heartbeat', val:false});
  Meteor.setInterval(
    ()=>HTTP.get(`http://${IP}/heartbeat`, {timeout:1000},
      (e,r)=>{
        if (e) Hue.update(hb_id, {name:'heartbeat', val:false})
        else if (r.content==='alive') Hue.update(hb_id, {name:'heartbeat', val:true})
          else Hue.update(hb_id, {name:'heartbeat', val:false})
      }),
    10000.0);
});

Meteor.methods({
  'hue.activate'(state='none', data={}){
      Hue.update({name:'active'}, {$set:{val:true, panel:state, data}});
  },
  'hue.deactivate'(){
      Hue.update({name:'active'}, {$set:{val:false, panel:'none', data:{}}});
  },
  'sunshow'(cmap, day, month, year){
    Meteor.call("hue.activate", 'sunshow', {day, month, year});
    //event.preventDefaults();
      HTTP.get(`http://${IP}/sun/${cmap}/${day}/${month}/${year}`, function(error, result){
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
    Meteor.call("hue.activate", 'rungame', {speed, tours});
    let url = `http://${IP}/run/${speed}/${tours}`;
    console.log(speed, tours, url);
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
    Meteor.call("hue.activate", 'download', {day, month, year});
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
