import { Meteor } from 'meteor/meteor';
import { Hue } from '../imports/api/hue.js';

Meteor.startup(() => {
  // code to run on server at startup

  // Set the backend python as inactive
  Meteor.call('hue.deactivate');
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

});
