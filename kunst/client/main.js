import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';
import { Hue } from '../imports/api/hue.js';

import './main.html';


const IP = 'ip322.alb283.cust.comxnet.dk:6785';

Template.hello.onCreated(function helloOnCreated() {
  // counter starts at 0
  this.counter = new ReactiveVar(0);
});

Template.hello.helpers({
  counter() {
    return Template.instance().counter.get();
  },
});

Template.hello.events({
  'click button'(event, instance) {
    // increment the counter when button is clicked
    instance.counter.set(instance.counter.get() + 1);
  },
});

Template.sunshow.helpers({
  disabled() {return (Hue.findOne({name:'active'}))? (Hue.findOne({name:'active'}).val)? "disabled" : "" : ""}
});

Template.sunshow.events({
  'click button'(event, instance){
    Meteor.call("hue.activate");
    //event.preventDefaults();
    HTTP.get(`http://${IP}/sun`, function(error, result){
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
})




Template.rungame.helpers({
    disabled() {return (Hue.findOne({name:'active'}))?
        (Hue.findOne({name:'active'}).val)? "disabled" : "" : ""}
});

Template.rungame.events({
  'click button'(event, instance){
    Meteor.call("hue.activate");
    let speed = $('#speed').val();
    let tours = $('#tours').val();
    let url = `http://${IP}/run/${speed}/${tours}`;
    console.log(event, instance, url, speed);
    //event.preventDefaults();
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
})

Template.lamps.events({
  'click .glyphicon-refresh'(event, instance){
      console.log('click!');
  }
});
