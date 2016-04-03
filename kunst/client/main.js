import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';

import './main.html';


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

Template.sunshow.onCreated(function sunshowOnCreaded(){
  this.in_use = new ReactiveVar(false);
});

Template.sunshow.helpers({
  disabled() {return (Template.instance().in_use.get())? "disabled" : ""}
});

Template.sunshow.events({
  'click button'(event, instance){
    instance.in_use.set(true);
    //event.preventDefaults();
    HTTP.get("http://81.161.138.239:6785/sun", function(error, result){
      if(error){
        console.log("error", error);
      }
      if(result){
         console.log("result", result)
         if (result.content === "done") {
           instance.in_use.set(false);
         }
      }
    });
  },
})

Template.rungame.onCreated(function rungameOnCreaded(){
  this.in_use = new ReactiveVar(false);
});


Template.rungame.helpers({
  disabled() {return (Template.instance().in_use.get())? "disabled" : ""}
});

Template.rungame.events({
  'click button'(event, instance){
    instance.in_use.set(true);
    let speed = $('#speed').val();
    let tours = $('#tours').val();
    let url = `http://81.161.138.239:6785/run/${speed}/${tours}`;
    console.log(event, instance, url, speed);
    //event.preventDefaults();
    HTTP.get(url, function(error, result){
      if(error){
        console.log("error", error);
      }
      if(result){
         console.log("result", result)
         if (result.content === "done") {
           instance.in_use.set(false);
         }
      }
    });
  },
})
